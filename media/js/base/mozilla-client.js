/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function() {
    'use strict';

    var Client = {};

    /**
     * Get the user's Firefox version number. '0' will be returned on non-Firefox browsers.
     *
     * @param  {String} ua - browser's user agent string, navigator.userAgent is used if not specified
     * @return {String} version number
     */
    Client._getFirefoxVersion = function (ua) {
        ua = ua || navigator.userAgent;

        var matches = /Firefox\/(\d+(?:\.\d+){1,2})/.exec(ua);

        return (matches !== null && matches.length > 0) ? matches[1] : '0';
    };

    /**
     * Detect whether the user's Firefox is up to date or outdated. This data is mainly used for security notifications.
     *
     * @param  {Boolean} strict - whether the minor and patch-level version numbers should be compared. Default: true
     * @param  {Boolean} isESR - whether the Firefox update channel is ESR. Default: false
     * @param  {String}  userVer - browser's version number
     * @return {Boolean} result
     */
    Client._isFirefoxUpToDate = function (strict, isESR, userVer) {
        strict = strict === undefined ? true : strict;
        isESR = isESR === undefined ? false : isESR;
        userVer = userVer === undefined ? this._getFirefoxVersion() : userVer;

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
        if (this.FirefoxDetails) {
            callback(this.FirefoxDetails);

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

            // Log the info with GA. Remove this once we have sufficient data
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                'event': 'firefox-details-retrieved',
                'accurate': accurate,
                'version': version,
                'channel': channel,
                'isUpToDate': isUpToDate,
                'isESR': isESR
            });
        };

        // Prepare fallback function in case the API doesn't work
        var userVer = this._getFirefoxVersion();
        var fallback = function () { onRetrieved(false, userVer, 'release'); };

        // If Firefox is old or for Android, call the fallback function immediately because the API is not implemented
        if (parseFloat(userVer) < 35 || window.isFirefoxMobile()) {
            fallback();

            return;
        }

        // Fire the fallback function in .2 seconds
        var timer = window.setTimeout(fallback, 200);

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

    window.Mozilla.Client = Client;

})();
