const path = require('path');

module.exports = {
    mode: 'development',
    entry: {
        'es6-test': [
            path.resolve(__dirname,'media/js/components/test.es6.js'),
            path.resolve(__dirname,'media/js/complied/test.es6.js'),
        ]
    },
    output: {
        'filename': '[name].js',
        'path': path.resolve(__dirname, "static_final/webpacked"),
    }
}