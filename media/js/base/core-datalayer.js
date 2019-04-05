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
    var isModernBrowser = 'querySelector' in document && 'querySelectorAll' in document;

    /** Returns whether page has download button.
    * @param {String} path - URL path name fallback if page ID does not exist.
    * @return {String} string.
    */
    analytics.pageHasDownload = function() {
        if (!isModernBrowser) {
            return 'false';
        }
        return document.querySelector('[data-download-os]') !== null ? 'true' : 'false';
    };

    /** Returns whether page has video.
    * @param {String} path - URL path name fallback if page ID does not exist.
    * @return {String} string.
    */
    analytics.pageHasVideo = function() {
        if (!isModernBrowser) {
            return 'false';
        }
        return (document.querySelector('video') !== null || document.querySelector('iframe[src^="https://www.youtube"]') !== null) ? 'true' : 'false';
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
        return document.getElementsByTagName('html')[0].getAttribute('data-latest-firefox');
    };

    /** Returns true if user is running Windows 10 in S mode.
    * @return {Boolean}.
    */
    analytics.isWin10S = function() {
        try {
            var mode = JSON.parse(window.external.getHostEnvironmentValue('os-mode'));
            if (mode && mode['os-mode'] === '2') {
                return true;
            }
            return false;
        } catch(e) {
            return false;
        }
    };

    /** Returns an object containing GA-formatted FxA details
    * The specs for this are a combination of:
    * - https://bugzilla.mozilla.org/show_bug.cgi?id=1457024#c33
    * - https://bugzilla.mozilla.org/show_bug.cgi?id=1457004#c22
    * Our implmentation it might deviate from the spec where there was conflicting info in the spec.
    *
    * Data arrives from Client.getFxaDetails as an object, see getFxaDetails for details.
    *
    * @param {Object} FxaDetails - object of FxA details returned by getFxaDetails
    * @return {Object} FxA details formatted for GA
    */
    analytics.formatFxaDetails = function(FxaDetails) {
        // start with empty object
        var formatted = {};

        if (FxaDetails.firefox === true) {
            // only add FxA account details if this is Fx, otherwise their segment is just 'Not Firefox'
            if (FxaDetails.mobile) {
                // Firefox Mobile
                formatted.FxASegment = 'Firefox Mobile';
            } else {
                // Firefox Desktop
                if (FxaDetails.setup) {
                    // set FxALogin
                    formatted.FxALogin = true;
                    // set FxASegment with default value, to be refined
                    formatted.FxASegment = 'Logged in';
                    // Change FxASegment to Legacy if this is an old browser
                    if (FxaDetails.legacy === true) {
                        formatted.FxASegment = 'Legacy Firefox';
                    }

                    // variables to compare to determine the segments
                    var mobileSync = false;
                    var desktopSync = false;
                    var desktopMultiSync = false;

                    // set FxAMobileSync
                    if (FxaDetails.mobileDevices > 0) {
                        formatted.FxAMobileSync = true;
                        mobileSync = true;
                    } else if (FxaDetails.mobileDevices === 0) {
                        formatted.FxAMobileSync = false;
                    } else {
                        formatted.FxAMobileSync = 'unknown';
                    }

                    // set FxAMultiDesktopSync
                    if (FxaDetails.desktopDevices > 1) {
                        formatted.FxAMultiDesktopSync = true;
                        desktopMultiSync = true;
                    } else if (FxaDetails.desktopDevices === 1) {
                        formatted.FxAMultiDesktopSync = false;
                        desktopSync = true;
                    } else if (FxaDetails.desktopDevices === 0){
                        formatted.FxAMultiDesktopSync = false;
                    } else {
                        formatted.FxAMultiDesktopSync = 'unknown';
                    }

                    // refine FxASegment based on device syncing
                    if (desktopMultiSync && mobileSync) {
                        formatted.FxASegment = 'Multi-Desktop and Mobile Sync';
                    } else if (desktopSync && mobileSync) {
                        formatted.FxASegment = 'Desktop and Mobile Sync';
                    } else if (desktopMultiSync) {
                        formatted.FxASegment = 'Multi-Desktop Sync';
                    }

                } else {
                    // Not logged into FxA
                    if (FxaDetails.legacy === true) {
                        // too old to support UITour or FxA, or pre FxASegment and logged out
                        formatted.FxASegment = 'Legacy Firefox';
                        formatted.FxALogin = 'unknown';
                    } else {
                        // not too old, just logged out
                        formatted.FxASegment = 'Not logged in';
                        formatted.FxALogin = false;
                    }
                }
            }
        } else {
            formatted.FxASegment = 'Not Firefox';
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
