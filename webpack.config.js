const path = require('path');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const MiniCssExtractPlugin  = require('mini-css-extract-plugin')

function resolveBundles(fileList){
  return fileList.map((f) => path.resolve(__dirname, "media", f));
}

module.exports = {
  mode: 'development',
  entry: {
    'firefox/mobile': resolveBundles([
      "js/base/mozilla-modal.js",
      "js/base/send-to-device.js",
      "js/base/mozilla-smoothscroll.js",
      "js/libs/jquery.waypoints.min.js",
      "js/libs/jquery.waypoints-sticky.min.js",
      "js/hubs/sub-nav.js",
      "js/firefox/mobile/features-scroller.js",
      "js/firefox/mobile/mobile.js",
      "css/base/send-to-device.less",
      "css/firefox/mobile.scss",
    ])
  },

  output: {
    'filename': 'js/[name].js',
    'path': path.resolve(__dirname, "static_final/webpacked"),
  },

  plugins: [
    new UglifyJSPlugin(),
    new MiniCssExtractPlugin({'filename': 'css/[name].css'}),
  ],

  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          "sass-loader"
        ]
      },
      {
        test: /\.less$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          {
            'loader': 'less-loader',
            'options': {
              javascriptEnabled: true,
            }
          },
        ]
      },
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader"
        ]
      },
    ]
  }
}
