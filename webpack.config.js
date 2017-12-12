const path = require('path');
const webpack = require('webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const publicPath = path.resolve(__dirname, 'mycat-discriminator/public')

const debug = !!process.env.DEBUG;
const proxyUrl = process.env.PROXY_URL || 'http://localhost:8001';
const port = process.env.PORT || 8002;

module.exports = {
  entry: {
    index: path.resolve(__dirname, 'mycat-discriminator/assets/js/index.js')
  },
  output: {
    path: publicPath,
    filename: 'js/[hash].[name].min.js'
  },
  plugins: [
    new CleanWebpackPlugin(debug ? [] : [publicPath]),
    new HtmlWebpackPlugin({
      template: path.resolve(__dirname, 'mycat-discriminator/assets/index.html')
    }),
    new webpack.optimize.UglifyJsPlugin(),
  ],
  module: {
    loaders: [
      {
        test: /\.js/,
        loader: 'babel-loader',
        exclude: /node_modules(?!\/webpack-dev-server)/,
        query: {
          presets: [
            'es2015'
          ],
          plugins: [
            'transform-runtime',
          ],
        },
      },
    ],
  },
  devServer: {
    host: '0.0.0.0',
    port: port,
    proxy: {
      '/api': {
        target: proxyUrl,
      },
    },
  },
}
