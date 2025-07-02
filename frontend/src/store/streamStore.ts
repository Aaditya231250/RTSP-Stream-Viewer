import { create } from 'zustand'

interface StreamData {
  id: string
  url: string
  title: string
  status: 'connecting' | 'active' | 'error' | 'paused'
  chunks: Uint8Array[]
  lastUpdate: number
  playing: boolean
}

interface StreamStore {
  streams: Map<string, StreamData>
  connectionStatus: 'connecting' | 'connected' | 'disconnected'
  
  // Actions
  addStream: (id: string, url: string, title: string) => void
  updateStreamStatus: (id: string, status: StreamData['status']) => void
  addStreamChunk: (id: string, chunk: Uint8Array) => void
  toggleStreamPlayback: (id: string) => void
  removeStream: (id: string) => void
  setConnectionStatus: (status: StreamStore['connectionStatus']) => void
  
  // Getters
  getStream: (id: string) => StreamData | undefined
  getActiveStreams: () => StreamData[]
}

export const useStreamStore = create<StreamStore>((set, get) => ({
  streams: new Map(),
  connectionStatus: 'disconnected',

  addStream: (id, url, title) => set((state) => {
    const newStreams = new Map(state.streams)
    newStreams.set(id, {
      id,
      url,
      title,
      status: 'connecting',
      chunks: [],
      lastUpdate: Date.now(),
      playing: false
    })
    return { streams: newStreams }
  }),

  updateStreamStatus: (id, status) => set((state) => {
    const newStreams = new Map(state.streams)
    const stream = newStreams.get(id)
    if (stream) {
      newStreams.set(id, { ...stream, status, lastUpdate: Date.now() })
    }
    return { streams: newStreams }
  }),

  addStreamChunk: (id, chunk) => set((state) => {
    const newStreams = new Map(state.streams)
    const stream = newStreams.get(id)
    if (stream) {
      // Keep only last 10 chunks to prevent memory issues
      const chunks = [...stream.chunks, chunk].slice(-10)
      newStreams.set(id, { 
        ...stream, 
        chunks, 
        lastUpdate: Date.now(),
        status: 'active'
      })
    }
    return { streams: newStreams }
  }),

  toggleStreamPlayback: (id) => set((state) => {
    const newStreams = new Map(state.streams)
    const stream = newStreams.get(id)
    if (stream) {
      newStreams.set(id, { ...stream, playing: !stream.playing })
    }
    return { streams: newStreams }
  }),

  removeStream: (id) => set((state) => {
    const newStreams = new Map(state.streams)
    newStreams.delete(id)
    return { streams: newStreams }
  }),

  setConnectionStatus: (connectionStatus) => set({ connectionStatus }),

  // Getters
  getStream: (id) => get().streams.get(id),
  getActiveStreams: () => Array.from(get().streams.values())
}))
