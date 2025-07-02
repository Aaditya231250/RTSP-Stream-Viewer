import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: process.env.NODE_ENV === 'production' ? '/your-repo-name/' : '/',
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
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['lucide-react', 'zustand'],
          video: ['hls.js']
        }
      }
    }
  }
})
