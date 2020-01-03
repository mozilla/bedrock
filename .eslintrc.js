module.exports = {
    env: {
        'jquery': true,
        'jasmine': true
    },
    extends: [
        '@mozilla-protocol/eslint-config'
    ],
    plugins: [
        'jquery'
    ],
    rules: {
        'jquery/no-ajax': 1,
        'jquery/no-ajax-events': 1,
        'jquery/no-animate': 1,
        'jquery/no-attr': 1,
        'jquery/no-bind': 1,
        'jquery/no-class': 1,
        'jquery/no-clone': 1,
        'jquery/no-closest': 1,
        'jquery/no-css': 1,
        'jquery/no-data': 1,
        'jquery/no-deferred': 1,
        'jquery/no-delegate': 1,
        'jquery/no-each': 1,
        'jquery/no-extend': 1,
        'jquery/no-fade': 1,
        'jquery/no-filter': 1,
        'jquery/no-find': 1,
        'jquery/no-global-eval': 1,
        'jquery/no-grep': 1,
        'jquery/no-has': 1,
        'jquery/no-hide': 1,
        'jquery/no-html': 1,
        'jquery/no-in-array': 1,
        'jquery/no-is-array': 1,
        'jquery/no-is-function': 1,
        'jquery/no-is': 1,
        'jquery/no-load': 1,
        'jquery/no-map': 1,
        'jquery/no-merge': 1,
        'jquery/no-param': 1,
        'jquery/no-parent': 1,
        'jquery/no-parents': 1,
        'jquery/no-parse-html': 1,
        'jquery/no-prop': 1,
        'jquery/no-proxy': 1,
        'jquery/no-ready': 1,
        'jquery/no-serialize': 1,
        'jquery/no-show': 1,
        'jquery/no-size': 1,
        'jquery/no-sizzle': 1,
        'jquery/no-slide': 1,
        'jquery/no-submit': 1,
        'jquery/no-text': 1,
        'jquery/no-toggle': 1,
        'jquery/no-trigger': 1,
        'jquery/no-trim': 1,
        'jquery/no-val': 1,
        'jquery/no-when': 1,
        'jquery/no-wrap': 1
    },
    /**
     * Provide a set of overrides for `gulpfile.js` in the root directory.
     * Ideally we want to extend @mozilla-protocol/eslint-config/index-node,
     * however ESLint does not currently allow extends inside glob overrides.
     * (see https://github.com/eslint/eslint/issues/8813)
     * */
    overrides: [
        {
            files: ['gulpfile.js', 'tests/unit/karma.conf.js'],
            env: {
                'commonjs': true,
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
        'Mozilla': true,
        'site': true
    }
};
