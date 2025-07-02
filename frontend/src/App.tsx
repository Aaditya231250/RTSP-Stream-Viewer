import { useState, useEffect } from 'react'
import { Plus, Monitor, Wifi, WifiOff, AlertCircle } from 'lucide-react'
import { useWebSocket } from './hooks/useWebSocket'
import { useStreamStore } from './store/streamStore'
import { StreamPlayer } from './components/StreamPlayer'

// Use environment variables with fallbacks
const WS_URL = import.meta.env.VITE_WS_URL || "wss://rtsp-backend-88322650503.us-central1.run.app/ws/stream/"
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "https://rtsp-backend-88322650503.us-central1.run.app"

function App() {
  const [rtspUrl, setRtspUrl] = useState('')
  const [notification, setNotification] = useState<{type: 'success' | 'error', message: string} | null>(null)
  
  const { isConnected, lastMessage, addStream, removeStream } = useWebSocket(WS_URL)
  const { 
    addStream: addStreamToStore, 
    updateStreamStatus, 
    addStreamChunk, 
    setConnectionStatus,
    getActiveStreams,
    removeStream: removeStreamFromStore
  } = useStreamStore()

  // Update connection status
  useEffect(() => {
    setConnectionStatus(isConnected ? 'connected' : 'disconnected')
  }, [isConnected, setConnectionStatus])

  // Handle WebSocket messages
  useEffect(() => {
    if (!lastMessage) return

    switch (lastMessage.type) {
      case 'connection_established':
        console.log('WebSocket connected')
        setNotification({ type: 'success', message: 'Connected to stream server' })
        break
        
      case 'stream_added':
        if (lastMessage.stream_id && lastMessage.url && lastMessage.title) {
          addStreamToStore(lastMessage.stream_id, lastMessage.url, lastMessage.title)
          setNotification({ type: 'success', message: `Stream "${lastMessage.title}" added` })
          console.log(`Stream added: ${lastMessage.stream_id}`)
        }
        break
        
      case 'stream_data':
        if (lastMessage.stream_id && lastMessage.chunk) {
          try {
            // Decode base64 chunk to Uint8Array
            const binaryString = atob(lastMessage.chunk)
            const chunk = new Uint8Array(binaryString.length)
            for (let i = 0; i < binaryString.length; i++) {
              chunk[i] = binaryString.charCodeAt(i)
            }
            addStreamChunk(lastMessage.stream_id, chunk)
          } catch (error) {
            console.error('Failed to decode stream chunk:', error)
          }
        }
        break
        
      case 'stream_status':
        if (lastMessage.stream_id) {
          const status = lastMessage.message?.includes('error') ? 'error' : 'active'
          updateStreamStatus(lastMessage.stream_id, status)
        }
        break
        
      case 'stream_removed':
        if (lastMessage.stream_id) {
          removeStreamFromStore(lastMessage.stream_id)
          setNotification({ type: 'success', message: 'Stream removed successfully' })
          console.log(`Stream removed: ${lastMessage.stream_id}`)
        }
        break
        
      case 'error':
        console.error('WebSocket error:', lastMessage.message)
        setNotification({ type: 'error', message: lastMessage.message || 'Unknown error' })
        break
        
      default:
        console.log('Unhandled message type:', lastMessage.type)
    }
  }, [lastMessage, addStreamToStore, updateStreamStatus, addStreamChunk, removeStreamFromStore])

  // Auto-hide notifications
  useEffect(() => {
    if (notification) {
      const timer = setTimeout(() => setNotification(null), 5000)
      return () => clearTimeout(timer)
    }
  }, [notification])

  const handleAddStream = () => {
    if (rtspUrl.trim() && rtspUrl.startsWith('rtsp://')) {
      const title = `Camera ${getActiveStreams().length + 1}`
      addStream(rtspUrl, title)
      setRtspUrl('')
    } else {
      setNotification({ type: 'error', message: 'Please enter a valid RTSP URL starting with rtsp://' })
    }
  }

  const handleRemoveStream = (streamId: string) => {
    removeStream(streamId)
  }

  const activeStreams = getActiveStreams()

  return (
    <div className="min-h-screen bg-sky-bg">
      {/* Animated background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-sky-primary/5 rounded-full blur-3xl animate-pulse-neon"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-sky-secondary/5 rounded-full blur-3xl animate-pulse-neon" style={{animationDelay: '1s'}}></div>
      </div>

      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 right-4 z-50 glass-card p-4 rounded-lg shadow-neon-lg animate-slide-up ${
          notification.type === 'error' ? 'border-red-500/50' : 'border-green-500/50'
        }`}>
          <div className="flex items-center space-x-2">
            <AlertCircle className={`h-4 w-4 ${notification.type === 'error' ? 'text-red-400' : 'text-green-400'}`} />
            <span className="text-sky-text text-sm">{notification.message}</span>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="relative border-b border-white/10 backdrop-blur-md bg-white/5">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Monitor className="h-8 w-8 text-sky-primary animate-pulse-neon" />
              <h1 className="text-2xl font-heading font-bold bg-gradient-to-r from-sky-primary to-sky-secondary bg-clip-text text-transparent">
                RTSP Viewer
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm text-sky-subtle">
                {isConnected ? (
                  <>
                    <Wifi className="h-4 w-4 text-green-400" />
                    <span>Connected</span>
                  </>
                ) : (
                  <>
                    <WifiOff className="h-4 w-4 text-red-400" />
                    <span>Disconnected</span>
                  </>
                )}
              </div>
              <div className="text-sm text-sky-subtle">
                {activeStreams.length} active streams
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="relative max-w-7xl mx-auto px-6 py-8">
        {/* Add Stream Form */}
        <div className="glass-card rounded-xl p-6 mb-8 animate-fade-in">
          <h2 className="text-xl font-semibold mb-4 text-sky-text">Add RTSP Stream</h2>
          <div className="flex space-x-4">
            <input
              type="text"
              value={rtspUrl}
              onChange={(e) => setRtspUrl(e.target.value)}
              placeholder="rtsp://username:password@ip:port/path"
              className="flex-1 bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-sky-text placeholder-sky-subtle focus:outline-none focus:ring-2 focus:ring-sky-primary focus:border-transparent transition-all"
              onKeyPress={(e) => e.key === 'Enter' && handleAddStream()}
            />
            <button
              onClick={handleAddStream}
              disabled={!isConnected}
              className="glass-button px-6 py-2 rounded-lg flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Plus className="h-4 w-4" />
              <span>Add Stream</span>
            </button>
          </div>
        </div>

        {/* Stream Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {activeStreams.length === 0 ? (
            <div className="col-span-full text-center py-12 animate-fade-in">
              <Monitor className="h-16 w-16 text-sky-subtle mx-auto mb-4 animate-pulse" />
              <p className="text-sky-subtle text-lg">No streams added yet</p>
              <p className="text-sky-subtle/60">Add your first RTSP stream to get started</p>
            </div>
          ) : (
            activeStreams.map((stream) => (
              <StreamPlayer 
                key={stream.id} 
                streamId={stream.id} 
                onRemove={handleRemoveStream}
              />
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default App
