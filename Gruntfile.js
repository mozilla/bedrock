/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global module, require */

module.exports = function (grunt) {

    // Load grunt tasks automatically
    require('load-grunt-tasks')(grunt);

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        eslint: {
            options: {
                configFile: './.eslintrc.js',
                cache: true
            },
            target: ['media/js/**/*.js', '!media/js/libs/*.js']
        },
        jsonlint: {
            all : {
                src : [
                    '*.json',
                    './**/*.json'
                ]
            }
        },
        watch: {
            scripts: {
                files: ['media/js/**/*.js', '!media/js/libs/*.js'],
                tasks: ['eslint']
            },
            json: {
                files: ['*.json'],
                tasks: ['jsonlint']
            }
        },
        karma: {
            unit: {
                configFile: 'tests/unit/karma.conf.js'
            }
        },
        clean: ['media/css/**/*.less.css']
    });

    // Update the config to only build the changed files.
    grunt.event.on('watch', function (action, filepath) {
        grunt.config(['jsonlint', 'all'], [filepath]);
    });

    // Default task(s).
    grunt.registerTask('default', ['watch']);

    // Run JS tests in Firefox using Karma test runner
    grunt.registerTask('test', ['karma']);

};
