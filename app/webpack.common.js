const webpack = require('webpack');
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyPlugin = require('copy-webpack-plugin');


const config = {
    optimization: {
        usedExports: true,  // this is automatically set to true when in production mode
    },
    entry: {
        'main': __dirname + '/public/src/js/index.js',
    },
    output: {
        path: __dirname + '/public/dist/assets/',
        filename: '[name].js',
    },
    module: {
        rules: [
                {
					// Sass/Scss loader
                    test: /\.(sa|sc|c)ss$/,
                    use: [
						{
                            loader: MiniCssExtractPlugin.loader,
                        },
                        //{
						//	// Inject css to page
                        //    loader: 'style-loader',
                        //},
                        {
							// Translate css into CommonJS modules
                            loader: 'css-loader',
                        },
                        {
							// Run postcss actions
                            loader: 'postcss-loader',
							options: {
								postcssOptions: {
									// post css plugins, can be exported to postcss.config.js
									plugins: function () {
										return [
											require('autoprefixer')
                            		  	];
                            		}
								},
							},
                        },
                        {
							// Compile sass to css
                            loader: 'sass-loader',
                        },
                    ]
                },
				{
					test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
      			  	use: [
						{
							loader: 'file-loader',
      			  	  	  	options: {
								name: '[name].[ext]',
      			  	  	  	  	outputPath: 'fonts/'
      			  	  	  	}
      			  	  	}
      			  	]
      			},
				//{
				//	// Css loader
                //    test: /\.css$/,
				//	use: ['style-loader', 'css-loader'],
				//},
			],
			},
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].css',
            chunkFilename: '[id].css',
        }),
		//new CopyPlugin({
		//	patterns: [
		//		// Needed because tinymce is a tiny bitch and doesn't want to work without the skins being in the public assets
		//		{ from: './node_modules/tinymce/skins', to: './skins' },
		//	],
		//}),
    ],
};
module.exports = config;
