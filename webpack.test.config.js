/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const path = require('path');
const glob = require('glob');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
    entry: {
        test: glob.sync('tests/unit/spec/**/*.js'),
        'test-deps': [
            'media/js/base/site.js',
            'media/js/base/mozilla-utils.js',
            'media/js/base/mozilla-client.js',
            'media/js/base/search-params.js',
            'media/js/base/mozilla-cookie-helper.js',
            'media/js/base/banners/mozilla-banner.js',
            'media/js/base/mozilla-run.js',
            'media/js/base/core-datalayer-page-id.js',
            'media/js/base/core-datalayer.js',
            'media/js/base/experiment-utils.es6.js',
            'media/js/base/mozilla-fxa.js',
            'media/js/base/mozilla-smoothscroll.js',
            'media/js/base/stub-attribution.js',
            'media/js/firefox/all/all-downloads-unified.js',
            'media/js/firefox/new/common/thanks.js',
            'media/js/firefox/family/fx-is-default.es6.js',
            'media/js/pocket/analytics.es6.js',
            'media/js/pocket/mobile-nav.es6.js',
            'media/js/products/shared/affiliate-attribution.es6.js',
            'media/js/newsletter/form-utils.es6.js',
            'media/js/newsletter/recovery.es6.js',
            'node_modules/sinon/pkg/sinon.js'
        ]
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'tests/unit/dist')
    },
    plugins: [new CleanWebpackPlugin()],
    resolve: {
        modules: [__dirname, 'src', 'node_modules'],
        extensions: ['*', '.js']
    },
    module: {
        rules: [
            {
                test: /\.es6\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            [
                                '@babel/preset-env',
                                {
                                    targets: {
                                        ie: '10'
                                    }
                                }
                            ]
                        ]
                    }
                }
            }
        ]
    }
};
