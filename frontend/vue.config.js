const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    historyApiFallback: true, // Assicura che le route del frontend siano gestite da Vue Router
  },
  css: {
    loaderOptions: {
      postcss: {
        postcssOptions: {
          plugins: [
            require("tailwindcss"),
            require("autoprefixer"),
          ],
        },
      },
    },
  },
})
