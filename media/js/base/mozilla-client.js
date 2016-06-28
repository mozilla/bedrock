/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function() {
    'use strict';

    /**
     * Provide information on the user's browsing environment, including the platform and browser details.
     *
     * @namespace
     * @see {@link https://developer.mozilla.org/en-US/docs/Gecko_user_agent_string_reference}
     */
    var Client = {};

    /**
     * Detect whether the user's browser is Firefox on any platform. This includes WebKit-based Firefox for iOS.
     *
     * @private
     * @param  {String} ua - browser's user agent string, navigator.userAgent is used if not specified
     * @return {Boolean} result
     */
    Client._isFirefox = function (ua) {
        ua = ua || navigator.userAgent;

        return /\s(Firefox|FxiOS)/.test(ua) && !Client._isLikeFirefox(ua);
    };

    /**
     * Detect whether the user's browser is Firefox for Windows, OS X or Linux.
     *
     * @private
     * @param  {String} ua - browser's user agent string, navigator.userAgent is used if not specified
     * @return {Boolean} result
     */
    Client._isFirefoxDesktop = function (ua) {
        ua = ua || navigator.userAgent;

        return /\sFirefox/.test(ua) && !/Mobile|Tablet|Fennec/.test(ua) && !Client._isLikeFirefox(ua);
    };

    /**
     * Detect whether the user's browser is Firefox for Android.
     *
     * @private
     * @param  {String} ua - browser's user agent string, navigator.userAgent is used if not specified
     * @return {Boolean} result
     */
    Client._isFirefoxAndroid = function (ua) {
        ua = ua || navigator.userAgent;

        return /\sFirefox/.test(ua) && /Android/.test(ua);
    };

    /**
     * Detect whether the user's browser is Firefox for iOS.
     *
     * @private
     * @param  {String} ua - browser's user agent string, navigator.userAgent is used if not specified
     * @return {Boolean} result
     */
    Client._isFirefoxiOS = function (ua) {
        ua = ua || navigator.userAgent;

        return /FxiOS/.test(ua);
    };

    /**
     * Detect whether the user's browser is the Browser app on Firefox OS.
     *
     * @private
     * @param  {String} ua - browser's user agent string, navigator.userAgent is used if not specified
     * @param  {String} pf - browser's platform name, navigator.platform is used if not specified
     * @return {Boolean} result
     */
    Client._isFirefoxFxOS = function (ua, pf) {
        ua = ua || navigator.userAgent;
        pf = (pf === '') ? '' : pf || navigator.platform;

        return /Firefox/.test(ua) && pf === '';
    };

    /**
     * Detect whether the user's browser is Gecko-based. Used on the plugincheck page to support all Gecko browsers.
     *
     * @private
     * @param  {String} ua - browser's user agent string, navigator.userAgent is used if not specified
     * @return {Boolean} result
     */
    Client._isLikeFirefox = function (ua) {
        ua = ua || navigator.userAgent;

        return /Iceweasel|IceCat|SeaMonkey|Camino|like\ Firefox/i.test(ua);
    };

    /**
     * Get the user's Firefox version number. '0' will be returned on Firefox for iOS and non-Firefox browsers.
     *
     * @private
     * @param  {String} ua - browser's user agent string, navigator.userAgent is used if not specified
     * @return {String} version number
     */
    Client._getFirefoxVersion = function (ua) {
        ua = ua || navigator.userAgent;

        var matches = /Firefox\/(\d+(?:\.\d+){1,2})/.exec(ua);

        return (matches && !Client._isLikeFirefox(ua)) ? matches[1] : '0';
    };

    /**
     * Get the user's Firefox major version number. 0 will be returned on Firefox for iOS and non-Firefox browsers.
     *
     * @private
     * @param  {String} ua - browser's user agent string, navigator.userAgent is used if not specified
     * @return {Number} major version number in integer
     */
    Client._getFirefoxMajorVersion = function (ua) {
        return parseInt(Client._getFirefoxVersion(ua), 10);
    };

    /**
     * Detect whether the user's Firefox is up to date or outdated. This data is mainly used for security notifications.
     *
     * @private
     * @param  {Boolean} strict - whether the minor and patch-level version numbers should be compared. Default: true
     * @param  {Boolean} isESR - whether the Firefox update channel is ESR. Default: false
     * @param  {String}  userVer - browser's version number
     * @return {Boolean} result
     */
    Client._isFirefoxUpToDate = function (strict, isESR, userVer) {
        strict = strict === undefined ? true : strict;
        isESR = isESR === undefined ? false : isESR;
        userVer = userVer === undefined ? Client._getFirefoxVersion() : userVer;

        var $html = $(document.documentElement);

        if (!$html.attr('data-esr-versions') || !$html.attr('data-latest-firefox')) {
            return false;
        }

        var versions = isESR ? $html.attr('data-esr-versions').split(' ') : [$html.attr('data-latest-firefox')];
        var userVerArr = userVer.match(/^(\d+(?:\.\d+){1,2})/)[1].split('.');
        var isUpToDate = false;

        // Compare the newer version first
        versions.sort(function(a, b) { return parseFloat(a) < parseFloat(b); });

        // Only check the major version in non-strict comparison mode
        if (!strict) {
            userVerArr.length = 1;
        }

        for (var i = 0; i < versions.length; i++) {
            var latestVerArr = versions[i].split('.');

            // Only check the major version in non-strict comparison mode
            if (!strict) {
                latestVerArr.length = 1;
            }

            for (var j = 0; j < userVerArr.length; j++) {
                if (Number(userVerArr[j]) < Number(latestVerArr[j] || 0)) {
                    isUpToDate = false;
                    break;
                } else {
                    isUpToDate = true;
                }
            }

            if (isUpToDate) {
                break;
            }
        }

        return isUpToDate;
    };

    /**
     * Use the async mozUITour API of Firefox to retrieve the user's browser info, including the update channel and
     * accurate, patch-level version number. This API is available on Firefox 35 and later. See
     * http://bedrock.readthedocs.org/en/latest/uitour.html for details.
     *
     * @param  {Function} callback - callback function to be executed with the Firefox details
     * @return {None}
     */
    Client.getFirefoxDetails = function (callback) {
        // Fire the callback function immediately if cache exists
        if (Client.FirefoxDetails) {
            callback(Client.FirefoxDetails);

            return;
        }

        var callbackID = Math.random().toString(36).replace(/[^a-z]+/g, '');

        var listener = function (event) {
            if (!event.detail || !event.detail.data || event.detail.callbackID !== callbackID) {
                return;
            }

            window.clearTimeout(timer);
            onRetrieved(true, event.detail.data.version, event.detail.data.defaultUpdateChannel);
        };

        var onRetrieved = function (accurate, version, channel) {
            document.removeEventListener('mozUITourResponse', listener);

            var isESR = channel === 'esr';
            var isUpToDate = Client._isFirefoxUpToDate(accurate, accurate ? isESR : false, version);
            var details = Client.FirefoxDetails = {
                'accurate': accurate,
                'version': version,
                'channel': channel,
                'isUpToDate': isUpToDate,
                'isESR': isESR
            };

            callback(details);
        };

        // Prepare fallback function in case the API doesn't work
        var userVer = Client._getFirefoxVersion();
        var fallback = function () { onRetrieved(false, userVer, 'release'); };

        // If Firefox is old or for Android, call the fallback function immediately because the API is not implemented
        if (parseFloat(userVer) < 35 || Client._isFirefoxAndroid()) {
            fallback();

            return;
        }

        // Fire the fallback function in .4 seconds
        var timer = window.setTimeout(fallback, 400);

        // Trigger the API
        document.addEventListener('mozUITourResponse', listener);
        document.dispatchEvent(new CustomEvent('mozUITour', {
            'bubbles': true,
            'detail': {
                'action': 'getConfiguration',
                'data': { 'configuration': 'appinfo', 'callbackID': callbackID }
            }
        }));
    };

    // Append static properties for faster access
    Client.isFirefox = Client._isFirefox();
    Client.isFirefoxDesktop = Client._isFirefoxDesktop();
    Client.isFirefoxAndroid = Client._isFirefoxAndroid();
    Client.isFirefoxiOS = Client._isFirefoxiOS();
    Client.isFirefoxFxOS = Client._isFirefoxFxOS();
    Client.isLikeFirefox = Client._isLikeFirefox();
    Client.FirefoxVersion = Client._getFirefoxVersion();
    Client.FirefoxMajorVersion = Client._getFirefoxMajorVersion();

    // Append platform info as well for convenience
    Client.platform = window.site.platform;
    Client.isMobile = /^(android|ios|fxos)$/.test(Client.platform);
    Client.isDesktop = !Client.isMobile;

    window.Mozilla.Client = Client;

})();
