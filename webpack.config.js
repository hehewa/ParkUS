var path = require('path');

module.exports = {
  entry: './scripts/main.jsx',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static/scripts')
  },
  module: {
    rules: [
      {
        test: /\.jsx$/,
        use: [
          {loader: 'babel-loader'}
        ]
      },
      {
        test: /\.css$/,
        use: [
          {loader: 'style-loader'},
          {loader: 'css-loader'}
        ]
      },
      {
        test: /\.png$/,
        use: [
          {loader: 'file-loader?name=[name].[ext]&outputPath=../img/'}
        ]
      }
    ]
  },
  resolve: {
    alias: {
      Bower: path.resolve(__dirname, 'static/bower_components'),
      Css: path.resolve(__dirname, 'static/css')
    }
  }
};
