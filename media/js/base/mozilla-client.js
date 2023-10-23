/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function () {
    'use strict';

    /**
     * Provide information on the user's browsing environment, including the platform and browser details.
     *
     * @namespace
     * @see {@link https://developer.mozilla.org/en-US/docs/Gecko_user_agent_string_reference}
     */
    var Client = {};

    /**
     * Minimum Firefox version supported by FxA.
     * https://mozilla.github.io/ecosystem-platform/docs/fxa-engineering/fxa-dev-process#browser-support
     */
    Client.FxALastSupported = 60;

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

        return (
            /\sFirefox/.test(ua) &&
            !/Mobile|Tablet|Fennec/.test(ua) &&
            !Client._isLikeFirefox(ua)
        );
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
     * Detect whether the user's browser is Gecko-based.
     *
     * @private
     * @param  {String} ua - browser's user agent string, navigator.userAgent is used if not specified
     * @return {Boolean} result
     */
    Client._isLikeFirefox = function (ua) {
        ua = ua || navigator.userAgent;

        return /Iceweasel|IceCat|SeaMonkey|Camino|like Firefox/i.test(ua);
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

        return matches && !Client._isLikeFirefox(ua) ? matches[1] : '0';
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
     * Determine if user version is up to date with latest version from product details.
     *
     * @private
     * @param  {Boolean} strict - if false compare the major version number only.
     * @param  {Array} userVerArr - the user version number.
     * @param  {Array} latestVerArr - the latest version number from product details.
     * @return {Boolean} true if user version number is equal to or greater than product details version.
     */
    Client._compareVersion = function (strict, userVerArr, latestVerArr) {
        var currentUserNumber = 0;
        var currentLatestNumber = 0;
        var isUpToDate = false;

        // Make sure both latest and user array lengths match.
        while (latestVerArr.length < userVerArr.length) {
            latestVerArr.push('0');
        }
        while (userVerArr.length < latestVerArr.length) {
            userVerArr.push('0');
        }

        // Only check the major version in non-strict comparison mode.
        if (!strict) {
            latestVerArr.length = 1;
        }

        // Step through the array from product details and compare to the user array.
        for (var j = 0; j < latestVerArr.length; j++) {
            currentUserNumber = Number(userVerArr[j]);
            currentLatestNumber = Number(latestVerArr[j]);

            if (currentUserNumber < currentLatestNumber) {
                isUpToDate = false;
                break;
            } else if (currentUserNumber > currentLatestNumber) {
                isUpToDate = true;
                break;
            } else {
                isUpToDate = true;
            }
        }

        return isUpToDate;
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

        var html = document.documentElement;

        if (
            !html.getAttribute('data-esr-versions') ||
            !html.getAttribute('data-latest-firefox')
        ) {
            return false;
        }

        var versions = isESR
            ? html.getAttribute('data-esr-versions').split(' ')
            : [html.getAttribute('data-latest-firefox')];
        var userVerArr = userVer.match(/^(\d+(?:\.\d+){1,2})/);

        if (userVerArr && userVerArr.length > 0) {
            userVerArr = userVerArr[1].split('.');
        } else {
            // if there's no version in the UA string, assume out of date (issue 10582)
            return false;
        }

        var isUpToDate = false;

        // Sort product details version so we compare the newer version first
        versions.sort(function (a, b) {
            return parseFloat(a) < parseFloat(b);
        });

        // Compare each latest version in product details to the user version.
        for (var i = 0; i < versions.length; i++) {
            var latestVerArr = versions[i].split('.');

            isUpToDate = Client._compareVersion(
                strict,
                userVerArr,
                latestVerArr
            );

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

        var callbackID = Math.random()
            .toString(36)
            .replace(/[^a-z]+/g, '');

        var listener = function (event) {
            if (
                !event.detail ||
                !event.detail.data ||
                event.detail.callbackID !== callbackID
            ) {
                return;
            }

            window.clearTimeout(timer);
            onRetrieved(
                true,
                event.detail.data.version,
                event.detail.data.defaultUpdateChannel,
                event.detail.data.distribution
            );
        };

        var onRetrieved = function (accurate, version, channel, distribution) {
            document.removeEventListener('mozUITourResponse', listener, false);

            var isESR = channel === 'esr';
            var isUpToDate = Client._isFirefoxUpToDate(
                accurate,
                accurate ? isESR : false,
                version
            );
            var details = (Client.FirefoxDetails = {
                accurate: accurate,
                version: version,
                channel: channel,
                distribution: distribution,
                isUpToDate: isUpToDate,
                isESR: isESR
            });

            callback(details);
        };

        // Prepare fallback function in case the API doesn't work
        var userVer = Client._getFirefoxVersion();
        var fallback = function () {
            onRetrieved(false, userVer, 'release', undefined);
        };

        // If Firefox is old or for Android, call the fallback function immediately because the API is not implemented
        if (parseFloat(userVer) < 35 || Client._isFirefoxAndroid()) {
            fallback();

            return;
        }

        // Fire the fallback function in .4 seconds
        var timer = window.setTimeout(fallback, 400);

        // Trigger the API
        document.addEventListener('mozUITourResponse', listener, false);
        document.dispatchEvent(
            new CustomEvent('mozUITour', {
                bubbles: true,
                detail: {
                    action: 'getConfiguration',
                    data: { configuration: 'appinfo', callbackID: callbackID }
                }
            })
        );
    };

    /**
     * Use the async mozUITour API of Firefox to retrieve the user's FxA info. See
     * http://bedrock.readthedocs.org/en/latest/uitour.html for details.
     *
     * The various states here are... complicated
     * This is the intention:
     *     - firefox: true if Firefox
     *     - legacy: true if older than FxALastSupported
     *     - mobile: false | android | ios
     *     - setup: true if Fx >= 29 and logged into *Sync*.
     *              true if Fx >= 74 and logged into *FxA*.
     *     - browserServices.sync
     *              setup: logged into Sync.
     *              desktopDevices: number of desktop devices synced.
     *              mobileDevices: number of mobile devices synced.
     *              totalDevices: number of total devices synced.
     * Notes:
     * - Fx < 50 has FxA and UITour support but the API does not return device counts
     * - Fx < FxALastSupported accounts.firefox.com does not work
     *     - FxALastSupported is supplied by the FxA team
     *     - these versions are still capable of logging in through the browser
     *     - differentiated because we generally do not give these versions the FxA calls to action (eg. "Create an Account")
     * - Fx < 29 the mozUITour API is not available, though the user may still be logged in
     * - If you're curious, "sync" began with Fx 4.
     *
     * @param  {Function} callback - callback function to be executed with the FxA details
     * @return {None}
     */

    Client.getFxaDetails = function (callback) {
        // Fire the callback function immediately if FxaDetails are already defined
        if (Client.FxaDetails) {
            callback(Client.FxaDetails);
            return;
        }

        var request = {
            name: null,
            callback: null
        };

        // Set up the object with default values of false
        var details = {
            firefox: false,
            legacy: false,
            mobile: false,
            setup: false,
            browserServices: {
                sync: {
                    setup: false,
                    desktopDevices: false,
                    mobileDevices: false,
                    totalDevices: false
                }
            }
        };

        // Override object values as we get more information
        if (Client._isFirefoxAndroid()) {
            details.firefox = true;
            details.mobile = 'android';
            returnFxaDetails();
            return;
        } else if (Client._isFirefoxiOS()) {
            details.firefox = true;
            details.mobile = 'ios';
            returnFxaDetails();
            return;
        } else if (Client._isFirefoxDesktop()) {
            details.firefox = true;
            var userVer = parseFloat(Client._getFirefoxVersion());

            if (userVer < 29) {
                // UITour not supported
                details.legacy = true;
                returnFxaDetails();
                return;
            } else {
                // UITour supported
                // still note if it's older than accounts.firefox.com supports
                if (userVer < Client.FxALastSupported) {
                    details.legacy = true;
                }

                // callbackID to make sure we're responding to our request
                var callbackID = Math.random()
                    .toString(36)
                    .replace(/[^a-z]+/g, '');

                // UITour API response event handler for 'sync', checks for callbackID
                var listenerSync = function (event) {
                    if (
                        !event.detail ||
                        !event.detail.data ||
                        event.detail.callbackID !== callbackID
                    ) {
                        return;
                    }

                    var config = event.detail.data;

                    // Clear the timeout and remove the event listener.
                    window.clearTimeout(timer);
                    document.removeEventListener(
                        'mozUITourResponse',
                        listenerSync,
                        false
                    );

                    /**
                     * Account signed-in state
                     * Assume being signed-in to Sync equals being signed in to an account.
                     */
                    details.setup = config.setup;

                    /**
                     * Browser services
                     * Device counts are only available in Fx50+, fallback 'unknown' if not detectable
                     */
                    details.browserServices.sync = {
                        setup: config.setup,
                        desktopDevices: Object.prototype.hasOwnProperty.call(
                            config,
                            'desktopDevices'
                        )
                            ? config.desktopDevices
                            : 'unknown',
                        mobileDevices: Object.prototype.hasOwnProperty.call(
                            config,
                            'mobileDevices'
                        )
                            ? config.mobileDevices
                            : 'unknown',
                        totalDevices: Object.prototype.hasOwnProperty.call(
                            config,
                            'totalDevices'
                        )
                            ? config.totalDevices
                            : 'unknown'
                    };

                    returnFxaDetails();
                };

                // UITour API response event handler for 'fxa', checks for callbackID
                var listenerFxA = function (event) {
                    if (
                        !event.detail ||
                        !event.detail.data ||
                        event.detail.callbackID !== callbackID
                    ) {
                        return;
                    }

                    var config = event.detail.data;

                    // Clear the timeout and remove the event listener.
                    window.clearTimeout(timer);
                    document.removeEventListener(
                        'mozUITourResponse',
                        listenerFxA,
                        false
                    );

                    // Account signed-in state
                    details.setup = config.setup;

                    // Browser services (Sync is the only service here currently).
                    details.browserServices = config.browserServices;

                    returnFxaDetails();
                };

                // Query Mozilla account signed In stage via 'fxa' config.
                if (userVer >= 74) {
                    request.name = 'fxa';
                    request.callback = listenerFxA;
                }
                // UITour supported but client must use legacy 'sync' configuration call.
                else {
                    request.name = 'sync';
                    request.callback = listenerSync;
                }

                // Trigger the UITour API and start listening for the reponse
                document.addEventListener(
                    'mozUITourResponse',
                    request.callback,
                    false
                );
                document.dispatchEvent(
                    new CustomEvent('mozUITour', {
                        bubbles: true,
                        detail: {
                            action: 'getConfiguration',
                            data: {
                                configuration: request.name,
                                callbackID: callbackID
                            }
                        }
                    })
                );
            }
        }

        function returnFxaDetails() {
            window.clearTimeout(timer);
            Client.FxaDetails = details;
            callback(details);
        }

        // Fire the fallback function in .4 seconds
        var timer = window.setTimeout(returnFxaDetails, 400);
    };

    // Append static properties for faster access
    Client.isFirefox = Client._isFirefox();
    Client.isFirefoxDesktop = Client._isFirefoxDesktop();
    Client.isFirefoxAndroid = Client._isFirefoxAndroid();
    Client.isFirefoxiOS = Client._isFirefoxiOS();
    Client.isLikeFirefox = Client._isLikeFirefox();
    Client.FirefoxVersion = Client._getFirefoxVersion();
    Client.FirefoxMajorVersion = Client._getFirefoxMajorVersion();

    // Append platform info as well for convenience
    Client.platform = window.site.platform;
    Client.isMobile = /^(android|ios)$/.test(Client.platform);
    Client.isDesktop = !Client.isMobile;

    window.Mozilla.Client = Client;
})();
