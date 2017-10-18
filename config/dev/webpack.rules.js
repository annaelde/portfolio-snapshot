const ExtractTextPlugin = require('extract-text-webpack-plugin')
const webpackIf = require('webpack-if')

module.exports = (env = {}) => {
    const dev = webpackIf.ifElse(env.dev === true)
    const prod = webpackIf.ifElse(env.prod === true)
    return webpackIf({
        module: {
            rules: [
                /**
                 * .js
                 */
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: [
                        {
                            loader: 'babel-loader',
                            options: {
                                presets: [
                                    [
                                        'env',
                                        {
                                            targets: {
                                                browsers: [
                                                    'last 2 versions',
                                                    'ie >= 10'
                                                ]
                                            }
                                        }
                                    ]
                                ]
                            }
                        },
                        {
                            loader: 'ifdef-loader',
                            options: {
                                PRODUCTION: prod(true, false)
                            }
                        }
                    ]
                },
                /**
                 * .css
                 */
                {
                    test: /\.css$/,
                    use: ExtractTextPlugin.extract({
                        use: [
                            { loader: 'css-loader', options: { url: false } },
                            {
                                loader: 'postcss-loader',
                                options: {
                                    plugins: prod(
                                        (
                                            loader // Production Plugins
                                        ) => [
                                            require('autoprefixer')(),
                                            require('postcss-base64')({
                                                pattern: /<svg.*<\/svg>/i,
                                                prepend:
                                                    'data:image/svg+xml;base64,'
                                            }),
                                            require('postcss-clean')()
                                        ],
                                        (
                                            loader // Development Plugins
                                        ) => [
                                            require('autoprefixer')(),
                                            require('postcss-base64')({
                                                pattern: /<svg.*<\/svg>/i,
                                                prepend:
                                                    'data:image/svg+xml;base64,'
                                            })
                                        ]
                                    )
                                }
                            }
                        ]
                    })
                },
                /**
                 * .scss
                 */
                {
                    test: /\.(scss)$/,
                    use: ExtractTextPlugin.extract({
                        use: [
                            { loader: 'css-loader', options: { url: false } },
                            {
                                loader: 'postcss-loader',
                                options: {
                                    plugins: prod(
                                        (
                                            loader // Production Plugins
                                        ) => [
                                            require('autoprefixer')(),
                                            require('postcss-base64')({
                                                pattern: /<svg.*<\/svg>/i,
                                                prepend:
                                                    'data:image/svg+xml;base64,'
                                            }),
                                            require('postcss-clean')()
                                        ],
                                        (
                                            loader // Development Plugins
                                        ) => [
                                            require('autoprefixer')(),
                                            require('postcss-base64')({
                                                pattern: /<svg.*<\/svg>/i,
                                                prepend:
                                                    'data:image/svg+xml;base64,'
                                            })
                                        ]
                                    )
                                }
                            },
                            { loader: 'sass-loader', options: { url: false } }
                        ]
                    })
                },
                /**
                 * .json
                 */
                {
                    test: /\.json$/,
                    exclude: /node_modules/,
                    use: [{ loader: 'json-loader' }]
                }
            ]
        }
    })
}
