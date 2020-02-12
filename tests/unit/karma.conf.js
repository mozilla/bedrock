'use strict';

module.exports = function(config) {
    config.set({
        // Karma configuration

        // base path, that will be used to resolve files and exclude
        basePath: '../../',

        frameworks: ['jasmine'],

        // list of files / patterns to load in the browser
        files: [
            // begin common dependencies.
            'media/js/libs/jquery-3.4.1.min.js',
            'media/js/base/site.js',
            'media/js/base/mozilla-utils.js',
            'media/js/base/mozilla-client.js',
            'media/js/base/search-params.js',
            // end common dependencies.
            'media/js/base/mozilla-run.js',
            'media/js/base/core-datalayer-page-id.js',
            'media/js/base/core-datalayer.js',
            'media/js/base/dnt-helper.js',
            'media/js/base/fxa-utm-referral.js',
            'media/js/base/mozilla-convert.js',
            'media/js/base/mozilla-fxa.js',
            'media/js/base/mozilla-fxa-form.js',
            'media/js/base/mozilla-fxa-link.js',
            'media/js/base/mozilla-lazy-load.js',
            'media/js/base/mozilla-fxa-product-button.js',
            'media/js/base/mozilla-pixel.js',
            'media/js/base/mozilla-smoothscroll.js',
            'media/js/base/mozilla-traffic-cop-funnelcake-geo.js',
            'media/js/base/send-to-device.js',
            'media/js/base/stub-attribution-macos.js',
            'media/js/base/stub-attribution.js',
            'media/js/firefox/all/all-downloads-unified.js',
            'media/js/firefox/new/yandex/scene1.js',
            'media/js/ie/mozilla-utils-ie.js',
            'tests/unit/spec/base/mozilla-run.js',
            'tests/unit/spec/base/core-datalayer-page-id.js',
            'tests/unit/spec/base/core-datalayer.js',
            'tests/unit/spec/base/dnt-helper.js',
            'tests/unit/spec/base/fxa-utm-referral.js',
            'tests/unit/spec/base/mozilla-convert.js',
            'tests/unit/spec/base/mozilla-client.js',
            'tests/unit/spec/base/mozilla-fxa.js',
            'tests/unit/spec/base/mozilla-fxa-form.js',
            'tests/unit/spec/base/mozilla-fxa-link.js',
            'tests/unit/spec/base/mozilla-lazy-load.js',
            'tests/unit/spec/base/mozilla-fxa-product-button.js',
            'tests/unit/spec/base/mozilla-pixel.js',
            'tests/unit/spec/base/mozilla-smoothscroll.js',
            'tests/unit/spec/base/mozilla-traffic-cop-funnelcake-geo.js',
            'tests/unit/spec/base/mozilla-utils.js',
            'tests/unit/spec/base/search-params.js',
            'tests/unit/spec/base/send-to-device.js',
            'tests/unit/spec/base/site.js',
            'tests/unit/spec/base/stub-attribution-macos.js',
            'tests/unit/spec/base/stub-attribution.js',
            'tests/unit/spec/firefox/all/all-downloads-unified.js',
            'tests/unit/spec/firefox/new/yandex/scene1.js',
            'tests/unit/spec/ie/mozilla-utils-ie.js',
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

        // Continuous Integration mode
        // if true, it capture browsers, run tests and exit
        singleRun: true
    });
};
