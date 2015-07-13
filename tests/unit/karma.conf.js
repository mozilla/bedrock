module.exports = function(config) {
    config.set({
        // Karma configuration

        // base path, that will be used to resolve files and exclude
        basePath: '../../',

        frameworks: ['jasmine'],

        // list of files / patterns to load in the browser
        files: [
            'media/js/libs/jquery-1.11.0.min.js',
            'media/js/base/site.js',
            'media/js/base/global.js',
            'media/js/base/mozilla-form-helper.js',
            'media/js/base/mozilla-image-helper.js',
            'media/js/base/mozilla-accordion.js',
            'media/js/base/mozilla-pager.js',
            'media/js/base/search-params.js',
            'media/js/firefox/australis/browser-tour.js',
            'media/js/plugincheck/lib/utils.js',
            'media/js/plugincheck/lib/version-compare.js',
            'media/js/plugincheck/lib/plugincheck.js',
            'media/js/base/send-to-device.js',
            'tests/unit/spec/site.js',
            'tests/unit/spec/global.js',
            'tests/unit/spec/mozilla-form-helper.js',
            'tests/unit/spec/mozilla-image-helper.js',
            'tests/unit/spec/mozilla-accordion.js',
            'tests/unit/spec/mozilla-pager.js',
            'tests/unit/spec/search-params.js',
            'tests/unit/spec/browser-tour.js',
            'tests/unit/spec/utils.js',
            'tests/unit/spec/version-compare.js',
            'tests/unit/spec/plugincheck.js',
            'tests/unit/spec/send-to-device.js',
            {
                pattern: 'node_modules/sinon/pkg/sinon.js',
                watched: false,
                included: true
            },
            {
                pattern: 'tests/img/*',
                included: false,
                served: true
            }
        ],

        proxies: {
            '/img/': '/base/tests/img/'
        },

        // list of files to exclude
        exclude: [],

        // test results reporter to use
        // possible values: 'dots', 'progress', 'junit'
        reporters: ['dots'],

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
