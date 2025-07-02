/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        sky: {
          bg: '#0b0d14',
          primary: '#00e6ff',
          secondary: '#3e7bff', 
          text: '#e8f6ff',
          subtle: '#9ca7b6',
          glass: 'rgba(255,255,255,0.06)',
          card: 'rgba(255,255,255,0.08)',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Sora', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        neon: '0 0 6px 0 rgba(0,230,255,0.5)',
        'neon-lg': '0 0 20px 0 rgba(0,230,255,0.3)',
        'neon-xl': '0 0 40px 0 rgba(0,230,255,0.2)',
        glass: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
      },
      backdropBlur: {
        glass: '12px',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-neon': 'pulseNeon 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        pulseNeon: {
          '0%, 100%': { boxShadow: '0 0 6px 0 rgba(0,230,255,0.5)' },
          '50%': { boxShadow: '0 0 20px 0 rgba(0,230,255,0.8)' },
        }
      }
    },
  },
  plugins: [],
}
