const path = require("path")
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require("webpack");



module.exports = {
    entry: "./flask_blog/static/js/index.js",
    mode: "production", //change to production
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, "flask_blog/static/"),
    },
    //devtool: 'inline-source-map', //remove on production
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                    },
                      {
                        loader: 'css-loader',
                        options: {importLoaders: 2, url: false},
                    },
                      {
                        loader: 'postcss-loader',
                        options: {
                          postcssOptions: {
                            config: path.resolve(__dirname, 'postcss.config.js'),
                          },
                        },
                    },
                ],
            }, 
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
          filename: "bundle.css"
        }),
        new webpack.ProvidePlugin({
          $: 'jquery',
          jQuery: 'jquery',
        }),
    ]
}