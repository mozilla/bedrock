/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global __dirname, require, process */

var gulp = require('gulp');
var karma = require('karma');
var eslint = require('gulp-eslint');
var watch = require('gulp-watch');
var spawn = require('child_process').spawn;

var lintPaths = [
    'media/js/**/*.js',
    '!media/js/libs/*.js',
    'tests/unit/spec/**/*.js',
    'gulpfile.js'
];

gulp.task('serve:backend', function () {
    var devServerPort = process.env.PORT || 8000;
    process.env.PYTHONUNBUFFERED = 1;
    process.env.PYTHONDONTWRITEBITECODE = 1;
    spawn('python', ['manage.py', 'runserver', '0.0.0.0:' + devServerPort], {
        stdio: 'inherit'
    });
});

gulp.task('media:watch', function () {
    return gulp.src('./media/**/*')
        .pipe(watch('./media/**/*', {
            'verbose': true
        }))
        .pipe(gulp.dest('./static'));
});

gulp.task('js:test', function(done) {
    new karma.Server({
        configFile: __dirname + '/tests/unit/karma.conf.js',
        singleRun: true
    }, done).start();
});

gulp.task('js:lint', function() {
    return gulp.src(lintPaths)
        .pipe(eslint())
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
});

gulp.task('default', function() {
    gulp.start('serve:backend');
    gulp.start('media:watch');
    gulp.watch(lintPaths, ['js:lint']);
});
