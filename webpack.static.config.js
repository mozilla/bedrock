/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const CopyPlugin = require('copy-webpack-plugin');
const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
    entry: './media/index.js',
    output: {
        path: path.resolve(__dirname, 'assets/'),
        publicPath: '/media/'
    },
    performance: {
        hints: 'warning'
    },
    plugins: [
        // Clean out /assets before processing
        new CleanWebpackPlugin(),
        new CopyPlugin({
            patterns: [
                {
                    // Copy static assets such as images, fonts etc from /media to /assets.
                    from: path.resolve(__dirname, 'media/'),
                    globOptions: {
                        ignore: ['**/*.scss', '**/*.js']
                    }
                },
                {
                    // Copy Protocol images to /assets.
                    from: path.resolve(
                        __dirname,
                        'node_modules/@mozilla-protocol/core/protocol/img/'
                    ),
                    to: 'protocol/img/'
                },
                {
                    // Copy Protocol fonts to /assets.
                    from: path.resolve(
                        __dirname,
                        'node_modules/@mozilla-protocol/core/protocol/fonts/'
                    ),
                    to: 'protocol/fonts/'
                }
            ]
        })
    ]
};
