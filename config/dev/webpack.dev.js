const webpack = require('webpack')
const LiveReloadPlugin = require('webpack-livereload-plugin')

module.exports = {
    output : { publicPath: 'http://localhost:8000/static/' },
    devtool: 'source-map',
    plugins: [new LiveReloadPlugin({ appendScriptTag: true })]
}
