const path = require('path')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const merge = require('webpack-merge')

const ruleConfig = require('./config/dev/webpack.rules.js')
const devConfig = require('./config/dev/webpack.dev.js')
const prodConfig = require('./config/dev/webpack.prod.js')

const dir = {
    /** Filepaths */
    entryJS: './src/js/',
    bundleJS: './site/static/js/',
    entryCSS: './src/scss/',
    bundleCSS: './site/static/css/'
}

const commonConfig = {
    entry: [dir.entryJS + 'entry.js', dir.entryCSS + 'style.scss'],
    output: { filename: dir.bundleJS + 'bundle.js' },
    plugins: [
        new ExtractTextPlugin({
            filename: dir.bundleCSS + 'style.css',
            allChunks: true
        })
    ],
    node: {
        console: false,
        Buffer: false,
        path: false,
        url: false,
        global: false,
        fs: 'empty',
        net: 'empty',
        tls: 'empty'
    }
}

module.exports = (env = {}) => {
    var config = merge.smart(commonConfig, ruleConfig(env))

    if (env.prod === true) config = merge.smart(config, prodConfig(dir))
    else if (env.dev === true) config = merge.smart(config, devConfig)

    return config
}
