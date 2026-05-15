import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3300,
    proxy: {
      // ต้องใส่ intent ก่อน เพราะ /investment-ai-agent เป็น prefix ของมัน
      '^/investment-ai-agent-intent': {
        target: 'http://localhost:8802',
        changeOrigin: true,
      },
      '^/investment-ai-agent(?!-intent)': {
        target: 'http://localhost:8801',
        changeOrigin: true,
      },
    },
  },
})
