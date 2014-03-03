module.exports = function(config) {
    config.set({
        // Karma configuration

        // base path, that will be used to resolve files and exclude
        basePath: '',

        frameworks: ['jasmine'],

        // list of files / patterns to load in the browser
        files: [
            '../libs/jquery-1.11.0.min.js',
            '../base/site.js',
            '../base/global.js',
            '../base/mozilla-form-helper.js',
            'http://localhost:8000/tabzilla/tabzilla.js?build=dev',
            'spec/site.js',
            'spec/global.js',
            'spec/mozilla-form-helper.js',
            'spec/tabzilla.js',
            {
                pattern: '../../../node_modules/sinon/pkg/sinon.js',
                watched: false,
                included: true
            }
        ],

        // list of files to exclude
        exclude: [],

        // test results reporter to use
        // possible values: 'dots', 'progress', 'junit'
        reporters: ['dots', 'junit'],

        junitReporter: {
          outputFile: 'test-results.xml'
        },

        // web server port
        port: 9876,

        // cli runner port
        runnerPort: 9100,

        // enable / disable colors in the output (reporters and logs)
        colors: true,

        // level of logging
        // possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || LOG_INFO || LOG_DEBUG
        logLevel: LOG_INFO,

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
        browsers: ['PhantomJS'],

        // If browser does not capture in given timeout [ms], kill it
        captureTimeout: 60000,

        // Continuous Integration mode
        // if true, it capture browsers, run tests and exit
        singleRun: true
    });
};
