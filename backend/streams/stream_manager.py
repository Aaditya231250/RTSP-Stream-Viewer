import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import hashlib
from .models import StreamInfo, UserConnection

class StreamManager:
    """Centralized stream management"""
    
    def __init__(self):
        self.streams: Dict[str, StreamInfo] = {}
        self.user_connections: Dict[str, UserConnection] = {}
    
    def generate_stream_id(self, rtsp_url: str) -> str:
        """Generate unique stream ID"""
        return hashlib.md5(rtsp_url.encode()).hexdigest()[:12]
    
    def add_user_to_stream(self, stream_id: str, user_id: str) -> bool:
        """Add user to existing stream"""
        if stream_id in self.streams:
            if user_id not in self.streams[stream_id].viewers:
                self.streams[stream_id].viewers.append(user_id)
            return True
        return False
    
    def remove_user_from_stream(self, stream_id: str, user_id: str) -> bool:
        """Remove user from stream, return True if stream should be stopped"""
        if stream_id in self.streams:
            if user_id in self.streams[stream_id].viewers:
                self.streams[stream_id].viewers.remove(user_id)
            
            # Return True if no viewers left
            return len(self.streams[stream_id].viewers) == 0
        return False
    
    def create_stream(self, rtsp_url: str, title: str, user_id: str) -> StreamInfo:
        """Create new stream"""
        stream_id = self.generate_stream_id(rtsp_url)
        stream = StreamInfo(
            id=stream_id,
            url=rtsp_url,
            title=title or f"Stream {stream_id[:6]}",
            status='starting',
            created_at=datetime.now(),
            viewers=[user_id]
        )
        self.streams[stream_id] = stream
        return stream
    
    def get_stream(self, stream_id: str) -> Optional[StreamInfo]:
        """Get stream by ID"""
        return self.streams.get(stream_id)
    
    def get_user_streams(self, user_id: str) -> List[StreamInfo]:
        """Get all streams a user is watching"""
        user_streams = []
        for stream in self.streams.values():
            if user_id in stream.viewers:
                user_streams.append(stream)
        return user_streams
    
    def update_stream_status(self, stream_id: str, status: str):
        """Update stream status"""
        if stream_id in self.streams:
            self.streams[stream_id].status = status

# Global instance
stream_manager = StreamManager()
