from django.core.management.base import BaseCommand
import asyncio
from streams.health_service import health_service

class Command(BaseCommand):
    help = 'Test system components'

    def handle(self, *args, **options):
        async def run_tests():
            self.stdout.write("🔍 Testing system components...")
            
            status = await health_service.get_system_status()
            
            # Redis test
            if status['redis']['status']:
                self.stdout.write(self.style.SUCCESS(f"✅ Redis: {status['redis']['message']}"))
            else:
                self.stdout.write(self.style.ERROR(f"❌ Redis: {status['redis']['message']}"))
            
            # FFmpeg test
            if status['ffmpeg']['status']:
                self.stdout.write(self.style.SUCCESS(f"✅ FFmpeg: {status['ffmpeg']['message']}"))
            else:
                self.stdout.write(self.style.ERROR(f"❌ FFmpeg: {status['ffmpeg']['message']}"))
            
            # Overall status
            if status['overall_health']:
                self.stdout.write(self.style.SUCCESS("🎉 All systems operational!"))
            else:
                self.stdout.write(self.style.ERROR("⚠️ Some systems need attention"))
        
        asyncio.run(run_tests())
