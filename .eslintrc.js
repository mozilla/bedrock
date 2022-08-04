/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

module.exports = {
    env: {
        browser: true,
        commonjs: true
    },
    extends: ['eslint:recommended', 'plugin:json/recommended', 'prettier'],
    rules: {
        // Require strict mode directive in top level functions
        // https://eslint.org/docs/rules/strict
        strict: ['error', 'function'],

        // Use type-safe equality operators
        // https://eslint.org/docs/rules/eqeqeq
        eqeqeq: ['error', 'always'],

        // Treat var statements as if they were block scoped
        // https://eslint.org/docs/rules/block-scoped-var
        'block-scoped-var': 'error',

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
        radix: 'error',

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
            files: ['media/js/**/*.es6.js'],
            env: {
                es2017: true
            },
            parserOptions: {
                sourceType: 'module'
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
                'media/js/firefox/firstrun/**/*.js'
            ],
            env: {
                es2017: true
            }
        },
        {
            // JS Karma test files.
            files: ['tests/unit/**/*.js'],
            env: {
                es2017: true,
                jasmine: true
            },
            parserOptions: {
                sourceType: 'module'
            },
            globals: {
                sinon: 'writable'
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
                node: true,
                es2017: true
            },
            rules: {
                strict: ['error', 'global']
            }
        }
    ],
    globals: {
        Mozilla: 'writable',
        Mzp: 'writable',
        site: 'writable'
    }
};
