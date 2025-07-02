from django.db import models
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class StreamInfo:
    """Stream data structure"""
    id: str
    url: str
    title: str
    status: str  # 'starting', 'active', 'error', 'stopped'
    created_at: datetime
    viewers: List[str]
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'viewer_count': len(self.viewers)
        }

@dataclass 
class UserConnection:
    """User connection data structure"""
    user_id: str
    channel_name: str
    connected_at: datetime
    watching_streams: List[str]

