/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const CopyPlugin = require('copy-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const Dotenv = require('dotenv-webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const path = require('path');
const staticBundles = require('./media/static-bundles.json');
const webpack = require('webpack');

function resolveBundles(fileList) {
    return fileList.map((f) => {
        return path.resolve(__dirname, 'media', f);
    });
}

function getBundles() {
    return new Promise((resolve) => {
        const allFiles = {};
        staticBundles['css'].forEach((bundle) => {
            const name = `${bundle['name']}--css`;
            const files = resolveBundles(bundle['files']);
            allFiles[name] = files;
        });
        staticBundles['js'].forEach((bundle) => {
            const name = bundle['name'];
            const files = resolveBundles(bundle['files']);
            allFiles[name] = files;
        });
        resolve(allFiles);
    });
}

module.exports = {
    entry: () => getBundles(),
    output: {
        filename: 'js/[name].js',
        path: path.resolve(__dirname, 'assets/'),
        publicPath: '/media/'
    },
    devtool: 'source-map',
    optimization: {
        minimizer: [
            new TerserPlugin({
                terserOptions: { ie8: true }
            }),
            new CssMinimizerPlugin({})
        ]
    },
    module: {
        rules: [
            {
                test: /\.es6\.js$/,
                include: path.resolve(__dirname, 'media'),
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
            },
            {
                test: /\.scss$/,
                include: path.resolve(__dirname, 'media'),
                exclude: /node_modules/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            url: false
                        }
                    },
                    'sass-loader'
                ]
            }
        ]
    },
    watchOptions: {
        aggregateTimeout: 600,
        ignored: '/node_modules/'
    },
    performance: {
        hints: 'warning'
    },
    devServer: {
        port: 8000,
        open: false,
        hot: false,
        static: false,
        devMiddleware: {
            index: false // specify to enable root proxy'ing
        },
        proxy: [
            {
                context: () => true,
                target: process.env.WP_PROXY_URL || 'http://0.0.0.0:8080'
            }
        ],
        watchFiles: ['media/**/*.js', 'media/**/*.scss', 'bedrock/**/*.html'],
        client: {
            logging: 'error',
            overlay: false
        },
        setupExitSignals: true
    },
    plugins: [
        new CopyPlugin({
            patterns: [
                {
                    // Copy legacy IE scripts that aren't bundled.
                    from: path.resolve(__dirname, 'media/js/ie/'),
                    to: 'js/ie/'
                }
            ]
        }),
        new Dotenv(),
        /**
         * Enable tree shaking of Sentry SDK debug code
         * https://docs.sentry.io/platforms/javascript/configuration/tree-shaking/
         */
        new webpack.DefinePlugin({
            __SENTRY_DEBUG__: false,
            __SENTRY_TRACING__: false,
            __RRWEB_EXCLUDE_IFRAME__: true,
            __RRWEB_EXCLUDE_SHADOW_DOM__: true,
            __SENTRY_EXCLUDE_REPLAY_WORKER__: true
        }),
        new MiniCssExtractPlugin({
            filename: ({ chunk }) =>
                `css/${chunk.name.replace('--css', '')}.css`
        })
    ]
};
