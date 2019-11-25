const path = require('path');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
  mode: 'development',
  entry: {
    'es6-test': [
      path.resolve(__dirname,'media/js/components/test.es6.js'),
      path.resolve(__dirname,'media/js/components/test2.es6.js'),
      // path.resolve(__dirname,''),
    ],
    'firefox-mobile': [
      path.resolve(__dirname,"media/js/base/mozilla-modal.js"),
      path.resolve(__dirname,"media/js/base/send-to-device.js"),
      path.resolve(__dirname,"media/js/base/mozilla-smoothscroll.js"),
      path.resolve(__dirname,"media/js/libs/jquery.waypoints.min.js"),
      path.resolve(__dirname,"media/js/libs/jquery.waypoints-sticky.min.js"),
      path.resolve(__dirname,"media/js/hubs/sub-nav.js"),
      path.resolve(__dirname,"media/js/firefox/mobile/features-scroller.js"),
      path.resolve(__dirname,"media/js/firefox/mobile/mobile.js"),
    ]
  },

  output: {
    'filename': '[name].js',
    'path': path.resolve(__dirname, "static_final/webpacked"),
  },

  plugins: [
    new UglifyJSPlugin(),
  ],

  // module: {
  //   rules: [
  //     {
  //       test: /\.scss$/,
  //       use: [
  //         MiniCssExtractPlugin.loader,
  //         "css-loader",
  //         "sass-loader"
  //       ]
  //     },
  //     {
  //       test: /\.less$/,
  //       loader: 'less-loader',
  //     },
  //     {
  //       test: /\.css$/,
  //       use: [
  //         MiniCssExtractPlugin.loader,
  //         "css-loader"
  //       ]
  //     },
  //   ]
  // }
}