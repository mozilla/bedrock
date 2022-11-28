/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

module.exports = function (config) {
    config.set({
        // Karma configuration

        // base path, that will be used to resolve files and exclude
        basePath: '../../',

        frameworks: ['jasmine', 'webpack'],

        // list of files / patterns to load in the browser
        files: [
            // begin common dependencies.
            'media/js/base/site.js',
            'media/js/base/mozilla-utils.js',
            'media/js/base/mozilla-client.js',
            'media/js/base/search-params.js',
            'media/js/base/mozilla-cookie-helper.js',
            // end common dependencies.
            'media/js/base/banners/mozilla-banner.js',
            'media/js/base/mozilla-run.js',
            'media/js/base/core-datalayer-page-id.js',
            'media/js/base/core-datalayer.js',
            'media/js/base/experiment-utils.es6.js',
            'media/js/base/mozilla-convert.js',
            'media/js/base/mozilla-fxa.js',
            'media/js/base/mozilla-pixel.js',
            'media/js/base/mozilla-smoothscroll.js',
            'media/js/base/stub-attribution.js',
            'media/js/firefox/all/all-downloads-unified.js',
            'media/js/firefox/new/common/thanks.js',
            'media/js/firefox/family/fx-is-default.es6.js',
            'media/js/pocket/mobile-nav.es6.js',
            'media/js/products/vpn/affiliate-attribution.es6.js',
            'media/js/newsletter/form-utils.es6.js',
            'media/js/newsletter/recovery.es6.js',
            'tests/unit/spec/base/core-datalayer-page-id.js',
            'tests/unit/spec/base/core-datalayer.js',
            'tests/unit/spec/base/experiment-utils.js',
            'tests/unit/spec/base/fxa-form.js',
            'tests/unit/spec/base/fxa-link.js',
            'tests/unit/spec/base/fxa-utm.js',
            'tests/unit/spec/base/mozilla-banner.js',
            'tests/unit/spec/base/mozilla-client.js',
            'tests/unit/spec/base/mozilla-convert.js',
            'tests/unit/spec/base/fxa-product-button.js',
            'tests/unit/spec/base/mozilla-fxa.js',
            'tests/unit/spec/base/mozilla-pixel.js',
            'tests/unit/spec/base/mozilla-run.js',
            'tests/unit/spec/base/mozilla-smoothscroll.js',
            'tests/unit/spec/base/mozilla-utils.js',
            'tests/unit/spec/base/search-params.js',
            'tests/unit/spec/base/send-to-device.js',
            'tests/unit/spec/base/site.js',
            'tests/unit/spec/base/stub-attribution.js',
            'tests/unit/spec/careers/filters.js',
            'tests/unit/spec/careers/params.js',
            'tests/unit/spec/firefox/all/all-downloads-unified.js',
            'tests/unit/spec/firefox/new/common/thanks.js',
            'tests/unit/spec/firefox/family/fx-is-default.js',
            'tests/unit/spec/pocket/mobile-nav.js',
            'tests/unit/spec/glean/elements.js',
            'tests/unit/spec/glean/page.js',
            'tests/unit/spec/glean/utils.js',
            'tests/unit/spec/products/vpn/invite.js',
            'tests/unit/spec/products/vpn/affiliate-attribution.js',
            'tests/unit/spec/newsletter/country.js',
            'tests/unit/spec/newsletter/form-utils.js',
            'tests/unit/spec/newsletter/recovery.js',
            'tests/unit/spec/newsletter/newsletter.js',
            'tests/unit/spec/privacy/data-preferences-cookie.js',
            {
                pattern: 'node_modules/sinon/pkg/sinon.js',
                watched: false,
                included: true
            },
            {
                pattern: 'tests/unit/img/*',
                included: false,
                served: true
            }
        ],

        preprocessors: {
            'media/js/**/*.js': ['webpack', 'sourcemap'],
            'tests/unit/**/*.js': ['webpack', 'sourcemap']
        },

        webpack: {
            devtool: 'inline-source-map',
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
        },

        proxies: {
            '/img/': '/base/tests/unit/img/'
        },

        // list of files to exclude
        exclude: [],

        // test results reporter to use
        // possible values: 'dots', 'progress', 'junit', 'coverage'
        reporters: ['progress'],

        // web server port
        port: 9876,

        // cli runner port
        runnerPort: 9100,

        // enable / disable colors in the output (reporters and logs)
        colors: true,

        // level of logging
        // possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || LOG_INFO || LOG_DEBUG
        //logLevel: console.LOG_INFO,

        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: false,

        // Start these browsers, currently available:
        // - Chrome
        // - ChromeCanary
        // - Firefox
        // - Opera
        // - Safari (only Mac)
        // - PhantomJS
        // - IE (only Windows)
        browsers: ['Firefox', 'Chrome'],

        // If browser does not capture in given timeout [ms], kill it
        captureTimeout: 60000,

        // Supress console logs triggered in code.
        client: {
            captureConsole: false
        },

        // Continuous Integration mode
        // if true, it capture browsers, run tests and exit
        singleRun: true
    });
};
