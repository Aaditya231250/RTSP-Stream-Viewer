import { useEffect, useRef, useState, useCallback } from 'react'

interface StreamMessage {
  type: string
  stream_id?: string
  chunk?: string
  timestamp?: string
  segment_name?: string
  chunk_size?: number
  url?: string
  title?: string
  message?: string
  user_id?: string
}

interface UseWebSocketReturn {
  isConnected: boolean
  sendMessage: (message: any) => void
  lastMessage: StreamMessage | null
  addStream: (url: string, title?: string) => void
  removeStream: (streamId: string) => void
}

export function useWebSocket(url: string): UseWebSocketReturn {
  const ws = useRef<WebSocket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<StreamMessage | null>(null)
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout>>()

  const connect = useCallback(() => {
    try {
      ws.current = new WebSocket(url)
      
      ws.current.onopen = () => {
        console.log('WebSocket connected')
        setIsConnected(true)
      }
      
      ws.current.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as StreamMessage
          setLastMessage(message)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }
      
      ws.current.onclose = () => {
        console.log('WebSocket disconnected')
        setIsConnected(false)
        
        // Auto-reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('Attempting to reconnect...')
          connect()
        }, 3000)
      }
      
      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error)
        setIsConnected(false)
      }
    } catch (error) {
      console.error('Failed to create WebSocket:', error)
    }
  }, [url])

  useEffect(() => {
    connect()
    
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      if (ws.current) {
        ws.current.close()
      }
    }
  }, [connect])

  const sendMessage = useCallback((message: any) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket not connected, cannot send message')
    }
  }, [])

  const addStream = useCallback((url: string, title?: string) => {
    sendMessage({
      action: 'add_stream',
      url,
      title: title || `Stream ${Date.now()}`
    })
  }, [sendMessage])

  const removeStream = useCallback((streamId: string) => {
    sendMessage({
      action: 'remove_stream',
      stream_id: streamId
    })
  }, [sendMessage])

  return {
    isConnected,
    sendMessage,
    lastMessage,
    addStream,
    removeStream
  }
}
