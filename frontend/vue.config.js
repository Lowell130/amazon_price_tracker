const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/': {
        target: 'http://127.0.0.1:8000', // URL del backend FastAPI
        changeOrigin: true,
        ws: false // Disabilita WebSocket
      }
    }
  }
})
