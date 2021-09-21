module.exports = {
    env: {
        'jasmine': true,
        'commonjs': true
    },
    extends: [
        '@mozilla-protocol/eslint-config',
        'plugin:json/recommended'
    ],
    /**
     * A set of overrides for JavaScript assets where we support ES2015+.
     * */
    overrides: [
        {
            files: [
                'media/js/firefox/welcome/**/*.js',
                'media/js/firefox/whatsnew/**/*.js'
            ],
            env: {
                'es6': true
            },
            parserOptions: {
                ecmaVersion: 8
            }
        },
        {
            files: [
                'webpack.config.js',
                'webpack.static.config.js',
                'tests/unit/karma.conf.js'
            ],
            env: {
                'node': true,
                'es6': true
            },
            parserOptions: {
                ecmaVersion: 8
            },
            rules: {
                'strict': ['error', 'global'],
            }
        }
    ],
    globals: {
        'Mozilla': 'writable',
        'site': 'writable'
    }
};
