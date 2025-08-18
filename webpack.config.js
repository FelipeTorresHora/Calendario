const path = require('path');

module.exports = {
  entry: {
    main: './static/js/main.js',
    calendar: './static/js/components/Calendar/index.js',
    metrics: './static/js/components/Metrics/index.js',
  },
  output: {
    path: path.resolve(__dirname, 'static/dist'),
    filename: '[name].bundle.js',
    publicPath: '/static/dist/',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
          },
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  devtool: 'source-map',
};