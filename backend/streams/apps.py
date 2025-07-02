from django.apps import AppConfig

class StreamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'streams'
    
    def ready(self):
        """Initialize when Django app starts"""
        print("✅ Streams app is ready!")
        print("🔴 Redis-based stream management initialized")
        
        self.cleanup_redis_on_startup()
    
    def cleanup_redis_on_startup(self):
        """Clean up old Redis data from previous runs"""
        try:
            import redis
            import os
            
            redis_url = os.environ.get('REDIS_URL', 'redis://redis:6379')
            r = redis.from_url(redis_url)
            
            # Clear old stream data
            r.delete("active_streams")
            r.delete("running_streams")
            
            # Clear any old stream keys
            for key in r.scan_iter("stream:*"):
                r.delete(key)
                
            print("🧹 Cleaned up old Redis data")
            r.close()
            
        except Exception as e:
            print(f"⚠️ Redis cleanup failed (normal if Redis not running): {e}")
