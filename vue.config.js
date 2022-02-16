module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    port: 8800
  },
  publicPath: process.env.NODE_ENV == 'production' ? '/lagrange/' : '/',
  outputDir: 'dist/lagrange'
}
