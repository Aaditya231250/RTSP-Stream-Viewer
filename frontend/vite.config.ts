import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './', // Change from '/RTSP-Stream-Viewer/' to './'
  server: {
    host: '0.0.0.0',
    port: 5173,
    watch: {
      usePolling: true,
    },
  },
  define: {
    'process.env': {}
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser',
  }
})
