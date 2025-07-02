from channels.generic.websocket import AsyncWebsocketConsumer
import json
import uuid
from .stream_manager import stream_manager
from .ffmpeg_processor import ffmpeg_processor
from .redis_service import redis_service

class StreamConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer - handles real-time stream communication"""
        
    async def connect(self):
        await self.accept()
        self.user_id = str(uuid.uuid4())
        self.user_streams = set()
        
        # Join user group in Redis
        await redis_service.add_user_to_group(self.user_id, self.channel_name)
        
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'user_id': self.user_id
        }))
        
        print(f"User connected: {self.user_id}")

    async def disconnect(self, close_code):
        """Enhanced cleanup on disconnect"""
        print(f"User disconnecting: {self.user_id}")
        
        # Clean up ALL user streams
        streams_to_cleanup = list(self.user_streams)
        
        for stream_id in streams_to_cleanup:
            try:
                should_stop = stream_manager.remove_user_from_stream(stream_id, self.user_id)
                await self.channel_layer.group_discard(f"stream_{stream_id}", self.channel_name)
                await redis_service.remove_user_from_stream_group(stream_id, self.channel_name)
                
                if should_stop:
                    print(f"Stopping FFmpeg for stream: {stream_id}")
                    await ffmpeg_processor.stop_stream_processing(stream_id)
                    
            except Exception as e:
                print(f"Error cleaning up stream {stream_id}: {e}")
        
        await redis_service.remove_user_from_group(self.user_id, self.channel_name)
        print(f"User disconnected: {self.user_id}")

    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            action = data.get('action')

            if action == 'add_stream':
                await self.handle_add_stream(data)
            elif action == 'remove_stream':
                await self.handle_remove_stream(data)
            elif action == 'get_streams':
                await self.handle_get_streams(data)
            else:
                await self.send_error(f"Unknown action: {action}")
                
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format")
        except Exception as e:
            await self.send_error(f"Error processing request: {str(e)}")
            print(f"Error in receive: {e}")

    async def handle_add_stream(self, data):
        """Orchestrate adding new stream with duplicate handling"""
        rtsp_url = data.get('url')
        title = data.get('title')
        
        if not rtsp_url or not rtsp_url.startswith('rtsp://'):
            await self.send_error("Invalid RTSP URL format")
            return
        
        try:
            # Business logic
            stream_id = stream_manager.generate_stream_id(rtsp_url)
            
            # Check if stream exists and clean it up if needed
            existing_stream = stream_manager.get_stream(stream_id)
            
            if existing_stream:
                print(f"Stream {stream_id} already exists, checking status...")
                
                # Check if FFmpeg process is still running
                if stream_id not in ffmpeg_processor.active_processes:
                    print(f"Stream {stream_id} FFmpeg stopped, cleaning up...")
                    stream_manager.streams.pop(stream_id, None)
                    existing_stream = None
            
            if existing_stream:
                # Add user to existing active stream
                stream_manager.add_user_to_stream(stream_id, self.user_id)
                print(f"Added user to existing stream: {stream_id}")
            else:
                # Create new stream (or recreate cleaned up stream)
                stream = stream_manager.create_stream(rtsp_url, title, self.user_id)
                print(f"Created new stream: {stream_id}")
                
                # Start FFmpeg processing
                await ffmpeg_processor.start_stream_processing(stream_id, rtsp_url)
            
            # Join WebSocket group
            await self.channel_layer.group_add(f"stream_{stream_id}", self.channel_name)
            
            # Redis management
            await redis_service.add_user_to_stream_group(stream_id, self.channel_name)
            await redis_service.store_stream_info(stream_id, stream_manager.get_stream(stream_id))
            
            self.user_streams.add(stream_id)
            
            await self.send(text_data=json.dumps({
                'type': 'stream_added',
                'stream_id': stream_id,
                'url': rtsp_url,
                'title': title or f'Stream {stream_id[:6]}'
            }))
            
        except Exception as e:
            await self.send_error(f"Failed to add stream: {str(e)}")
            print(f"Error adding stream: {e}")

    async def handle_remove_stream(self, data):
        """Handle removing stream with proper cleanup"""
        stream_id = data.get('stream_id')
        
        if not stream_id:
            await self.send_error("Stream ID is required")
            return
        
        try:
            print(f"Removing stream: {stream_id}")
            
            # Remove user from stream
            should_stop = stream_manager.remove_user_from_stream(stream_id, self.user_id)
            
            # Leave WebSocket group
            await self.channel_layer.group_discard(f"stream_{stream_id}", self.channel_name)
            await redis_service.remove_user_from_stream_group(stream_id, self.channel_name)
            
            # Stop FFmpeg if no users left
            if should_stop:
                print(f"Stopping FFmpeg for stream: {stream_id}")
                await ffmpeg_processor.stop_stream_processing(stream_id)
            
            self.user_streams.discard(stream_id)
            
            await self.send(text_data=json.dumps({
                'type': 'stream_removed',
                'stream_id': stream_id
            }))
            
            print(f"Successfully removed stream: {stream_id}")
            
        except Exception as e:
            await self.send_error(f"Failed to remove stream: {str(e)}")
            print(f"Error removing stream: {e}")

    async def handle_get_streams(self, data):
        """Get user's active streams"""
        try:
            user_streams = stream_manager.get_user_streams(self.user_id)
            streams_data = [stream.to_dict() for stream in user_streams]
            
            await self.send(text_data=json.dumps({
                'type': 'streams_list',
                'streams': streams_data
            }))
            
        except Exception as e:
            await self.send_error(f"Failed to get streams: {str(e)}")

    async def stream_data(self, event):
        """Handle stream data broadcast"""
        await self.send(text_data=json.dumps({
            'type': 'stream_data',
            'stream_id': event['stream_id'],
            'chunk': event['chunk'],
            'timestamp': event['timestamp'],
            'segment_name': event.get('segment_name', 'unknown'),
            'chunk_size': event.get('chunk_size', 0)
        }))

    async def stream_status(self, event):
        """Handle stream status updates"""
        await self.send(text_data=json.dumps({
            'type': 'stream_status',
            'stream_id': event['stream_id'],
            'status': event['status'],
            'message': event.get('message', '')
        }))

    async def send_error(self, message):
        """Send error message to frontend"""
        await self.send(text_data=json.dumps({
            'type': 'error', 
            'message': message
        }))
