module.exports = {
    env: {
        'jquery': true,
        'jasmine': true
    },
    extends: [
        '@mozilla-protocol/eslint-config'
    ],
    plugins: [
        'no-jquery'
    ],
    rules: {
        'no-jquery/no-ajax': 'warn',
        'no-jquery/no-ajax-events': 'warn',
        'no-jquery/no-and-self': 'warn',
        'no-jquery/no-animate': 'warn',
        'no-jquery/no-attr': 'warn',
        'no-jquery/no-bind': 'warn',
        'no-jquery/no-box-model': 'warn',
        'no-jquery/no-browser': 'warn',
        'no-jquery/no-camel-case': 'warn',
        'no-jquery/no-class': 'warn',
        'no-jquery/no-class-state': 'warn',
        'no-jquery/no-clone': 'warn',
        'no-jquery/no-closest': 'warn',
        'no-jquery/no-constructor-attributes': 'warn',
        'no-jquery/no-contains': 'warn',
        'no-jquery/no-context-prop': 'warn',
        'no-jquery/no-css': 'warn',
        'no-jquery/no-data': 'warn',
        'no-jquery/no-deferred': 'warn',
        'no-jquery/no-delegate': 'warn',
        'no-jquery/no-each-collection': 'warn',
        'no-jquery/no-each-util': 'warn',
        'no-jquery/no-error': 'warn',
        'no-jquery/no-error-shorthand': 'warn',
        'no-jquery/no-event-shorthand': 'warn',
        'no-jquery/no-extend': 'warn',
        'no-jquery/no-fade': 'warn',
        'no-jquery/no-filter': 'warn',
        'no-jquery/no-find-collection': 'warn',
        'no-jquery/no-find-util': 'warn',
        'no-jquery/no-fx-interval': 'warn',
        'no-jquery/no-global-eval': 'warn',
        'no-jquery/no-grep': 'warn',
        'no-jquery/no-has': 'warn',
        'no-jquery/no-hold-ready': 'warn',
        'no-jquery/no-html': 'warn',
        'no-jquery/no-in-array': 'warn',
        'no-jquery/no-is': 'warn',
        'no-jquery/no-is-array': 'warn',
        'no-jquery/no-is-empty-object': 'warn',
        'no-jquery/no-is-function': 'warn',
        'no-jquery/no-is-numeric': 'warn',
        'no-jquery/no-is-plain-object': 'warn',
        'no-jquery/no-is-window': 'warn',
        'no-jquery/no-live': 'warn',
        'no-jquery/no-load': 'warn',
        'no-jquery/no-load-shorthand': 'warn',
        'no-jquery/no-map-collection': 'warn',
        'no-jquery/no-map-util': 'warn',
        'no-jquery/no-merge': 'warn',
        'no-jquery/no-node-name': 'warn',
        'no-jquery/no-noop': 'warn',
        'no-jquery/no-now': 'warn',
        'no-jquery/no-on-ready': 'warn',
        'no-jquery/no-param': 'warn',
        'no-jquery/no-parent': 'warn',
        'no-jquery/no-parents': 'warn',
        'no-jquery/no-parse-html': 'warn',
        'no-jquery/no-parse-html-literal': 'warn',
        'no-jquery/no-parse-json': 'warn',
        'no-jquery/no-parse-xml': 'warn',
        'no-jquery/no-prop': 'warn',
        'no-jquery/no-proxy': 'warn',
        'no-jquery/no-ready': 'warn',
        'no-jquery/no-ready-shorthand': 'warn',
        'no-jquery/no-selector-prop': 'warn',
        'no-jquery/no-serialize': 'warn',
        'no-jquery/no-size': 'warn',
        'no-jquery/no-sizzle': 'warn',
        'no-jquery/no-slide': 'warn',
        'no-jquery/no-sub': 'warn',
        'no-jquery/no-submit': 'warn',
        'no-jquery/no-support': 'warn',
        'no-jquery/no-text': 'warn',
        'no-jquery/no-trigger': 'warn',
        'no-jquery/no-trim': 'warn',
        'no-jquery/no-type': 'warn',
        'no-jquery/no-unique': 'warn',
        'no-jquery/no-val': 'warn',
        'no-jquery/no-visibility': 'warn',
        'no-jquery/no-when': 'warn',
        'no-jquery/no-wrap': 'warn',
        'no-jquery/variable-pattern': 'error'
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
