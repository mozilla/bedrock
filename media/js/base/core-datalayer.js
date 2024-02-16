/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * Utility class for core dataLayer object to track contextual user and page data
 */

if (typeof window.Mozilla.Analytics === 'undefined') {
    window.Mozilla.Analytics = {};
}

(function () {
    'use strict';

    var analytics = Mozilla.Analytics;
    var isModernBrowser =
        'querySelector' in document && 'querySelectorAll' in document;

    /** Returns whether page has download button.
     * @param {String} path - URL path name fallback if page ID does not exist.
     * @return {String} string.
     */
    analytics.pageHasDownload = function () {
        if (!isModernBrowser) {
            return 'false';
        }
        return document.querySelector('[data-download-os]') !== null
            ? 'true'
            : 'false';
    };

    /** Returns whether page has video.
     * @param {String} path - URL path name fallback if page ID does not exist.
     * @return {String} string.
     */
    analytics.pageHasVideo = function () {
        if (!isModernBrowser) {
            return 'false';
        }
        return document.querySelector('video') !== null ||
            document.querySelector('iframe[src^="https://www.youtube"]') !==
                null
            ? 'true'
            : 'false';
    };

    /** Returns page version.
     * @param {String} path - URL path name fallback if page ID does not exist.
     * @return {String} version number from URL.
     */
    analytics.getPageVersion = function (path) {
        var pathName = path ? path : document.location.pathname;
        var versionResults = /firefox\/(\d+(?:\.\d+)?\.\da?\d?)/.exec(pathName);

        return versionResults ? versionResults[1] : null;
    };

    /** Returns latest Fx version.
     * @return {String} latest Fx version.
     */
    analytics.getLatestFxVersion = function () {
        return document
            .getElementsByTagName('html')[0]
            .getAttribute('data-latest-firefox');
    };

    analytics.getAMOExperiment = function (params) {
        var allowedExperiment = /^\d{8}_amo_.[\w/.%-]{1,50}$/; // should match the format YYYYMMDD_amo_experiment_name.
        var allowedVariation = /^[\w/.%-]{1,50}$/; // allow alpha numeric & common URL encoded chars.

        if (
            Object.prototype.hasOwnProperty.call(params, 'experiment') &&
            Object.prototype.hasOwnProperty.call(params, 'variation')
        ) {
            var experiment = decodeURIComponent(params['experiment']);
            var variation = decodeURIComponent(params['variation']);

            if (
                allowedExperiment.test(experiment) &&
                allowedVariation.test(variation)
            ) {
                return {
                    experiment: experiment,
                    variation: variation
                };
            }
        }

        return null;
    };

    /** Monkey patch for dataLayer.push
     *   Adds href stripped of locale to link click objects when pushed to the dataLayer,
     *   also removes protocol and host if same as parent page from href.
     */
    analytics.updateDataLayerPush = function (host) {
        var dataLayer = (window.dataLayer = window.dataLayer || []);
        var hostname = host || document.location.hostname;

        dataLayer.defaultPush = dataLayer.push;
        dataLayer.push = function () {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i].event === 'gtm.linkClick') {
                    var element = arguments[i]['gtm.element'];
                    var href = element.href;

                    if (element.hostname === hostname) {
                        // remove host and locale from internal links
                        var path = href.replace(
                            /^(?:https?:\/\/)(?:[^/])*/,
                            ''
                        );
                        var locale = path.match(
                            /^(\/\w{2}-\w{2}\/|\/\w{2,3}\/)/
                        );

                        path = locale ? path.replace(locale[0], '/') : path;
                        arguments[i].newClickHref = path;
                    } else {
                        arguments[i].newClickHref = href;
                    }

                    dataLayer.defaultPush(arguments[i]);
                } else {
                    dataLayer.defaultPush(arguments[i]);
                }
            }
        };
    };
})();
