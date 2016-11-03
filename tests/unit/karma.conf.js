module.exports = function(config) {
    config.set({
        // Karma configuration

        // base path, that will be used to resolve files and exclude
        basePath: '../../',

        frameworks: ['jasmine'],

        // list of files / patterns to load in the browser
        files: [
            'media/js/libs/jquery-1.11.3.min.js',
            'media/js/base/site.js',
            'media/js/base/global.js',
            'media/js/base/dnt-helper.js',
            'media/js/base/core-datalayer-page-id.js',
            'media/js/base/mozilla-accordion-gatrack.js',
            'media/js/base/mozilla-accordion.js',
            'media/js/base/mozilla-client.js',
            'media/js/base/mozilla-firefox-default.js',
            'media/js/base/mozilla-form-helper.js',
            'media/js/base/mozilla-fxa-iframe.js',
            'media/js/base/mozilla-highlight-target.js',
            'media/js/base/mozilla-image-helper.js',
            'media/js/base/mozilla-modal.js',
            'media/js/base/mozilla-pager.js',
            'media/js/base/mozilla-share-cta.js',
            'media/js/base/mozilla-traffic-cop.js',
            'media/js/base/mozilla-video-poster.js',
            'media/js/base/nav-main-resp.js',
            'media/js/base/nav-main.js',
            'media/js/base/mozilla-smoothscroll.js',
            'media/js/base/search-params.js',
            'media/js/base/svg-animation-check.js',
            'media/js/base/mozilla-svg-image-fallback.js',
            'media/js/base/stub-attribution.js',
            'media/js/firefox/new-ios-redirect-helper.js',
            'media/js/firefox/tracking-protection-tour.js',
            'media/js/firefox/whatsnew/whatsnew-zh-tw-49.js',
            'media/js/plugincheck/lib/utils.js',
            'media/js/plugincheck/lib/version-compare.js',
            'media/js/plugincheck/lib/plugincheck.js',
            'media/js/base/send-to-device.js',
            'media/js/base/core-datalayer.js',
            'tests/unit/spec/base/site.js',
            'tests/unit/spec/base/global.js',
            'tests/unit/spec/base/dnt-helper.js',
            'tests/unit/spec/base/core-datalayer-page-id.js',
            'tests/unit/spec/base/mozilla-client.js',
            'tests/unit/spec/base/mozilla-firefox-default.js',
            'tests/unit/spec/base/mozilla-form-helper.js',
            'tests/unit/spec/base/mozilla-fxa-iframe.js',
            'tests/unit/spec/base/mozilla-highlight-target.js',
            'tests/unit/spec/base/mozilla-image-helper.js',
            'tests/unit/spec/base/mozilla-accordion.js',
            'tests/unit/spec/base/mozilla-pager.js',
            'tests/unit/spec/base/mozilla-traffic-cop.js',
            'tests/unit/spec/base/search-params.js',
            'tests/unit/spec/base/mozilla-svg-image-fallback.js',
            'tests/unit/spec/firefox/new-ios-redirect-helper.js',
            'tests/unit/spec/firefox/tracking-protection-tour.js',
            'tests/unit/spec/firefox/whatsnew/whatsnew-zh-tw-49.js',
            'tests/unit/spec/plugincheck/lib/utils.js',
            'tests/unit/spec/plugincheck/lib/version-compare.js',
            'tests/unit/spec/plugincheck/lib/plugincheck.js',
            'tests/unit/spec/base/send-to-device.js',
            'tests/unit/spec/base/core-datalayer.js',
            'tests/unit/spec/base/stub-attribution.js',
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
        reporters: ['dots', 'coverage'],

        preprocessors: {
            'media/js/**/!(libs|test)/*.js': ['coverage']
        },

        coverageReporter: {
            type: 'lcov',
            dir: 'tests/unit/coverage/',
            instrumenterOptions: {
                istanbul: {
                    noCompact: true
                }
            }
        },

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
        autoWatch: true,

        // Start these browsers, currently available:
        // - Chrome
        // - ChromeCanary
        // - Firefox
        // - Opera
        // - Safari (only Mac)
        // - PhantomJS
        // - IE (only Windows)
        browsers: ['Firefox'],

        // If browser does not capture in given timeout [ms], kill it
        captureTimeout: 60000,

        // Continuous Integration mode
        // if true, it capture browsers, run tests and exit
        singleRun: true
    });
};
