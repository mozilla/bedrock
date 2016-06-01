/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof Mozilla == 'undefined') {
    var Mozilla = {};
}

/**
* Utility class for core dataLayer object to track contextual user and page data
*/

(function() {
    var Analytics = {};

    /** Returns page ID used in Event Category for GA events tracked on page.
    * @param {String} path - URL path name fallback if page ID does not exist.
    * @return {String} GTM page ID.
    */
    Analytics.getPageId = function(path) {
        var pageId = $('html').attr('data-gtm-page-id');
        var pathName = path ? path : document.location.pathname;

        return pageId ? pageId : pathName.replace(/\/[^\/]*/, '');
    };

    /** Returns whether page has download button.
    * @param {String} path - URL path name fallback if page ID does not exist.
    * @return {String} string.
    */
    Analytics.pageHasDownload = function() {
        return $('[data-download-os]').length ? 'true' : 'false';
    };

    /** Returns whether page has video.
    * @param {String} path - URL path name fallback if page ID does not exist.
    * @return {String} string.
    */
    Analytics.pageHasVideo = function() {
        return ($('video').length || $('iframe[src^="https://www.youtube"]').length) ? 'true' : 'false';
    };

    /** Returns page version.
    * @param {String} path - URL path name fallback if page ID does not exist.
    * @return {String} version number from URL.
    */
    Analytics.getPageVersion = function(path) {
        var pathName = path ? path : document.location.pathname;
        var versionResults = /firefox\/(\d+(?:\.\d+)?\.\da?\d?)/.exec(pathName);

        return versionResults ? versionResults[1] : null;
    };

    /** Monkey patch for dataLayer.push
    *   Adds href stripped of locale to link click objects when pushed to the dataLayer,
    *   also removes protocol and host if same as parent page from href.
    */
    Analytics.updateDataLayerPush = function(host) {
        var dataLayer = window.dataLayer = window.dataLayer || [];
        var hostname = host || document.location.hostname;

        dataLayer.defaultPush = dataLayer.push;
        dataLayer.push = function() {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i].event === 'gtm.linkClick') {
                    var element = arguments[i]['gtm.element'];
                    var href = element.href;

                    if (element.hostname === hostname) {
                        // remove host and locale from internal links
                        var path = href.replace(/^(?:https?\:\/\/)(?:[^\/])*/, '');
                        var locale = path.match(/^(\/\w{2}\-\w{2}\/|\/\w{2,3}\/)/);

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

    Mozilla.Analytics = Analytics;

})();
