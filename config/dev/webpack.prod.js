const webpack = require('webpack')

const licenseCSS = `
    Arcon / http://www.zarthwork.de/typografie.html
    License: http://anna.elde.codes/static/fonts/arcon/license.txt

    Pacifico / https://www.fontsquirrel.com/fonts/pacifico
    License: http://anna.elde.codes/static/fonts/pacifico/license.txt

    Feather / https://github.com/colebemis/feather/
    License: https://anna.elde.codes/static/license/feather.txt
    `
const licenseJS = `
    barba.js / https://github.com/luruke/barba.js
    License: https://anna.elde.codes/static/license/barba.txt

    promise-polyfill / https://github.com/taylorhakes/promise-polyfill/
    License: https://anna.elde.codes/static/license/promise-polyfill.txt

    microevent.js / https://github.com/jeromeetienne/microevent.js/
    License: https://anna.elde.codes/static/license/microevent.txt

    js-cookie / https://github.com/js-cookie/js-cookie
    License: https://anna.elde.codes/static/license/js-cookie.txt

    ScrollReveal 3.3.6 / https://github.com/jlmakes/scrollreveal
    License: https://anna.elde.codes/static/license/scrollreveal.txt

    SuperAgent / https://github.com/visionmedia/superagent
    License: https://anna.elde.codes/static/license/superagent.txt

    component-emitter / https://github.com/component/emitter
    License: https://anna.elde.codes/static/license/component-emitter.txt
    `

module.exports = (dir = {}) => {
    return {
        devtool: 'nosources-source-map',
        output : { publicPath: 'https://anna.elde.codes/static/' },
        plugins: [
            new webpack.optimize.UglifyJsPlugin({
                include: dir.bundleJS,
                uglifyOptions: {
                    mangle: true,
                    compress: {
                        drop_debugger: true,
                        drop_console: true
                    },
                    output: {
                        comments: false,
                        beautify: false
                    }
                }
            }),
            new webpack.BannerPlugin({
                banner: licenseJS,
                entryOnly: true,
                include: dir.bundleJS
            }),
            new webpack.BannerPlugin({
                banner: licenseCSS,
                entryOnly: true,
                include: dir.bundleCSS
            })
        ]
    }
}
