/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const js = require('@eslint/js');
const globals = require('globals');
const eslintConfigPrettier = require('eslint-config-prettier');

const baseRules = {
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
    'no-console': 'error',

    // Allow unused vars in caught errors for older
    // browsers that don't support optional catch binding
    // https://eslint.org/docs/latest/rules/no-unused-vars#options
    'no-unused-vars': [
        'error',
        {
            caughtErrors: 'none'
        }
    ]
};

const extendedRules = {
    // Require `let` or `const` instead of `var`
    // https://eslint.org/docs/rules/no-var
    'no-var': 'error',

    // Require `const` declarations for variables that are never reassigned after declared
    // https://eslint.org/docs/rules/prefer-const
    'prefer-const': 'error'
};

const nodeRules = {
    // Require strict mode directive in global scope
    // https://eslint.org/docs/rules/strict
    strict: ['error', 'global']
};

const customGlobals = {
    Mozilla: true,
    site: true
};

const testingGlobals = {
    sinon: true
};

module.exports = [
    js.configs.recommended,
    eslintConfigPrettier,
    {
        ignores: [
            'docs/_build/**/*.js',
            'media/js/ie/libs/**/*.js',
            'media/js/libs/**/*.js',
            'static/**/*.js',
            'tests/unit/dist/**/*.js'
        ]
    },
    {
        files: ['media/js/**/*.js'],
        languageOptions: {
            sourceType: 'script',
            globals: {
                ...customGlobals,
                ...globals.browser,
                ...globals.commonjs
            }
        },
        rules: baseRules
    },
    {
        files: ['media/js/**/*.es6.js'],
        languageOptions: {
            ecmaVersion: 2018,
            sourceType: 'module',
            globals: {
                ...customGlobals,
                ...globals.browser,
                ...globals.commonjs
            }
        },
        rules: {
            ...baseRules,
            ...extendedRules
        }
    },
    {
        // JS files where we support native modern JS.
        files: [
            'media/js/firefox/welcome/**/*.js',
            'media/js/firefox/whatsnew/**/*.js',
            'media/js/firefox/firstrun/**/*.js'
        ],
        languageOptions: {
            ecmaVersion: 'latest',
            globals: customGlobals
        },
        rules: {
            ...baseRules,
            ...extendedRules
        }
    },
    {
        // JS Jasmine test files.
        files: ['tests/unit/**/*.js'],
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'module',
            globals: {
                ...customGlobals,
                ...testingGlobals,
                ...globals.browser,
                ...globals.jasmine
            }
        },
        rules: {
            ...baseRules,
            ...extendedRules
        }
    },
    {
        // JS Playwright test files.
        files: ['tests/playwright/**/*.js'],
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'script',
            globals: {
                ...globals.browser,
                ...globals.node,
                ...globals.commonjs
            }
        },
        rules: {
            ...baseRules,
            ...extendedRules,
            ...nodeRules
        }
    },
    {
        // JS build files for local dev.
        files: [
            'eslint.config.js',
            'webpack.config.js',
            'webpack.static.config.js',
            'webpack.test.config.js'
        ],
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'script',
            globals: {
                ...globals.node,
                ...globals.commonjs
            }
        },
        rules: {
            ...baseRules,
            ...extendedRules,
            ...nodeRules
        }
    }
];
