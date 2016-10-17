/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global __dirname, require */

const gulp = require('gulp');
const karma = require('karma');
const eslint = require('gulp-eslint');
const watch = require('gulp-watch');

const lintPaths = [
    'media/js/**/*.js',
    '!media/js/libs/*.js',
    'tests/unit/spec/**/*.js',
    'gulpfile.js'
];

gulp.task('media:watch', () => {
    return gulp.src('./media/**/*')
        .pipe(watch('./media/**/*', {
            'verbose': true
        }))
        .pipe(gulp.dest('./static'));
});

gulp.task('js:test', done => {
    new karma.Server({
        configFile: `${__dirname}/tests/unit/karma.conf.js`,
        singleRun: true
    }, done).start();
});

gulp.task('js:lint', () => {
    return gulp.src(lintPaths)
        .pipe(eslint())
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
});

gulp.task('default', () => {
    gulp.start('media:watch');
    gulp.watch(lintPaths, ['js:lint']);
});
