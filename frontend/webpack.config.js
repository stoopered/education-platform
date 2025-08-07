const path = require('path');
const webpack = require('webpack');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    publicPath: '/' ,
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
          },
        },
      },
    ],
  },
  devServer: {
    static: {
      directory: path.join(__dirname, 'public'),
    },
    historyApiFallback: true,
    port: 3000,
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },

  /*
   * Inject selected environment variables into the bundle at build time.
   * Without this plugin, variables like process.env.REACT_APP_API_URL will
   * be undefined in the browser.  Compose or your shell can set these
   * variables when building the image or running `npm start` locally.
   */
  plugins: [
    new webpack.DefinePlugin({
      'process.env.REACT_APP_API_URL': JSON.stringify(process.env.REACT_APP_API_URL),
      'process.env.REACT_APP_REGION': JSON.stringify(process.env.REACT_APP_REGION),
      'process.env.REACT_APP_USER_POOL_ID': JSON.stringify(process.env.REACT_APP_USER_POOL_ID),
      'process.env.REACT_APP_USER_POOL_CLIENT': JSON.stringify(process.env.REACT_APP_USER_POOL_CLIENT),
      'process.env.REACT_APP_SKIP_LOGIN': JSON.stringify(process.env.REACT_APP_SKIP_LOGIN),
    }),
  ],
};