import asyncio
import redis.asyncio as redis
import os
from .stream_manager import stream_manager
from .ffmpeg_processor import ffmpeg_processor

class HealthService:
    """Service health monitoring and diagnostics"""
    
    async def check_redis_connection(self):
        """Test Redis connectivity"""
        try:
            redis_url = os.environ.get('REDIS_URL', 'redis://redis:6379')
            r = redis.from_url(redis_url)
            await r.ping()
            await r.close()
            return True, "Redis connection OK"
        except Exception as e:
            return False, f"Redis connection failed: {e}"
    
    async def check_ffmpeg_availability(self):
        """Test FFmpeg installation"""
        try:
            process = await asyncio.create_subprocess_exec(
                'ffmpeg', '-version',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode == 0:
                return True, "FFmpeg available"
            else:
                return False, f"FFmpeg check failed: {stderr.decode()}"
        except Exception as e:
            return False, f"FFmpeg not found: {e}"
    
    async def get_system_status(self):
        """Get comprehensive system status"""
        redis_ok, redis_msg = await self.check_redis_connection()
        ffmpeg_ok, ffmpeg_msg = await self.check_ffmpeg_availability()
        
        active_streams = len(stream_manager.streams)
        active_processes = len(ffmpeg_processor.active_processes)
        total_viewers = sum(len(s.viewers) for s in stream_manager.streams.values())
        
        return {
            'redis': {'status': redis_ok, 'message': redis_msg},
            'ffmpeg': {'status': ffmpeg_ok, 'message': ffmpeg_msg},
            'streams': {
                'active_streams': active_streams,
                'active_processes': active_processes,
                'total_viewers': total_viewers
            },
            'overall_health': redis_ok and ffmpeg_ok
        }

health_service = HealthService()


