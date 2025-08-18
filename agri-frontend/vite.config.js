// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react'

// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [react()],
// })

// // vite.config.js
// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react'

// export default defineConfig({
//   plugins: [react()],
//   optimizeDeps: {
//     include: ['react', 'react-dom', 'react-router-dom'],
//   },
//     server: {
//     host: true // 👈 This makes Vite show the "Network" link
//   }
// })




// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',         // auto update SW
      injectRegister: 'auto',              // auto-inject registration code
      manifest: {
        name: 'AgriSathi AI',
        short_name: 'AgriSathi',
        start_url: '/',
        display: 'standalone',
        background_color: '#ffffff',
        theme_color: '#0b1726',
        icons: [
          { src: '/pwa-192x192.png', sizes: '192x192', type: 'image/png' },
          { src: '/pwa-512x512.png', sizes: '512x512', type: 'image/png' },
          { src: '/maskable-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' }
        ]
      },
      workbox: {
        // optional but recommended for SPA route handling from SW
        navigateFallback: '/index.html',
        globPatterns: ['**/*.{js,css,html,png,svg,ico,json}']
      }
      // For local testing of SW in dev, you can enable:
      // devOptions: { enabled: true }
    })
  ],
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom'],
  },
  server: {
    host: true
  }
})
