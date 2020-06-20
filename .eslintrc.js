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
        'no-jquery/no-ajax': 1,
        'no-jquery/no-ajax-events': 1,
        'no-jquery/no-and-self': 1,
        'no-jquery/no-animate': 1,
        'no-jquery/no-attr': 1,
        'no-jquery/no-bind': 1,
        'no-jquery/no-box-model': 1,
        'no-jquery/no-browser': 1,
        'no-jquery/no-camel-case': 1,
        'no-jquery/no-class': 1,
        'no-jquery/no-class-state': 1,
        'no-jquery/no-clone': 1,
        'no-jquery/no-closest': 1,
        'no-jquery/no-constructor-attributes': 1,
        'no-jquery/no-contains': 1,
        'no-jquery/no-context-prop': 1,
        'no-jquery/no-css': 1,
        'no-jquery/no-data': 1,
        'no-jquery/no-deferred': 1,
        'no-jquery/no-delegate': 1,
        'no-jquery/no-each-collection': 1,
        'no-jquery/no-each-util': 1,
        'no-jquery/no-error': 1,
        'no-jquery/no-error-shorthand': 1,
        'no-jquery/no-event-shorthand': 1,
        'no-jquery/no-extend': 1,
        'no-jquery/no-fade': 1,
        'no-jquery/no-filter': 1,
        'no-jquery/no-find-collection': 1,
        'no-jquery/no-find-util': 1,
        'no-jquery/no-fx-interval': 1,
        'no-jquery/no-global-eval': 1,
        'no-jquery/no-grep': 1,
        'no-jquery/no-has': 1,
        'no-jquery/no-hold-ready': 1,
        'no-jquery/no-html': 1,
        'no-jquery/no-in-array': 1,
        'no-jquery/no-is': 1,
        'no-jquery/no-is-array': 1,
        'no-jquery/no-is-empty-object': 1,
        'no-jquery/no-is-function': 1,
        'no-jquery/no-is-numeric': 1,
        'no-jquery/no-is-plain-object': 1,
        'no-jquery/no-is-window': 1,
        'no-jquery/no-live': 1,
        'no-jquery/no-load': 1,
        'no-jquery/no-load-shorthand': 1,
        'no-jquery/no-map-collection': 1,
        'no-jquery/no-map-util': 1,
        'no-jquery/no-merge': 1,
        'no-jquery/no-node-name': 1,
        'no-jquery/no-noop': 1,
        'no-jquery/no-now': 1,
        'no-jquery/no-on-ready': 1,
        'no-jquery/no-param': 1,
        'no-jquery/no-parent': 1,
        'no-jquery/no-parents': 1,
        'no-jquery/no-parse-html': 1,
        'no-jquery/no-parse-html-literal': 1,
        'no-jquery/no-parse-json': 1,
        'no-jquery/no-parse-xml': 1,
        'no-jquery/no-prop': 1,
        'no-jquery/no-proxy': 1,
        'no-jquery/no-ready': 1,
        'no-jquery/no-ready-shorthand': 1,
        'no-jquery/no-selector-prop': 1,
        'no-jquery/no-serialize': 1,
        'no-jquery/no-size': 1,
        'no-jquery/no-sizzle': 1,
        'no-jquery/no-slide': 1,
        'no-jquery/no-sub': 1,
        'no-jquery/no-submit': 1,
        'no-jquery/no-support': 1,
        'no-jquery/no-text': 1,
        'no-jquery/no-trigger': 1,
        'no-jquery/no-trim': 1,
        'no-jquery/no-type': 1,
        'no-jquery/no-unique': 1,
        'no-jquery/no-val': 1,
        'no-jquery/no-visibility': 1,
        'no-jquery/no-when': 1,
        'no-jquery/no-wrap': 1,
        'no-jquery/variable-pattern': 2
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
