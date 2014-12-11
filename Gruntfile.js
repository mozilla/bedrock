/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

path = require('path');

module.exports = function (grunt) {

    // Load grunt tasks automatically
    require('load-grunt-tasks')(grunt);

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        jshint: {
            options: {
                jshintrc: true
            },
            development: ['media/js/**/*.js']
        },
        jsonlint: {
            all : {
                src : [
                    '*.json',
                    './**/*.json'
                ]
            }
        },
        less: {
            development: {
                options: {
                    paths: ['media/css/']
                },
                files: {
                    'media/css/**/*.css': 'media/css/**/*.less'
                }
            }
        },
        watch: {
            options: {
                port: 35729,
                livereload: true,
                nospawn: true
            },
            css: {
                files: ['media/css/**/*.less'],
                tasks: ['less']
            },
            scripts: {
                files: ['media/js/**/*.js'],
                tasks: ['jshint']
            },
            html: {
                files: ['bedrock/**/*.html']
            },
            json: {
                files: ['*.json'],
                tasks: ['jsonlint']
            }
        },
        karma: {
          unit: {
            configFile: 'media/js/test/karma.conf.js'
          }
        },
        clean: ['media/css/**/*.less.css'],
        phantomas: {
            options: {
                group: {
                    'REQUESTS' : [
                        'requests',
                        'gzipRequests',
                        'notFound',
                        'multipleRequests',
                        'assetsNotGzipped'
                    ],
                    'TIMINGS' : [
                        'timeToFirstByte',
                        'timeToLastByte',
                        'timeToFirstCss',
                        'timeToFirstJs',
                        'timeToFirstImage',
                        'fastestResponse',
                        'slowestResponse',
                        'onDOMReadyTime',
                        'onDOMReadyTimeEnd',
                        'windowOnLoadTime',
                        'windowOnLoadTimeEnd'
                    ],
                    'HTML' : [
                        'bodyHTMLSize',
                        'hiddenContentSize',
                        'whiteSpacesSize',
                        'DOMelementsCount',
                        'DOMelementMaxDepth'
                    ],
                    'JAVASCRIPT' : [
                        'eventsBound',
                        'jsErrors',
                        'consoleMessages',
                        'globalVariables',
                        'localStorageEntries'
                    ],
                    'COUNTS & SIZES' : [
                        'contentLength',
                        'bodySize',
                        'htmlSize',
                        'htmlCount',
                        'cssSize',
                        'cssCount',
                        'jsSize',
                        'jsCount',
                        'imageSize',
                        'imageCount',
                        'webfontSize',
                        'webfontCount'
                    ]
                },
                options: {
                    'film-strip': false,
                    'timeout': 60
                },
                buildUi: true
            },
            homepage: {
                options: {
                    indexPath: './phantomas/home/',
                    url: 'https://www.allizom.org/en-US/'
                }
            },
            firefoxnew: {
                options: {
                    indexPath: './phantomas/firefoxnew/',
                    url: 'https://www.allizom.org/en-US/firefox/new/'
                }
            }
        }
    });

    // Update the config to only build the changed files.
    grunt.event.on('watch', function (action, filepath) {
        grunt.config(['less', 'development', 'files'], [
            { src: filepath, dest: filepath + '.css' }
        ]);

        grunt.config(['jshint', 'development'], [filepath]);

        grunt.config(['jsonlint', 'all'], [filepath]);
    });

    // Default task(s).
    grunt.registerTask('default', ['watch']);

    // Run JS tests in PhantomJS using Karma test runner
    grunt.registerTask('test', ['karma']);

};
