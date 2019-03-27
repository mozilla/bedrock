module.exports = {
    env: {
        'jquery': true,
        'jasmine': true
    },
    extends: '@mozilla-protocol/eslint-config',
    rules: {
        'no-useless-escape': 1,
    },
    /**
     * Provide a set of overrides for `gulpfile.js` in the root directory.
     * Ideally we want to extend @mozilla-protocol/eslint-config/index-node,
     * however ESLint does not currently allow extends inside glob overrides.
     * (see https://github.com/eslint/eslint/issues/8813)
     * */
    overrides: [
        {
            files: 'gulpfile.js',
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
