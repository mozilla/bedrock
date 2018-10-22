/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global __dirname, require, process, global */

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
const watch = require('gulp-watch');
const del = require('del');
const karma = require('karma');
const eslint = require('gulp-eslint');
const gulpStylelint = require('gulp-stylelint');
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

const sassPipeline = () => {
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
};

/***********************
 * Start Tasks
 */

/**
 * Delete the static_build directory and start fresh.
 */
gulp.task('clean', () => {
    return del([buildDir, finalDir]);
});

/**
 * Copy assets from various sources into the static_build dir for processing.
 */
gulp.task('assets', () => {
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
});

/**
 * Find all SASS files from bundles in the static_build directory and compile them.
 */
gulp.task('sass', ['assets'], sassPipeline);
gulp.task('sass:no-assets', sassPipeline);

/**
 * Watch and only compile those SASS files that have changed
 */
gulp.task('sass:watch', () => {
    return watch(buildDir + '/css/**/*.scss', {base: buildDir})
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

/**
 * Find all LESS files from bundles in the static_build directory and compile them.
 */
gulp.task('less', ['assets'], () => {
    return gulp.src(allBundleFiles('css', '.less'), {base: buildDir, cwd: buildDir})
        //filter out unchanged less files, only works when watching
        .pipe(gulpif(global.watching, cached('less', cachedOpts)))
        .pipe(gulpif(!production, sourcemaps.init()))
        .pipe(less({inlineJavaScript: true, ieCompat: true}).on('error', handleError('LESS')))
        // we don't serve the source files
        // so include scss content inside the sourcemaps
        .pipe(gulpif(!production, sourcemaps.write({
            'includeContent': true
        })))
        .pipe(gulp.dest(finalDir));
});

/**
 * Watch all LESS files from bundles in the static_build directory and compile them.
 */
gulp.task('less:watch', () => {
    return watch(buildDir + '/css/**/*.less', {base: buildDir})
        .pipe(sourcemaps.init())
        .pipe(less({inlineJavaScript: true, ieCompat: true}).on('error', handleError('LESS')))
        .pipe(sourcemaps.write({
            'includeContent': true
        }))
        .pipe(gulp.dest(finalDir));
});

/**
 * Combine the CSS files after SASS/LESS compilation into bundles
 * based on definitions in the `media/static-bundles.json` file.
 */
gulp.task('css:compile', ['sass', 'less'], () => {
    return merge(staticBundles.css.map(bundleCssFiles));
});


gulp.task('css:watch', () => {
    return gulp.watch(finalDir + '/css/**/*.css', { debounceDelay: 200 }, event => {
        let modBundles = staticBundles.css.filter(bundle => {
            let contains = false;
            bundle.files.every(filename => {
                let cssfn = filename.replace(/\.(less|scss)$/i, '.css');
                if (event.path.endsWith(cssfn)) {
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
});

/**
 * Combine the JS files into bundles
 * based on definitions in the `media/static-bundles.json` file.
 */
gulp.task('js:compile', ['assets'], () => {
    return merge(staticBundles.js.map(bundleJsFiles));
});

/**
 * Watch all JS and rebundle as necessary.
 */
gulp.task('js:watch', () => {
    return gulp.watch(finalDir + '/js/**/*.js', { debounceDelay: 200 }, event => {
        let modBundles = staticBundles.js.filter(bundle => {
            let contains = false;
            bundle.files.every(filename => {
                if (event.path.endsWith(filename)) {
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
});

/**
 * Minify all of the CSS files after compilation.
 */
gulp.task('css:minify', ['css:compile'], () => {
    return gulp.src(finalDir + '/css/**/*.css', {base: buildDir})
        .pipe(cleanCSS().on('error', handleError('CLEANCSS')))
        .pipe(gulp.dest(finalDir));
});

/**
 * Minify all of the JS files after compilation.
 */
gulp.task('js:minify', ['js:compile'], () => {
    return gulp.src(finalDir + '/js/**/*.js', {base: buildDir})
        .pipe(uglify({ie8: true}).on('error', handleError('UGLIFY')))
        .pipe(gulp.dest(finalDir));
});

/**
 * Run the JS test suite.
 */
gulp.task('js:test', done => {
    new karma.Server({
        configFile: `${__dirname}/tests/unit/karma.conf.js`,
        singleRun: true
    }, done).start();
});

/**
 * Run eslint style check on all JS.
 */
gulp.task('js:lint', () => {
    return gulp.src(lintPathsJS)
        .pipe(eslint())
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
});

/**
 * Run CSS style check on all CSS.
 */
gulp.task('css:lint', () => {
    return gulp.src(lintPathsCSS)
        .pipe(gulpStylelint({
            reporters: [{
                formatter: 'string',
                console: true
            }]
        }));
});

gulp.task('all:watch', ['js:compile', 'css:compile'], () => {
    // send everything but scss and less to the final dir
    watch([
        'media/**/*',
        '!media/**/*.{scss,less}'], {base: 'media'})
        .pipe(cached('all', cachedOpts))
        .pipe(gulp.dest(finalDir));
    // send scss and less to the build dir
    watch('media/**/*.{scss,less}', {base: 'media'})
        .pipe(cached('all', cachedOpts))
        .pipe(gulp.dest(buildDir));
});

/**
 * Start the browser-sync daemon for local development.
 */
gulp.task('browser-sync', ['all:watch'], () => {
    const proxyURL = process.env.BS_PROXY_URL || 'localhost:8080';
    const openBrowser = !(process.env.BS_OPEN_BROWSER === 'false');
    return browserSync.init({
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
});

/**
 * Reload tasks used by `gulp watch`.
 */
gulp.task('reload-sass', ['sass:no-assets'], browserSync.reload);
gulp.task('reload', browserSync.reload);

// --------------------------
// DEV/WATCH TASK
// --------------------------
gulp.task('watch', ['browser-sync'], () => {
    global.watching = true;

    gulp.start('sass:watch');
    gulp.start('less:watch');
    gulp.start('css:watch');
    gulp.start('js:watch');

    // --------------------------
    // watch:sass library files
    // --------------------------
    gulp.watch(buildDir + '/css/**/_*.scss', ['reload-sass']);

    // --------------------------
    // watch:js
    // --------------------------
    gulp.watch('media/js/**/*.js', ['js:lint']);

    // --------------------------
    // watch:html
    // --------------------------
    gulp.watch('bedrock/*/templates/**/*.html', ['reload']);

    log.info(colors.green('Watching for changes...'));
});

/**
 * Build all assets in prep for production.
 * Pass the `--production` flag to turn off sourcemaps.
 */
gulp.task('build', ['assets', 'js:minify', 'css:minify']);

gulp.task('default', ['watch']);
