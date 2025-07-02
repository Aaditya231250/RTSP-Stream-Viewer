from django.urls import path
from . import views

urlpatterns = [
    path('streams/', views.list_streams, name='list_streams'),
    path('streams/<str:stream_id>/', views.stream_detail, name='stream_detail'),
    path('health/', views.health_check, name='health_check'),
    path('stats/', views.system_stats, name='system_stats'),
    path('hls/<str:stream_id>/playlist.m3u8', views.serve_hls_playlist, name='hls_playlist'),
    path('hls/<str:stream_id>/<str:segment_name>', views.serve_hls_segment, name='hls_segment'),
]
