from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import FileResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import asyncio
from .stream_manager import stream_manager
from .health_service import health_service
from .ffmpeg_processor import ffmpeg_processor

@api_view(['GET'])
def list_streams(request):
    """GET /api/streams/ - List all active streams"""
    streams = [stream.to_dict() for stream in stream_manager.streams.values()]
    return Response({'streams': streams})

@api_view(['GET'])
def stream_detail(request, stream_id):
    """GET /api/streams/{id}/ - Get specific stream details"""
    stream = stream_manager.get_stream(stream_id)
    if stream:
        return Response(stream.to_dict())
    return Response({'error': 'Stream not found'}, status=404)

@api_view(['GET'])
def health_check(request):
    """GET /api/health/ - Synchronous health check"""
    try:
        # Run async health check in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        status = loop.run_until_complete(health_service.get_system_status())
        loop.close()
        
        return JsonResponse(status)
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'overall_health': False
        }, status=500)

@api_view(['GET'])
async def system_stats(request):
    """GET /api/stats/ - System statistics"""
    try:
        stats = {
            'streams': {
                'total': len(stream_manager.streams),
                'by_status': {}
            },
            'processes': {
                'ffmpeg_active': len(ffmpeg_processor.active_processes)
            }
        }
        
        # Count streams by status
        for stream in stream_manager.streams.values():
            status = stream.status
            stats['streams']['by_status'][status] = stats['streams']['by_status'].get(status, 0) + 1
        
        return Response(stats)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@csrf_exempt
def serve_hls_playlist(request, stream_id):
    """Serve HLS playlist with comprehensive CORS headers"""
    try:
        print(f"🔍 Serving playlist for stream: {stream_id}")
        
        for process_info in ffmpeg_processor.active_processes.values():
            temp_dir = process_info.get('temp_dir', '')
            if stream_id in temp_dir or temp_dir.endswith(stream_id):
                playlist_path = os.path.join(temp_dir, 'playlist.m3u8')
                
                if os.path.exists(playlist_path):
                    with open(playlist_path, 'r') as f:
                        content = f.read()
                    
                    response = HttpResponse(content, content_type='application/vnd.apple.mpegurl')
                    response['Access-Control-Allow-Origin'] = '*'
                    response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
                    response['Access-Control-Allow-Headers'] = '*'
                    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                    response['Pragma'] = 'no-cache'
                    response['Expires'] = '0'
                    
                    print(f"✅ Served playlist for {stream_id}")
                    return response
        
        print(f"❌ Playlist not found for {stream_id}")
        raise Http404("Playlist not found")
    except Exception as e:
        print(f"❌ Error serving playlist: {e}")
        raise Http404(f"Error: {e}")

@csrf_exempt 
def serve_hls_segment(request, stream_id, segment_name):
    """Serve HLS segment with comprehensive CORS headers"""
    try:
        for process_info in ffmpeg_processor.active_processes.values():
            temp_dir = process_info.get('temp_dir', '')
            if stream_id in temp_dir or temp_dir.endswith(stream_id):
                segment_path = os.path.join(temp_dir, segment_name)
                
                if os.path.exists(segment_path):
                    with open(segment_path, 'rb') as f:
                        content = f.read()
                    
                    response = HttpResponse(content, content_type='video/mp2t')
                    response['Access-Control-Allow-Origin'] = '*'
                    response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
                    response['Access-Control-Allow-Headers'] = '*'
                    response['Cache-Control'] = 'no-cache'
                    
                    return response
        
        raise Http404("Segment not found")
    except Exception as e:
        print(f"❌ Error serving segment {segment_name}: {e}")
        raise Http404(f"Error: {e}")
