import { useEffect, useRef, useState } from 'react'
import { Play, Pause, AlertCircle, Loader2, X } from 'lucide-react'
import { useStreamStore } from '../store/streamStore'

interface StreamPlayerProps {
  streamId: string
  onRemove: (streamId: string) => void
}

// Extend HLS interface to include missing methods
interface ExtendedHls {
  isSupported(): boolean
  loadSource(url: string): void
  attachMedia(video: HTMLVideoElement): void
  on(event: string, callback: Function): void
  destroy(): void
  startLoad(): void
  recoverMediaError(): void
}

export function StreamPlayer({ streamId, onRemove }: StreamPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const hlsRef = useRef<ExtendedHls | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [hlsUrl, setHlsUrl] = useState<string | null>(null)
  const [hlsReady, setHlsReady] = useState(false)
  
  const stream = useStreamStore((state) => state.getStream(streamId))

  // Update the HLS URL to use the backend environment variable
  useEffect(() => {
    if (stream && stream.chunks.length > 0) {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || "https://rtsp-backend-88322650503.us-central1.run.app"
      const url = `${backendUrl}/api/hls/${streamId}/playlist.m3u8`
      setHlsUrl(url)
      console.log(`🎬 HLS URL: ${url}`)
    }
  }, [stream?.chunks.length, streamId])

  // Initialize HLS.js with optimized live streaming config
  useEffect(() => {
    if (hlsUrl && videoRef.current) {
      import('hls.js').then((HlsModule) => {
        const Hls = HlsModule.default as any // Type assertion to bypass TypeScript issues
        
        if (Hls.isSupported()) {
          console.log(`Initializing HLS for stream: ${streamId}`)
          
          const hls = new Hls({
            debug: false,
            enableWorker: false,
            
            // Optimized live streaming settings
            lowLatencyMode: true,
            backBufferLength: 5,
            maxBufferLength: 15,
            maxMaxBufferLength: 30,
            maxBufferSize: 60 * 1000 * 1000,
            maxBufferHole: 0.5,
            
            // Live sync optimization
            liveSyncDurationCount: 2,
            liveMaxLatencyDurationCount: 4,
            liveDurationInfinity: true,
            
            // Fragment loading optimization
            fragLoadingTimeOut: 10000,
            fragLoadingMaxRetry: 3,
            fragLoadingRetryDelay: 1000,
            
            // Manifest loading optimization
            manifestLoadingTimeOut: 5000,
            manifestLoadingMaxRetry: 3,
            manifestLoadingRetryDelay: 1000,
            
            // Level loading optimization
            levelLoadingTimeOut: 5000,
            levelLoadingMaxRetry: 2,
            levelLoadingRetryDelay: 1000,
            
            // Stall recovery settings
            nudgeOffset: 0.1,
            nudgeMaxRetry: 3,
            maxSeekHole: 2,
            startFragPrefetch: true,
          }) as ExtendedHls
          
          hlsRef.current = hls
          
          hls.on('hlsManifestParsed', () => {
            console.log(`HLS initialized for stream: ${streamId}`)
            setHlsReady(true)
            setError(null)
          })
          
          hls.on('hlsError', (_event: any, data: any) => {
            if (data.fatal) {
              console.error(`Fatal HLS error: ${data.type} - ${data.details}`)
              setError(`Playback error: ${data.details}`)
              
              // Type-safe error handling
              try {
                switch (data.type) {
                  case 'networkError':
                    (hls as any).startLoad()
                    break
                  case 'mediaError':
                    (hls as any).recoverMediaError()
                    break
                  default:
                    hls.destroy()
                    break
                }
              } catch (recoveryError) {
                console.error('Error recovery failed:', recoveryError)
                hls.destroy()
              }
            }
          })
          
          hls.loadSource(hlsUrl)
          if (videoRef.current) {
            hls.attachMedia(videoRef.current)
          }
          
        } else if (videoRef.current?.canPlayType('application/vnd.apple.mpegurl')) {
          console.log(`Using native HLS for stream: ${streamId}`)
          videoRef.current.src = hlsUrl
          setHlsReady(true)
        } else {
          setError('HLS not supported in this browser')
        }
      }).catch(() => {
        console.error('HLS.js loading failed')
        setError('Video playback engine missing')
      })
    }

    return () => {
      if (hlsRef.current) {
        hlsRef.current.destroy()
        hlsRef.current = null
      }
    }
  }, [hlsUrl, streamId])

  const handlePlayPause = () => {
    if (!videoRef.current || !hlsReady) return
    
    if (isPlaying) {
      videoRef.current.pause()
    } else {
      videoRef.current.play().catch(() => {
        console.error('Playback failed')
        setError('Failed to start playback')
      })
    }
  }

  const handleRemove = () => {
    if (hlsRef.current) {
      hlsRef.current.destroy()
      hlsRef.current = null
    }
    onRemove(streamId)
  }

  if (!stream) {
    return (
      <div className="aspect-video bg-black/50 rounded-lg flex items-center justify-center">
        <p className="text-sky-subtle">Stream not found</p>
      </div>
    )
  }

  const getStatusIcon = () => {
    switch (stream.status) {
      case 'connecting':
        return <Loader2 className="h-8 w-8 text-sky-primary animate-spin" />
      case 'error':
        return <AlertCircle className="h-8 w-8 text-red-400" />
      case 'active':
        return isPlaying ? 
          <Pause className="h-8 w-8 text-sky-primary" /> : 
          <Play className="h-8 w-8 text-sky-primary" />
      default:
        return <Play className="h-8 w-8 text-sky-subtle" />
    }
  }

  const getStatusText = () => {
    if (error) return error
    if (hlsReady) return 'Live stream'
    return stream.status === 'connecting' ? 'Connecting to stream...' : 'Loading...'
  }

  return (
    <div className="glass-card rounded-xl p-4 hover:shadow-neon-lg transition-all duration-300">
      <div className="aspect-video bg-black/50 rounded-lg mb-3 relative overflow-hidden neon-border">
        <video
          ref={videoRef}
          className="w-full h-full object-cover"
          muted
          playsInline
          controls={false}
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
        />
        
        {/* Remove Button */}
        <button
          onClick={handleRemove}
          className="absolute top-2 left-2 bg-red-600/80 hover:bg-red-600 backdrop-blur-sm rounded-full p-2 transition-all duration-200 z-10"
          title="Remove Stream"
        >
          <X className="h-4 w-4 text-white" />
        </button>
        
        {/* Status overlay */}
        <div className="absolute inset-0 flex items-center justify-center">
          {error ? (
            <div className="text-center">
              <AlertCircle className="h-8 w-8 text-red-400 mx-auto mb-2" />
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          ) : !hlsReady ? (
            <div className="text-center">
              <Loader2 className="h-8 w-8 text-sky-primary animate-spin mx-auto mb-2" />
              <p className="text-sky-subtle text-sm">Loading HLS...</p>
            </div>
          ) : (
            <button
              onClick={handlePlayPause}
              className="bg-black/50 hover:bg-black/70 backdrop-blur-sm rounded-full p-4 transition-all duration-200 opacity-0 hover:opacity-100"
            >
              {getStatusIcon()}
            </button>
          )}
        </div>
        
        {/* Status indicator */}
        <div className="absolute top-2 right-2 bg-black/70 backdrop-blur-sm rounded px-2 py-1 text-xs text-sky-text">
          {error ? 'Error' : hlsReady ? (isPlaying ? 'Playing' : 'Ready') : 'Loading'}
        </div>
        
        {/* Error display */}
        {error && (
          <div className="absolute bottom-2 left-2 right-2 bg-red-900/80 backdrop-blur-sm rounded px-2 py-1 text-xs text-red-200">
            {error}
          </div>
        )}
      </div>
      
      <div className="flex items-center justify-between">
        <div>
          <span className="text-sky-text font-medium">{stream.title}</span>
          <p className="text-sky-subtle text-sm">{getStatusText()}</p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={handlePlayPause}
            disabled={!hlsReady || !!error}
            className="bg-sky-primary/20 hover:bg-sky-primary/30 text-sky-primary px-3 py-1 rounded text-sm transition-all duration-200 flex items-center space-x-1 disabled:opacity-50"
          >
            {isPlaying ? <Pause className="h-3 w-3" /> : <Play className="h-3 w-3" />}
            <span>{isPlaying ? 'Pause' : 'Play'}</span>
          </button>
          <button
            onClick={handleRemove}
            className="bg-red-500/20 hover:bg-red-500/30 text-red-400 px-3 py-1 rounded text-sm transition-all duration-200 flex items-center space-x-1"
          >
            <X className="h-3 w-3" />
            <span>Remove</span>
          </button>
        </div>
      </div>
    </div>
  )
}
