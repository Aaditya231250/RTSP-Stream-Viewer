import redis.asyncio as redis
import os
#import json
from .models import StreamInfo

class RedisService:
    """Handles all Redis operations"""
    
    def __init__(self):
        self.redis_url = os.environ.get('REDIS_URL', 'redis://redis:6379')
    
    async def get_redis(self):
        return redis.from_url(self.redis_url)
    
    async def add_user_to_group(self, user_id: str, channel_name: str):
        r = await self.get_redis()
        await r.sadd(f"user_group:{user_id}", channel_name)
        await r.close()
    
    async def add_user_to_stream_group(self, stream_id: str, channel_name: str):
        r = await self.get_redis()
        await r.sadd(f"stream_group:{stream_id}", channel_name)
        await r.close()
    
    async def remove_user_from_stream_group(self, stream_id: str, channel_name: str):
        r = await self.get_redis()
        await r.srem(f"stream_group:{stream_id}", channel_name)
        await r.close()
    
    async def store_stream_info(self, stream_id: str, stream_info: StreamInfo):
        r = await self.get_redis()
        await r.hset(f"stream:{stream_id}", mapping=stream_info.to_dict())
        await r.close()
    
    async def get_stream_info(self, stream_id: str):
        r = await self.get_redis()
        data = await r.hgetall(f"stream:{stream_id}")
        await r.close()
        return data
    
    async def remove_user_from_group(self, user_id: str, channel_name: str):
        r = await self.get_redis()
        await r.srem(f"user_group:{user_id}", channel_name)
        await r.close()

redis_service = RedisService()
