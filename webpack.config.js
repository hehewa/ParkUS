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
      }
    ]
  },
  resolve: {
    alias: {
      Bower: path.resolve(__dirname, 'static/bower_components'),
      // sans les lignes suivantes, les sous dépendances bower des libs npm
      // ne sont pas trouvées e.g. leaflet-react cherche leaflet :/
      leaflet: path.resolve(__dirname, 'static/bower_components/leaflet/leaflet')
    }
  }
};
