module.exports = {
    env: {
        'browser': true,
        'commonjs': true,
        'jasmine': true
    },
    extends: [
        'eslint:recommended',
        'plugin:json/recommended'
    ],
    rules: {
        // Require strict mode directive in top level functions
        // https://eslint.org/docs/rules/strict
        'strict': ['error', 'function'],

        // This option sets a specific tab width for your code
        // https://eslint.org/docs/rules/indent
        'indent': ['error', 4],

        // Disallow mixed 'LF' and 'CRLF' as linebreaks
        // https://eslint.org/docs/rules/linebreak-style
        'linebreak-style': ['error', 'unix'],

        // Specify whether double or single quotes should be used
        'quotes': ['error', 'single'],

        // Require or disallow use of semicolons instead of ASI
        'semi': ['error', 'always'],

        // Enforce location of semicolons
        // https://eslint.org/docs/rules/semi-style
        'semi-style': ['error', 'last'],

        // Require camel case names
        // https://eslint.org/docs/rules/camelcase
        'camelcase': ['error', { 'properties': 'always' }],

        // Use type-safe equality operators
        // https://eslint.org/docs/rules/eqeqeq
        'eqeqeq': ['error', 'always'],

        // Treat var statements as if they were block scoped
        // https://eslint.org/docs/rules/block-scoped-var
        'block-scoped-var': 'error',

        // Require newlines around variable declarations
        // https://eslint.org/docs/rules/one-var-declaration-per-line
        'one-var-declaration-per-line': ['error', 'always'],

        // Require constructor names to begin with a capital letter
        // https://eslint.org/docs/rules/new-cap
        'new-cap': 'error',

        // Disallow Use of alert, confirm, prompt
        // https://eslint.org/docs/rules/no-alert
        'no-alert': 'error',

        // Disallow eval()
        // https://eslint.org/docs/rules/no-eval
        'no-eval': 'error',

        // Disallow empty functions
        // https://eslint.org/docs/rules/no-empty-function
        'no-empty-function': 'error',

        // Require radix parameter
        // https://eslint.org/docs/rules/radix
        'radix': 'error',

        // Disallow the use of `console`
        // https://eslint.org/docs/rules/no-console
        'no-console': 'error'
    },
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
            },
            parserOptions: {
                'sourceType': 'module'
            },
            rules: {
                // Require `let` or `const` instead of `var`
                // https://eslint.org/docs/rules/no-var
                'no-var': 'error',

                // Require `const` declarations for variables that are never reassigned after declared
                // https://eslint.org/docs/rules/prefer-const
                'prefer-const': 'error'
            }
        },
        {
            // JS files where we support native modern JS.
            files: [
                'media/js/firefox/welcome/**/*.js',
                'media/js/firefox/whatsnew/**/*.js',
                'media/js/firefox/firstrun/**/*.js',
                'tests/unit/**/*.js'
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
