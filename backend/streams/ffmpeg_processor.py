import asyncio
import os
import tempfile
import json
from datetime import datetime
from channels.layers import get_channel_layer
import redis.asyncio as redis
import base64
import logging

# Add this after the class definition
logger = logging.getLogger(__name__)

class FFmpegProcessor:
    def __init__(self):
        self.active_processes = {}  # stream_id: process_info
        self.channel_layer = get_channel_layer()
        self.redis_url = os.environ.get('REDIS_URL', 'redis://redis:6379')
    
    async def start_stream_processing(self, stream_id, rtsp_url):
        """Start FFmpeg process for RTSP stream conversion with enhanced error handling"""
        if stream_id in self.active_processes:
            logger.info(f"Stream {stream_id} already processing")
            return
        
        try:
            logger.info(f"Starting stream processing for {stream_id}")
            
            # Validate RTSP URL first (but don't fail if validation fails)
            is_valid = await self.validate_rtsp_url(rtsp_url)
            if not is_valid:
                logger.warning(f"RTSP URL validation failed, but proceeding anyway")
            
            # Create temporary directory for HLS segments
            temp_dir = tempfile.mkdtemp(prefix=f"stream_{stream_id}_")
            playlist_path = os.path.join(temp_dir, "playlist.m3u8")
            
            # Enhanced FFmpeg command for live streaming
            ffmpeg_cmd = [
                'ffmpeg',
                '-rtsp_transport', 'tcp',
                '-i', rtsp_url,
                '-f', 'hls',
                '-hls_time', '2',                    # 2-second segments
                '-hls_list_size', '3',               # Keep only 3 segments in playlist
                '-hls_flags', 'delete_segments+append_list+omit_endlist',  # Live stream flags
                '-hls_start_number_source', 'epoch', # Use timestamp-based numbering
                '-hls_segment_filename', os.path.join(temp_dir, 'segment_%03d.ts'),
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-tune', 'zerolatency',
                '-profile:v', 'baseline',            # Better compatibility
                '-level', '3.0',
                '-g', '30',                          # 2-second GOP (15fps * 2)
                '-sc_threshold', '0',
                '-b:v', '500k',                      # Lower bitrate for stability
                '-maxrate', '600k',
                '-bufsize', '1200k',
                '-s', '640x480',
                '-r', '15',
                '-c:a', 'aac',
                '-b:a', '64k',
                '-ac', '1',
                '-avoid_negative_ts', 'make_zero',
                '-fflags', '+genpts',                # Generate PTS
                '-loglevel', 'error',                # Reduced FFmpeg logging
                playlist_path
            ]
            
            logger.info(f"Starting FFmpeg for stream {stream_id}")
            
            # Start FFmpeg process
            process = await asyncio.create_subprocess_exec(
                *ffmpeg_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            print(f"FFmpeg process started for stream: {stream_id}")
            
            # Store process info
            self.active_processes[stream_id] = {
                'process': process,
                'temp_dir': temp_dir,
                'playlist_path': playlist_path,
                'rtsp_url': rtsp_url,
                'started_at': datetime.now()
            }
            
            # Update Redis status
            await self.update_stream_status(stream_id, 'active', 'Stream processing started')
            
            # Start monitoring tasks
            asyncio.create_task(self.monitor_ffmpeg_process(stream_id))
            asyncio.create_task(self.stream_hls_segments(stream_id))
            
            logger.info(f"Successfully started FFmpeg processing for stream {stream_id}")
            
        except Exception as e:
            logger.error(f"Failed to start stream {stream_id}: {e}")
            print(f"Failed to start stream {stream_id}: {e}")
            await self.update_stream_status(stream_id, 'error', str(e))
            raise Exception(f"Failed to start stream processing: {str(e)}")

    async def monitor_ffmpeg_process(self, stream_id):
        """Enhanced monitoring with essential logging only"""
        if stream_id not in self.active_processes:
            return
        
        process_info = self.active_processes[stream_id]
        process = process_info['process']
        
        try:
            # Read stderr for FFmpeg logs
            while True:
                line = await process.stderr.readline()
                if not line:
                    break
                
                log_line = line.decode('utf-8').strip()
                if log_line:
                    # Only log critical errors
                    if 'Connection refused' in log_line or 'No route to host' in log_line:
                        print(f"RTSP connection failed for {stream_id}")
                        await self.update_stream_status(stream_id, 'error', 'RTSP connection failed')
                        break
                    elif 'Invalid data found' in log_line:
                        print(f"Invalid RTSP stream for {stream_id}")
                        await self.update_stream_status(stream_id, 'error', 'Invalid RTSP stream')
                        break
                    elif 'error' in log_line.lower() or 'failed' in log_line.lower():
                        print(f"FFmpeg error [{stream_id}]: {log_line}")
            
            # Wait for process to complete
            return_code = await process.wait()
            if return_code != 0:
                print(f"FFmpeg process for {stream_id} ended with error code {return_code}")
                await self.update_stream_status(stream_id, 'error', f'FFmpeg exited with code {return_code}')
            
        except Exception as e:
            print(f"Error monitoring FFmpeg for {stream_id}: {e}")
            await self.update_stream_status(stream_id, 'error', str(e))
        
        finally:
            # Cleanup
            await self.stop_stream_processing(stream_id)
    
    async def stream_hls_segments(self, stream_id):
        """Monitor HLS segments and stream them via WebSocket"""
        if stream_id not in self.active_processes:
            return
        
        process_info = self.active_processes[stream_id]
        temp_dir = process_info['temp_dir']
        
        processed_segments = set()
        
        try:
            while stream_id in self.active_processes:
                try:
                    # Check if directory exists
                    if not os.path.exists(temp_dir):
                        await asyncio.sleep(2)
                        continue
                    
                    # Check for new HLS segments
                    files = os.listdir(temp_dir)
                    for filename in files:
                        if filename.endswith('.ts') and filename not in processed_segments:
                            segment_path = os.path.join(temp_dir, filename)
                            
                            # Wait a bit to ensure segment is fully written
                            await asyncio.sleep(1)
                            
                            if os.path.exists(segment_path) and os.path.getsize(segment_path) > 0:
                                await self.send_hls_segment(stream_id, segment_path)
                                processed_segments.add(filename)
                                
                except FileNotFoundError:
                    pass
                except Exception as e:
                    print(f"Error scanning directory for {stream_id}: {e}")
                
                # Wait before checking again
                await asyncio.sleep(2)
                
        except Exception as e:
            print(f"Error streaming HLS segments for {stream_id}: {e}")

    async def send_hls_segment(self, stream_id, segment_path):
        """Send HLS segment"""
        try:
            # Read segment file
            with open(segment_path, 'rb') as f:
                segment_data = f.read()
            
            # Validate chunk data
            chunk_size = len(segment_data)
            if chunk_size == 0:
                return
            
            # Encode as base64
            segment_b64 = base64.b64encode(segment_data).decode('utf-8')
            
            # Basic validation - check for MPEG-TS sync byte
            if not segment_data.startswith(b'\x47'):
                return
            
            # Broadcast to all users watching this stream
            await self.channel_layer.group_send(
                f"stream_{stream_id}",
                {
                    'type': 'stream_data',
                    'stream_id': stream_id,
                    'chunk': segment_b64,
                    'timestamp': datetime.now().isoformat(),
                    'segment_name': os.path.basename(segment_path),
                    'chunk_size': chunk_size
                }
            )
                
        except Exception as e:
            print(f"Error sending HLS segment for {stream_id}: {e}")

    async def stop_stream_processing(self, stream_id):
        """Stop FFmpeg process and cleanup resources"""
        if stream_id not in self.active_processes:
            return
        
        try:
            process_info = self.active_processes[stream_id]
            process = process_info['process']
            temp_dir = process_info['temp_dir']
            
            # Terminate FFmpeg process
            if process.returncode is None:
                process.terminate()
                try:
                    await asyncio.wait_for(process.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
            
            # Cleanup temporary files
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
            # Remove from active processes
            del self.active_processes[stream_id]
            
            # Update status
            await self.update_stream_status(stream_id, 'stopped', 'Stream processing stopped')
            
            print(f"Stopped FFmpeg processing for stream {stream_id}")
            
        except Exception as e:
            print(f"Error stopping FFmpeg for {stream_id}: {e}")
    
    async def update_stream_status(self, stream_id, status, message=None):
        """Update stream status in Redis and notify clients"""
        try:
            r = redis.from_url(self.redis_url)
            
            # Update Redis
            await r.hset(f"stream:{stream_id}", "status", status)
            if message:
                await r.hset(f"stream:{stream_id}", "last_message", message)
            
            await r.close()
            
            # Notify all viewers
            await self.channel_layer.group_send(
                f"stream_{stream_id}",
                {
                    'type': 'stream_status',
                    'stream_id': stream_id,
                    'status': status,
                    'message': message or ''
                }
            )
            
        except Exception as e:
            print(f"Error updating stream status for {stream_id}: {e}")
    
    async def get_stream_info(self, stream_id):
        """Get detailed stream information"""
        if stream_id not in self.active_processes:
            return None
        
        process_info = self.active_processes[stream_id]
        return {
            'stream_id': stream_id,
            'rtsp_url': process_info['rtsp_url'],
            'started_at': process_info['started_at'].isoformat(),
            'temp_dir': process_info['temp_dir'],
            'is_running': process_info['process'].returncode is None
        }

    async def validate_rtsp_url(self, rtsp_url):
        """Quick validation of RTSP URL accessibility"""
        try:
            logger.info(f"Validating RTSP URL")
            
            # Quick FFmpeg probe to check if URL is accessible
            probe_cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_streams', '-timeout', '10000000',  # 10 second timeout
                '-rtsp_transport', 'tcp',  # Force TCP transport
                rtsp_url
            ]
            
            process = await asyncio.create_subprocess_exec(
                *probe_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=15)
                
                if process.returncode == 0:
                    logger.info(f"RTSP URL validation successful")
                    return True
                else:
                    logger.warning(f"RTSP URL validation failed")
                    return True  # Let FFmpeg try anyway
                    
            except asyncio.TimeoutError:
                logger.warning(f"RTSP URL validation timeout")
                process.kill()
                return True  # Let FFmpeg try anyway
            
        except Exception as e:
            logger.warning(f"RTSP URL validation error: {e}")
            return True  # Let FFmpeg try anyway
        
    async def update_playlist_urls(self, stream_id, playlist_path):
        """Update playlist to use proper HTTP URLs"""
        try:
            if os.path.exists(playlist_path):
                with open(playlist_path, 'r') as f:
                    content = f.read()
                
                # Replace relative paths with full URLs
                lines = content.split('\n')
                updated_lines = []
                
                for line in lines:
                    if line.endswith('.ts'):
                        # Convert to HTTP URL
                        segment_name = os.path.basename(line)
                        http_url = f"http://localhost:8000/api/hls/{stream_id}/{segment_name}"
                        updated_lines.append(http_url)
                    else:
                        updated_lines.append(line)
                
                # Write updated playlist
                updated_content = '\n'.join(updated_lines)
                with open(playlist_path, 'w') as f:
                    f.write(updated_content)
                    
        except Exception as e:
            print(f"Error updating playlist URLs: {e}")

# Global FFmpeg processor instance
ffmpeg_processor = FFmpegProcessor()
