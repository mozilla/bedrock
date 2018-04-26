/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
* Utility class for core dataLayer object to track contextual user and page data
*/

if (typeof Mozilla.Analytics == 'undefined') {
    Mozilla.Analytics = {};
}

(function() {
    var analytics = Mozilla.Analytics;

    /** Returns whether page has download button.
    * @param {String} path - URL path name fallback if page ID does not exist.
    * @return {String} string.
    */
    analytics.pageHasDownload = function() {
        return $('[data-download-os]').length ? 'true' : 'false';
    };

    /** Returns whether page has video.
    * @param {String} path - URL path name fallback if page ID does not exist.
    * @return {String} string.
    */
    analytics.pageHasVideo = function() {
        return ($('video').length || $('iframe[src^="https://www.youtube"]').length) ? 'true' : 'false';
    };

    /** Returns page version.
    * @param {String} path - URL path name fallback if page ID does not exist.
    * @return {String} version number from URL.
    */
    analytics.getPageVersion = function(path) {
        var pathName = path ? path : document.location.pathname;
        var versionResults = /firefox\/(\d+(?:\.\d+)?\.\da?\d?)/.exec(pathName);

        return versionResults ? versionResults[1] : null;
    };

    /** Returns latest Fx version.
    * @return {String} latest Fx version.
    */
    analytics.getLatestFxVersion = function() {
        return $('html').data('latest-firefox');
    };

    /** Returns an object containing GA-formatted Sync details
    * https://bugzilla.mozilla.org/show_bug.cgi?id=1457024#c33
    * @param {Object} syncDetails - object of Sync details returned by UITour
    * @return {Object} Sync details formatted for GA
    */
    analytics.formatSyncDetails = function(syncDetails) {
        // set up defaults
        var formatted = {
            FxASegment: 'Not logged in',
            FxAMultiDesktopSync: false,
            FxALogin: false,
            FxAMobileSync: false
        };

        if (syncDetails.setup) {
            formatted.FxALogin = true;

            // user has at least one mobile device sync'd
            if (syncDetails.mobileDevices >= 1) {
                formatted.FxAMobileSync = true;
            }

            // user has more than one desktop devices sync'd
            if (syncDetails.desktopDevices > 1) {
                formatted.FxAMultiDesktopSync = true;
            }

            if (syncDetails.desktopDevices > 1 && syncDetails.mobileDevices > 0) {
                formatted.FxASegment = 'Multi-Desktop and Mobile Sync';
            } else if (syncDetails.desktopDevices === 1 && syncDetails.mobileDevices > 0) {
                formatted.FxASegment = 'Desktop and Mobile Sync';
            } else if (syncDetails.desktopDevices > 1) {
                formatted.FxASegment = 'Multi-Desktop Sync';
            } else {
                formatted.FxASegment = 'Logged in';
            }
        }

        return formatted;
    };

    /** Monkey patch for dataLayer.push
    *   Adds href stripped of locale to link click objects when pushed to the dataLayer,
    *   also removes protocol and host if same as parent page from href.
    */
    analytics.updateDataLayerPush = function(host) {
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

})();
