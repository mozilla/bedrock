/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

'use strict';

const gulp = require('gulp');
const cached = require('gulp-cached');
const filter = require('gulp-filter');
const log = require('fancy-log');
const colors = require('ansi-colors');
const gulpif = require('gulp-if');
const sass = require('gulp-sass');
const less = require('gulp-less');
const cleanCSS = require('gulp-clean-css');
const uglify = require('gulp-uglify');
const concat = require('gulp-concat');
const sourcemaps = require('gulp-sourcemaps');
const del = require('del');
const karma = require('karma');
const eslint = require('gulp-eslint');
const gulpStylelint = require('gulp-stylelint');
const gulpJsonLint = require('gulp-jsonlint');
const argv = require('yargs').argv;
const browserSync = require('browser-sync').create();
const merge = require('merge-stream');
const staticBundles = require('./media/static-bundles.json');

// directory for building LESS, SASS, and bundles
const buildDir = 'static_build';

// directory for the final assets ready for consumption
const finalDir = 'static_final';

const lintPathsJS = [
    'media/js/**/*.js',
    '!media/js/libs/*.js',
    'tests/unit/spec/**/*.js',
    'gulpfile.js'
];

const lintPathsCSS = [
    'media/css/**/*.scss',
    'media/css/**/*.less',
    'media/css/**/*.css',
    '!media/css/libs/*'
];

const lintPathsJSON = [
    'bedrock/base/templates/includes/structured-data/**/*.json'
];

const cachedOpts = {
    optimizeMemory: true
};

global.watching = false;

// gulp build --production
const production = !!argv.production;

const allBundleFiles = (fileType, fileExt) => {
    let allFiles = [];
    staticBundles[fileType].forEach(bundle => {
        bundle.files.forEach(bFile => {
            if (bFile.endsWith(fileExt)) {
                allFiles.push(bFile);
            }
        });
    });
    return allFiles;
};

const handleError = task => {
    return err => {
        log.warn(colors.bold(colors.red(`[ERROR] ${task}:`)), colors.red(err));
    };
};

const bundleCssFiles = bundle => {
    let bundleFilename = `css/BUNDLES/${bundle.name}.css`;
    if (global.watching) {
        log.info(`building: ${bundleFilename}`);
    }
    let cssFiles = bundle.files.map(fileName => {
        if (!fileName.endsWith('.css')) {
            return fileName.replace(/\.(less|scss)$/i, '.css');
        }
        return fileName;
    });
    return gulp.src(cssFiles, {base: finalDir, 'cwd': finalDir})
        .pipe(concat(bundleFilename))
        .pipe(gulp.dest(finalDir));
};

const bundleJsFiles = bundle => {
    let bundleFilename = `js/BUNDLES/${bundle.name}.js`;
    if (global.watching) {
        log.info(`building: ${bundleFilename}`);
    }
    return gulp.src(bundle.files, {base: finalDir, cwd: finalDir})
        .pipe(gulpif(!production, sourcemaps.init()))
        .pipe(concat(bundleFilename))
        .pipe(gulpif(!production, sourcemaps.write({
            'includeContent': true
        })))
        .pipe(gulp.dest(finalDir));
};

/***********************
 * Start Tasks
 */

/**
 * Delete the static_build directory and start fresh.
 */
function clean(cb) {
    del([buildDir, finalDir]).then(() => {
        cb();
    });
}

/**
 * Copy assets from various sources into the static_build dir for processing.
 */
function assetsCopy() {
    return merge([
        // SASS and LESS go to build dir
        gulp.src([
            'media/**/*.{scss,less}',
            'node_modules/@mozilla-protocol/core/**/*',
            '!node_modules/@mozilla-protocol/core/*'])
            .pipe(gulpif(global.watching, cached('all', cachedOpts)))
            .pipe(gulp.dest(buildDir)),
        // Everything else goes to final dir
        gulp.src([
            'media/**/*',
            '!media/**/*.{scss,less}',
            'node_modules/@mozilla-protocol/core/**/*',
            '!node_modules/@mozilla-protocol/core/**/*.scss',
            '!node_modules/@mozilla-protocol/core/*'])
            .pipe(gulpif(global.watching, cached('all', cachedOpts)))
            .pipe(gulp.dest(finalDir)),
    ]);
}

/**
 * Find all SASS files from bundles in the static_build directory and compile them.
 */
function sassCompileAllFiles() {
    return gulp.src(allBundleFiles('css', '.scss'), { base: buildDir, cwd: buildDir })
        .pipe(gulpif(!production, sourcemaps.init()))
        .pipe(sass({
            sourceComments: !production,
            outputStyle: production ? 'compressed' : 'nested'
        }).on('error', handleError('SASS')))
        .pipe(gulpif(!production, sourcemaps.write({
            'includeContent': true
        })))
        .pipe(gulp.dest(finalDir));
}

/**
 * Watch and only compile those SASS files that have changed
 */
function sassWatch(cb) {
    const sassWatcher = gulp.watch(buildDir + '/css/**/*.scss', {base: buildDir});

    sassWatcher.on('change', function(path) {
        return gulp.src(path, {base: buildDir})
            // filter out internal imports (files starting with "_" )
            .pipe(filter(file => {
                return !file.relative.startsWith('_');
            }))
            .pipe(sourcemaps.init())
            .pipe(sass({
                sourceComments: !production,
                outputStyle: production ? 'compressed' : 'nested'
            }).on('error', handleError('SASS')))
            .pipe(sourcemaps.write({
                'includeContent': true
            }))
            .pipe(gulp.dest(finalDir));
    });

    cb();
}

/**
 * Find all LESS files from bundles in the static_build directory and compile them.
 */
function lessCompileAllFiles() {
    return gulp.src(allBundleFiles('css', '.less'), {base: buildDir, cwd: buildDir})
        //filter out unchanged less files, only works when watching
        .pipe(gulpif(global.watching, cached('less', cachedOpts)))
        .pipe(gulpif(!production, sourcemaps.init()))
        .pipe(less({javascriptEnabled: true, ieCompat: true}).on('error', handleError('LESS')))
        // we don't serve the source files
        // so include scss content inside the sourcemaps
        .pipe(gulpif(!production, sourcemaps.write({
            'includeContent': true
        })))
        .pipe(gulp.dest(finalDir));
}

/**
 * Watch all LESS files from bundles in the static_build directory and compile them.
 */
function lessWatch(cb) {
    const lessWatcher = gulp.watch(buildDir + '/css/**/*.less', {base: buildDir});

    lessWatcher.on('change', function(path) {
        return gulp.src(path, {base: buildDir})
            .pipe(sourcemaps.init())
            .pipe(less({javascriptEnabled: true, ieCompat: true}).on('error', handleError('LESS')))
            .pipe(sourcemaps.write({
                'includeContent': true
            }))
            .pipe(gulp.dest(finalDir));
    });

    cb();
}

/**
 * Combine the CSS files after SASS/LESS compilation into bundles
 * based on definitions in the `media/static-bundles.json` file.
 */
function cssCompileBundles() {
    return merge(staticBundles.css.map(bundleCssFiles));
}

/**
 * Watch for changes to CSS files in the `static_final` directory
 * and recompile bundles when necessary.
 */
function cssWatch(cb) {
    const cssWatcher = gulp.watch(finalDir + '/css/**/*.css');

    cssWatcher.on('change', function(path) {
        let modBundles = staticBundles.css.filter(bundle => {
            let contains = false;
            bundle.files.every(filename => {
                let cssfn = filename.replace(/\.(less|scss)$/i, '.css');
                if (path.endsWith(cssfn)) {
                    contains = true;
                    return false;
                }
                return true;
            });
            return contains;
        });
        if (modBundles) {
            modBundles.map(bundleCssFiles);
            browserSync.reload();
        }
    });

    cb();
}

/**
 * Combine the JS files into bundles
 * based on definitions in the `media/static-bundles.json` file.
 */
function jsCompileBundles() {
    return merge(staticBundles.js.map(bundleJsFiles));
}

/**
 * Watch for changes to JS files in the `static_final` directory
 * and recompile bundles when necessary.
 */
function jsWatch(cb) {
    const jsWatcher = gulp.watch(finalDir + '/js/**/*.js');

    jsWatcher.on('change', function(path) {
        let modBundles = staticBundles.js.filter(bundle => {
            let contains = false;
            bundle.files.every(filename => {
                if (path.endsWith(filename)) {
                    contains = true;
                    return false;
                }
                return true;
            });
            return contains;
        });
        if (modBundles) {
            modBundles.map(bundleJsFiles);
            browserSync.reload();
        }
    });

    cb();
}

/**
 * Minify all of the CSS files after compilation.
 */
function cssMinify() {
    return gulp.src(finalDir + '/css/**/*.css', {base: buildDir})
        .pipe(cleanCSS({
            compatibility: {
                properties: {
                    iePrefixHack: true, // controls keeping IE prefix hack used in oldIE.scss
                },
            }
        }).on('error', handleError('CLEANCSS')))
        .pipe(gulp.dest(finalDir));
}

/**
 * Minify all of the JS files after compilation.
 */
function jsMinify() {
    return gulp.src(finalDir + '/js/**/*.js', {base: buildDir})
        .pipe(uglify({ie8: true}).on('error', handleError('UGLIFY')))
        .pipe(gulp.dest(finalDir));
}

/**
 * Run the JS test suite.
 */
function jsTest(cb) {
    new karma.Server({
        configFile: `${__dirname}/tests/unit/karma.conf.js`,
        singleRun: true
    }, cb).start();
}
gulp.task('js:test', jsTest);

/**
 * Run eslint style check on all JS.
 */
function jsLint() {
    return gulp.src(lintPathsJS)
        .pipe(eslint())
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
}
gulp.task('js:lint', jsLint);

/**
 * Run CSS style check on all CSS.
 */
function cssLint() {
    return gulp.src(lintPathsCSS)
        .pipe(gulpStylelint({
            reporters: [{
                formatter: 'string',
                console: true
            }],
            debug: true
        }));
}
gulp.task('css:lint', cssLint);

/**
 * Run JSON lint on JSON files
 */

function jsonLint() {
    return gulp.src(lintPathsJSON)
        .pipe(gulpJsonLint())
        .pipe(gulpJsonLint.reporter());
}
gulp.task('json:lint', jsonLint);

/**
 * Watch for changes in the `media` directory and copy changed files to
 * either `static_build` or `static_final` depending on the file type.
 */
function assetsWatch(cb) {
    const assetsWatcher = gulp.watch(['media/**/*', '!media/**/*.{scss,less}'], {base: 'media'});
    const cssWatcher = gulp.watch('media/**/*.{scss,less}', {base: 'media'});
    // send everything but scss and less to the final dir
    assetsWatcher.on('change', function(path) {
        return gulp.src(path, {base: 'media'})
            .pipe(cached('all', cachedOpts))
            .pipe(gulp.dest(finalDir));
    });
    // send scss and less to the build dir
    cssWatcher.on('change', function(path) {
        return gulp.src(path, {base: 'media'})
            .pipe(cached('all', cachedOpts))
            .pipe(gulp.dest(buildDir));
    });

    cb();
}

/**
 * Start the browser-sync daemon for local development.
 */
function browserSyncTask(cb) {
    const proxyURL = process.env.BS_PROXY_URL || 'localhost:8080';
    const openBrowser = !(process.env.BS_OPEN_BROWSER === 'false');
    browserSync.init({
        port: 8000,
        proxy: proxyURL,
        open: openBrowser,
        notify: true,
        reloadDelay: 300,
        reloadDebounce: 500,
        injectChanges: false,
        ui: {
            port: 8001
        },
        serveStatic: [{
            route: '/media',
            dir: finalDir
        }]
    });
    cb();
}

/**
 * Reload tasks used by `gulp watch`.
 */
function reloadBrowser(cb) {
    browserSync.reload();
    cb();
}

const reloadSass = gulp.series(
    sassCompileAllFiles,
    reloadBrowser
);

// --------------------------
// DEV/WATCH TASK
// --------------------------
function devWatch(cb) {
    global.watching = true;

    // --------------------------
    // watch:sass library files
    // --------------------------
    gulp.watch(buildDir + '/css/**/_*.scss', reloadSass);

    // --------------------------
    // watch:js
    // --------------------------
    gulp.watch('media/js/**/*.js', jsLint);

    // --------------------------
    // watch:html
    // --------------------------
    gulp.watch('bedrock/*/templates/**/*.html', reloadBrowser);

    log.info(colors.green('Watching for changes...'));

    cb();
}

/**
 * Build all assets in prep for production.
 * Pass the `--production` flag to turn off sourcemaps.
 */
const buildTask = gulp.series(
    clean,
    assetsCopy,
    gulp.parallel(sassCompileAllFiles, lessCompileAllFiles),
    gulp.parallel(jsCompileBundles, cssCompileBundles),
    gulp.parallel(jsMinify, cssMinify)
);
gulp.task('build', buildTask);

const defaultTask = gulp.series(
    clean,
    assetsCopy,
    gulp.parallel(sassCompileAllFiles, lessCompileAllFiles),
    gulp.parallel(jsCompileBundles, cssCompileBundles),
    assetsWatch,
    browserSyncTask,
    gulp.parallel(sassWatch, lessWatch, cssWatch, jsWatch),
    devWatch
);
gulp.task('default', defaultTask);

module.exports = defaultTask;
