module.exports = {
    env: {
        'jasmine': true,
        'commonjs': true,
    },
    extends: [
        '@mozilla-protocol/eslint-config',
        'plugin:json/recommended'
    ],
    /**
     * Provide a set of overrides for `webpack-config.js` in the root directory.
     * Ideally we want to extend @mozilla-protocol/eslint-config/index-node,
     * however ESLint does not currently allow extends inside glob overrides.
     * (see https://github.com/eslint/eslint/issues/8813)
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
