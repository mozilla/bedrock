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

    window.dataLayer = window.dataLayer || [];

    /**
     * Constructs attribution data based on utm parameters and referrer information
     * for relay to the Firefox stub installer. Data is first signed and encoded via
     * an XHR request to the `stub_attribution_code` service, before being appended
     * to Bouncer download URLs as query parameters. Data returned from the service
     * is also stored in a cookie to save multiple requests when navigating
     * pages. Bug https://bugzilla.mozilla.org/show_bug.cgi?id=1279291
     */
    var StubAttribution = {};

    StubAttribution.COOKIE_CODE_ID = 'moz-stub-attribution-code';
    StubAttribution.COOKIE_SIGNATURE_ID = 'moz-stub-attribution-sig';
    StubAttribution.DLSOURCE = 'mozorg';

    /**
     * Experiment name and variation globals. These values can be set directly by a
     * page's JS instead of relying on supplied URL query parameters.
     */
    StubAttribution.experimentName;
    StubAttribution.experimentVariation;

    /**
     * Custom event handler callback globals. These can be defined as functions when
     * calling StubAttribution.init();
     */
    StubAttribution.successCallback;
    StubAttribution.timeoutCallback;
    StubAttribution.requestComplete = false;

    /**
     * Determines if session falls within the predefined stub attribution sample rate.
     * @return {Boolean}.
     */
    StubAttribution.withinAttributionRate = function () {
        return Math.random() < StubAttribution.getAttributionRate()
            ? true
            : false;
    };

    /**
     * Returns stub attribution value used for rate limiting.
     * @return {Number} float between 0 and 1.
     */
    StubAttribution.getAttributionRate = function () {
        var rate = document
            .getElementsByTagName('html')[0]
            .getAttribute('data-stub-attribution-rate');
        return isNaN(rate) || !rate
            ? 0
            : Math.min(Math.max(parseFloat(rate), 0), 1);
    };

    /**
     * Returns true if both cookies exist.
     * @return {Boolean} data.
     */
    StubAttribution.hasCookie = function () {
        return (
            Mozilla.Cookies.hasItem(StubAttribution.COOKIE_CODE_ID) &&
            Mozilla.Cookies.hasItem(StubAttribution.COOKIE_SIGNATURE_ID)
        );
    };

    /**
     * Stores a cookie with stub attribution data values.
     * @param {Object} data - attribution_code, attribution_sig.
     */
    StubAttribution.setCookie = function (data) {
        if (!data.attribution_code || !data.attribution_sig) {
            return;
        }

        // set cookie to expire in 24 hours
        var date = new Date();
        date.setTime(date.getTime() + 1 * 24 * 60 * 60 * 1000);
        var expires = date.toUTCString();

        Mozilla.Cookies.setItem(
            StubAttribution.COOKIE_CODE_ID,
            data.attribution_code,
            expires,
            '/',
            undefined,
            false,
            'lax'
        );
        Mozilla.Cookies.setItem(
            StubAttribution.COOKIE_SIGNATURE_ID,
            data.attribution_sig,
            expires,
            '/',
            undefined,
            false,
            'lax'
        );
    };

    /**
     * Gets stub attribution data from cookie.
     * @return {Object} - attribution_code, attribution_sig.
     */
    StubAttribution.getCookie = function () {
        return {
            /* eslint-disable camelcase */
            attribution_code: Mozilla.Cookies.getItem(
                StubAttribution.COOKIE_CODE_ID
            ),
            attribution_sig: Mozilla.Cookies.getItem(
                StubAttribution.COOKIE_SIGNATURE_ID
            )
            /* eslint-enable camelcase */
        };
    };

    /**
     * Updates all download links on the page with additional query params for
     * stub attribution.
     * @param {Object} data - attribution_code, attribution_sig.
     */
    StubAttribution.updateBouncerLinks = function (data) {
        /**
         * If data is missing or the browser does not meet requirements for
         * stub attribution, then do nothing.
         */
        if (
            !data.attribution_code ||
            !data.attribution_sig ||
            !StubAttribution.meetsRequirements()
        ) {
            return;
        }

        // target download buttons and other-platforms modal links.
        var downloadLinks = document.querySelectorAll(
            '.download-list .download-link, .c-button-download-thanks .download-link, .download-platform-list .download-link, .firefox-platform-button .download-link'
        );

        for (var i = 0; i < downloadLinks.length; i++) {
            var link = downloadLinks[i];
            var version;
            var directLink;
            // Append stub attribution data to direct download links.
            if (
                (link.href &&
                    (link.href.indexOf('https://download.mozilla.org') !== -1 ||
                        link.href.indexOf(
                            'https://bouncer-bouncer.stage.mozaws.net/'
                        ) !== -1)) ||
                link.href.indexOf(
                    'https://dev.bouncer.nonprod.webservices.mozgcp.net'
                ) !== -1
            ) {
                version = link.getAttribute('data-download-version');

                // Append attribution params to Windows links.
                if (version && /win/.test(version)) {
                    link.href = Mozilla.StubAttribution.appendToDownloadURL(
                        link.href,
                        data
                    );
                }
                // Append attribution params to macOS links (excluding ESR for now).
                if (
                    version &&
                    /osx/.test(version) &&
                    !/product=firefox-esr/.test(link.href)
                ) {
                    link.href = Mozilla.StubAttribution.appendToDownloadURL(
                        link.href,
                        data
                    );
                }
            } else if (
                link.href &&
                link.href.indexOf('/firefox/download/thanks/') !== -1
            ) {
                // Append stub data to direct-link data attributes on transitional links for old IE browsers (Issue #9350)
                directLink = link.getAttribute('data-direct-link');

                if (directLink) {
                    link.setAttribute(
                        'data-direct-link',
                        Mozilla.StubAttribution.appendToDownloadURL(
                            directLink,
                            data
                        )
                    );
                }
            }
        }
    };

    /**
     * Appends stub attribution data as URL parameters.
     * Note: data is already URI encoded when returned via the service.
     * @param {String} url - URL to append data to.
     * @param {Object} data - attribution_code, attribution_sig.
     * @return {String} url + additional parameters.
     */
    StubAttribution.appendToDownloadURL = function (url, data) {
        if (!data.attribution_code || !data.attribution_sig) {
            return url;
        }

        // append stub attribution query params.
        for (var key in data) {
            if (Object.prototype.hasOwnProperty.call(data, key)) {
                if (key === 'attribution_code' || key === 'attribution_sig') {
                    url +=
                        (url.indexOf('?') > -1 ? '&' : '?') +
                        key +
                        '=' +
                        data[key];
                }
            }
        }

        return url;
    };

    /**
     * Handles XHR request from `stub_attribution_code` service.
     * @param {Object} data - attribution_code, attribution_sig.
     */
    StubAttribution.onRequestSuccess = function (data) {
        if (
            data.attribution_code &&
            data.attribution_sig &&
            !StubAttribution.requestComplete
        ) {
            // Update download links on the current page.
            StubAttribution.updateBouncerLinks(data);
            // Store attribution data in a cookie should the user navigate.
            StubAttribution.setCookie(data);

            StubAttribution.requestComplete = true;

            if (typeof StubAttribution.successCallback === 'function') {
                StubAttribution.successCallback();
            }
        }
    };

    StubAttribution.onRequestTimeout = function () {
        if (!StubAttribution.requestComplete) {
            StubAttribution.requestComplete = true;

            if (typeof StubAttribution.timeoutCallback === 'function') {
                StubAttribution.timeoutCallback();
            }
        }
    };

    /**
     * AJAX request to bedrock service to authenticate stub attribution request.
     * @param {Object} data - utm params and referrer.
     */
    StubAttribution.requestAuthentication = function (data) {
        var SERVICE_URL =
            window.location.protocol +
            '//' +
            window.location.host +
            '/en-US/firefox/stub_attribution_code/';
        var xhr = new window.XMLHttpRequest();
        var timeoutValue = 10000;
        var timeout = setTimeout(
            StubAttribution.onRequestTimeout,
            timeoutValue
        );

        xhr.open(
            'GET',
            SERVICE_URL + '?' + window._SearchParams.objectToQueryString(data)
        );
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        // use readystate change over onload for IE8 support.
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                var status = xhr.status;
                if (status && status >= 200 && status < 400) {
                    try {
                        var data = JSON.parse(xhr.responseText);
                        clearTimeout(timeout);
                        StubAttribution.onRequestSuccess(data);
                    } catch (e) {
                        // something went wrong, fallback to the timeout handler.
                        StubAttribution.onRequestTimeout();
                    }
                }
            }
        };

        // must come after open call above for IE 10 & 11
        xhr.timeout = timeoutValue;
        xhr.send();
    };

    /**
     * Returns a browser name based on coarse UA string detection for only major browsers.
     * Other browsers (or modified UAs) that have strings that look like one of the top default user agent strings are treated as false positives.
     * @param {String} ua - Optional user agent string to facilitate testing.
     * @returns {String} - Browser name.
     */
    StubAttribution.getUserAgent = function (ua) {
        ua = typeof ua !== 'undefined' ? ua : navigator.userAgent;

        if (/MSIE|Trident/i.test(ua)) {
            return 'ie';
        }

        if (/Edg|Edge/i.test(ua)) {
            return 'edge';
        }

        if (/Firefox/.test(ua)) {
            return 'firefox';
        }

        if (/Chrome/.test(ua)) {
            return 'chrome';
        }

        return 'other';
    };

    /**
     * Gets the UA client ID from the GA object.
     * @returns {String} client ID.
     */
    StubAttribution.getUAClientID = function () {
        try {
            var clientID = window.ga.getAll()[0].get('clientId');

            if (clientID && typeof clientID === 'string' && clientID !== '') {
                return clientID;
            }
            return null;
        } catch (e) {
            return null;
        }
    };

    /**
     * Attempts to retrieve the GA4 client from the dataLayer
     * The GTAG GET API tag will write it to the dataLayer once GTM has loaded it
     * https://www.simoahava.com/gtmtips/write-client-id-other-gtag-fields-datalayer/
     */
    StubAttribution.getGtagClientID = function (dataLayer) {
        // need to pass in dataLayer for testing purposes, use global dataLayer if it's not passed
        dataLayer =
            typeof dataLayer !== 'undefined' ? dataLayer : window.dataLayer;

        var clientID = null;

        function _findAPI(obj) {
            for (var key in obj) {
                if (
                    typeof obj[key] === 'object' &&
                    Object.prototype.hasOwnProperty.call(obj, key)
                ) {
                    if (key === 'gtagApiResult') {
                        if (typeof obj[key].client_id === 'string') {
                            clientID = obj[key].client_id;
                        } else {
                            return clientID;
                        }
                        break;
                    } else {
                        _findAPI(obj[key]);
                    }
                }
            }
        }

        try {
            if (typeof dataLayer === 'object') {
                dataLayer.forEach(function (layer) {
                    _findAPI(layer);
                });
            }
        } catch (e) {
            // GA4
            window.dataLayer.push({
                event: 'log',
                label: 'getGtagClientID error: ' + e
            });
            return null;
        }

        return clientID;
    };

    /**
     * Returns a random identifier that we use to associate a
     * visitor's website GA data with their Telemetry attribution
     * data. This identifier is sent as a non-interaction event
     * to GA, and also to the stub attribution service as session_id.
     * @returns {String} session ID.
     */
    StubAttribution.createSessionID = function () {
        return Math.floor(1000000000 + Math.random() * 9000000000).toString();
    };

    /**
     * A crude check to see if Google Analytics has loaded.
     * @param {Function} callback
     */
    StubAttribution.waitForGoogleAnalyticsThen = function (callback) {
        var timeout;
        var pollRetry = 0;
        var interval = 100;
        var limit = 20; // (100 x 20) / 1000 = 2 seconds

        // Tries to get client IDs at a set interval
        function _checkGA() {
            clearTimeout(timeout);
            var clientIDUA = StubAttribution.getUAClientID();
            var clientIDGA4 = StubAttribution.getGtagClientID();

            if (clientIDUA && clientIDGA4) {
                callback(true);
            } else {
                if (pollRetry <= limit) {
                    pollRetry += 1;
                    timeout = window.setTimeout(_checkGA, interval);
                } else {
                    if (clientIDUA || clientIDGA4) {
                        callback(true);
                    } else {
                        callback(false);
                    }
                }
            }
        }

        _checkGA();
    };

    /**
     * Gets utm parameters and referrer information from the web page if they exist.
     * @param {String} ref - Optional referrer to facilitate testing.
     * @param {Boolean} omitNonEssentialFields - Optional flag to omit fields that are nonEssential for RTAMO.
     * @return {Object} - Stub attribution data object.
     */
    StubAttribution.getAttributionData = function (
        ref,
        omitNonEssentialFields
    ) {
        var params = new window._SearchParams();
        var utms = params.utmParams();
        var experiment = omitNonEssentialFields
            ? null
            : params.get('experiment') || StubAttribution.experimentName;
        var variation = omitNonEssentialFields
            ? null
            : params.get('variation') || StubAttribution.experimentVariation;
        var referrer = typeof ref === 'string' ? ref : document.referrer;
        var ua = omitNonEssentialFields
            ? 'other'
            : StubAttribution.getUserAgent();
        var clientIDUA = omitNonEssentialFields
            ? null
            : StubAttribution.getUAClientID();
        var clientIDGA4 = omitNonEssentialFields
            ? null
            : StubAttribution.getGtagClientID();

        /* eslint-disable camelcase */
        var data = {
            utm_source: utms.utm_source,
            utm_medium: utms.utm_medium,
            utm_campaign: utms.utm_campaign,
            utm_content: utms.utm_content,
            referrer: referrer,
            ua: ua,
            experiment: experiment,
            variation: variation,
            client_id: clientIDUA,
            client_id_ga4: clientIDGA4,
            session_id:
                clientIDUA || clientIDGA4
                    ? StubAttribution.createSessionID()
                    : null,
            dlsource: StubAttribution.DLSOURCE
        };
        /* eslint-enable camelcase */

        // Remove any undefined values.
        for (var key in data) {
            if (Object.prototype.hasOwnProperty.call(data, key)) {
                if (typeof data[key] === 'undefined' || data[key] === null) {
                    delete data[key];
                }
            }
        }

        return data;
    };

    StubAttribution.hasValidData = function (data) {
        if (
            typeof data.utm_content === 'string' &&
            typeof data.referrer === 'string'
        ) {
            var content = data.utm_content;
            var charLimit = 150;

            // If utm_content is unusually long, return false early.
            if (content.length > charLimit) {
                return false;
            }

            // Attribution data can be double encoded
            while (content.indexOf('%') !== -1) {
                try {
                    var result = decodeURIComponent(content);
                    if (result === content) {
                        break;
                    }
                    content = result;
                } catch (e) {
                    break;
                }
            }

            // If RTAMO data does not originate from AMO, drop attribution (Issues 10337, 10524).
            if (
                /^rta:/.test(content) &&
                data.referrer.indexOf('https://addons.mozilla.org') === -1
            ) {
                return false;
            }
        }
        return true;
    };

    /**
     * Determine if the current page is /download/thanks
     * This is needed as /thanks auto-initiates the download. There is little point
     * trying to make an XHR request here before the download begins, and we don't
     * want to make the request a dependency on the download starting.
     * @return {Boolean}.
     */
    StubAttribution.isFirefoxDownloadThanks = function (location) {
        location =
            typeof location !== 'undefined' ? location : window.location.href;
        return location.indexOf('/firefox/download/thanks/') > -1;
    };

    /**
     * Determines if requirements for stub attribution to work are satisfied.
     * Stub attribution is only applicable to Windows/macOS users on desktop.
     * @return {Boolean}.
     */
    StubAttribution.meetsRequirements = function () {
        if (
            typeof window.site === 'undefined' ||
            typeof Mozilla.Cookies === 'undefined' ||
            typeof window._SearchParams === 'undefined'
        ) {
            return false;
        }

        if (!Mozilla.Cookies.enabled()) {
            return false;
        }

        if (!/windows|osx/i.test(window.site.platform)) {
            return false;
        }

        return true;
    };

    /**
     * Determines whether to make a request to the stub authentication service.
     */
    StubAttribution.init = function (successCallback, timeoutCallback) {
        var data = {};

        if (!StubAttribution.meetsRequirements()) {
            return;
        }

        // Support custom callback functions for success and timeout.
        if (typeof successCallback === 'function') {
            StubAttribution.successCallback = successCallback;
        }

        if (typeof timeoutCallback === 'function') {
            StubAttribution.timeoutCallback = timeoutCallback;
        }

        /**
         * If cookie already exists, update download links on the page,
         * else make a request to the service if within attribution rate.
         */
        if (StubAttribution.hasCookie()) {
            data = StubAttribution.getCookie();
            StubAttribution.updateBouncerLinks(data);

            // As long as the user is not already on the automatic download page,
            // make the XHR request to the stub authentication service.
        } else if (!StubAttribution.isFirefoxDownloadThanks()) {
            // Wait for UA & GA4 to load and return client IDs
            StubAttribution.waitForGoogleAnalyticsThen(function () {
                // get attribution data
                data = StubAttribution.getAttributionData();

                if (
                    data &&
                    StubAttribution.withinAttributionRate() &&
                    StubAttribution.hasValidData(data)
                ) {
                    // if data is valid and we are in sample rate:
                    // request authentication from stub attribution service
                    StubAttribution.requestAuthentication(data);

                    // Send the session ID to UA and GA4
                    if (data.client_id) {
                        // UA
                        window.dataLayer.push({
                            event: 'stub-session-id',
                            eLabel: data.session_id
                        });
                    }
                    if (data.client_id_ga4) {
                        // GA4
                        window.dataLayer.push({
                            event: 'stub_session_set',
                            id: data.session_id
                        });
                    }
                }
            });
        }
    };

    window.Mozilla.StubAttribution = StubAttribution;
})();
