module.exports = {
    env: {
        'jasmine': true,
        'commonjs': true
    },
    extends: [
        'plugin:json/recommended'
    ],
    /**
     * A set of overrides for JavaScript assets where we support ES2015+.
     * */
    overrides: [
        {
            // JS files transpiled by Babel
            files: [
                'media/js/**/*.es6.js',
            ],
            env: {
                'es2017': true
            }
        },
        {
            // JS files served only to Firefox browsers.
            files: [
                'media/js/firefox/welcome/**/*.js',
                'media/js/firefox/whatsnew/**/*.js',
                'media/js/firefox/firstrun/**/*.js',
            ],
            env: {
                'es2017': true
            }
        },
        {
            // JS build files for local dev.
            files: [
                'webpack.config.js',
                'webpack.static.config.js',
                'tests/unit/karma.conf.js'
            ],
            env: {
                'node': true,
                'es2017': true
            },
            rules: {
                'strict': ['error', 'global'],
            }
        }
    ],
    globals: {
        'Mozilla': 'writable',
        'Mzp': 'writable',
        'site': 'writable'
    }
};
