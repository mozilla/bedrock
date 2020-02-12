/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

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

    /**
     * Experiment name and variation globals. These values can be set directly by a
     * page's JS instead of relying on supplied URL query parameters.
     */
    StubAttribution.experimentName;
    StubAttribution.experimentVariation;

    /**
     * Determines if session falls within the predefined stub attribution sample rate.
     * @return {Boolean}.
     */
    StubAttribution.withinAttributionRate = function() {
        return (Math.random() < StubAttribution.getAttributionRate()) ? true : false;
    };

    /**
     * Returns stub attribution value used for rate limiting.
     * @return {Number} float between 0 and 1.
     */
    StubAttribution.getAttributionRate = function() {
        var rate = $('html').attr('data-stub-attribution-rate');
        return isNaN(rate) ? 0 : Math.min(Math.max(parseFloat(rate), 0), 1);
    };

    /**
     * Returns true if both cookies exist.
     * @return {Boolean} data.
     */
    StubAttribution.hasCookie = function() {
        return Mozilla.Cookies.hasItem(StubAttribution.COOKIE_CODE_ID) && Mozilla.Cookies.hasItem(StubAttribution.COOKIE_SIGNATURE_ID);
    };

    /**
     * Stores a cookie with stub attribution data values.
     * @param {Object} data - attribution_code, attribution_sig.
     */
    StubAttribution.setCookie = function(data) {

        if (!data.attribution_code || !data.attribution_sig) {
            return;
        }

        // set cookie to expire in 24 hours
        var date = new Date();
        date.setTime(date.getTime() + (1 * 24 * 60 * 60 * 1000));
        var expires = date.toUTCString();

        Mozilla.Cookies.setItem(StubAttribution.COOKIE_CODE_ID, data.attribution_code, expires, '/');
        Mozilla.Cookies.setItem(StubAttribution.COOKIE_SIGNATURE_ID, data.attribution_sig, expires, '/');
    };

    /**
     * Gets stub attribution data from cookie.
     * @return {Object} - attribution_code, attribution_sig.
     */
    StubAttribution.getCookie = function() {
        return {
            /* eslint-disable camelcase */
            attribution_code: Mozilla.Cookies.getItem(StubAttribution.COOKIE_CODE_ID),
            attribution_sig: Mozilla.Cookies.getItem(StubAttribution.COOKIE_SIGNATURE_ID)
            /* eslint-enable camelcase */
        };
    };

    /**
     * Updates all download links on the page with additional query params for
     * stub attribution.
     * @param {Object} data - attribution_code, attribution_sig.
     */
    StubAttribution.updateBouncerLinks = function(data) {
        /**
         * If data is missing or the browser does not meet requirements for
         * stub attribution, then do nothing.
         */
        if (!data.attribution_code || !data.attribution_sig || !StubAttribution.meetsRequirements()) {
            return;
        }

        // target download buttons and other-platforms modal links.
        $('.download-list .download-link, .download-platform-list .download-link').each(function() {
            var version;
            // If this is a transitional download link do nothing.
            if (this.href && this.href.indexOf('/firefox/download/thanks/') === -1) {

                version = $(this).data('downloadVersion');
                // Currently only Windows 32bit uses the stub installer, but this could
                // easily change in the future so we're also adding params to 64 bit builds.
                if (version && (version === 'win' || version === 'win64')) {
                    this.href = Mozilla.StubAttribution.appendToDownloadURL(this.href, data);
                }
            }
        });
    };

    /**
     * Appends stub attribution data as URL parameters.
     * Note: data is already URI encoded when returned via the service.
     * @param {String} url - URL to append data to.
     * @param {Object} data - attribution_code, attribution_sig.
     * @return {String} url + additional parameters.
     */
    StubAttribution.appendToDownloadURL = function(url, data) {

        if (!data.attribution_code || !data.attribution_sig) {
            return url;
        }

        // append stub attribution query params.
        $.each(data, function(key, val) {
            if (key === 'attribution_code' || key === 'attribution_sig') {
                url += (url.indexOf('?') > -1 ? '&' : '?') + key + '=' + val;
            }
        });

        return url;
    };

    /**
     * Handles XHR request from `stub_attribution_code` service.
     * @param {Object} data - attribution_code, attribution_sig.
     */
    StubAttribution.onRequestSuccess = function(data) {
        if (data.attribution_code && data.attribution_sig) {
            // Update download links on the current page.
            StubAttribution.updateBouncerLinks(data);
            // Store attribution data in a cookie should the user navigate.
            StubAttribution.setCookie(data);
        }
    };

    /**
     * AJAX request to bedrock service to authenticate stub attribution request.
     * @param {Object} data - utm params and referrer.
     */
    StubAttribution.requestAuthentication = function(data) {
        var SERVICE_URL = window.location.protocol + '//' + window.location.host + '/en-US/firefox/stub_attribution_code/';
        $.get(SERVICE_URL, data).done(StubAttribution.onRequestSuccess);
    };

    /**
     * Returns a browser name based on coarse UA string detection for only major browsers.
     * Other browsers (or modified UAs) that have strings that look like one of the top default user agent strings are treated as false positives.
     * @param {String} ua - Optional user agent string to facilitate testing.
     * @returns {String} - Browser name.
     */
    StubAttribution.getUserAgent = function(ua) {
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
     * Gets utm parameters and referrer information from the web page if they exist.
     * @param {String} ref - Optional referrer to facilitate testing.
     * @return {Object} - Stub attribution data object.
     */
    StubAttribution.getAttributionData = function(ref) {
        var params = new window._SearchParams();
        var utms = params.utmParams();
        var experiment = params.get('experiment') || StubAttribution.experimentName;
        var variation = params.get('variation') || StubAttribution.experimentVariation;
        var referrer = typeof ref !== 'undefined' ? ref : document.referrer;
        var ua = StubAttribution.getUserAgent();

        /* eslint-disable camelcase */
        var data = {
            utm_source: utms.utm_source,
            utm_medium: utms.utm_medium,
            utm_campaign: utms.utm_campaign,
            utm_content: utms.utm_content,
            referrer: referrer,
            ua : ua,
            experiment: experiment,
            variation: variation
        };
        /* eslint-enable camelcase */

        return data;
    };

    /**
     * Determine if the current page is scene2 of /firefox/new/.
     * This is needed as scene2 auto-initiates the download. There is little point
     * trying to make an XHR request here before the download begins, and we don't
     * want to make the request a dependency on the download starting.
     * @return {Boolean}.
     */
    StubAttribution.isFirefoxNewScene2 = function(location) {
        location = typeof location !== 'undefined' ? location : window.location.href;
        return location.indexOf('/firefox/download/thanks/') > -1;
    };

    /**
     * Determines if requirements for stub attribution to work are satisfied.
     * Stub attribution is only applicable to Windows users who get the stub installer.
     * @return {Boolean}.
     */
    StubAttribution.meetsRequirements = function() {

        if (typeof window.site === 'undefined' || typeof Mozilla.Cookies === 'undefined') {
            return false;
        }

        if (!Mozilla.Cookies.enabled()) {
            return false;
        }

        if (window.site.platform !== 'windows') {
            return false;
        }

        if (Mozilla.dntEnabled()) {
            return false;
        }

        return true;
    };

    /**
     * Determines whether to make a request to the stub authentication service.
     */
    StubAttribution.init = function() {
        var data = {};

        if (!StubAttribution.meetsRequirements()) {
            return;
        }

        /**
         * If cookie already exists, update download links on the page,
         * else make a request to the service if within attribution rate.
         */
        if (StubAttribution.hasCookie()) {

            data = StubAttribution.getCookie();
            StubAttribution.updateBouncerLinks(data);

        // As long as the user is not already on scene2 of the main download page,
        // make the XHR request to the stub authentication service.
        } else if (!StubAttribution.isFirefoxNewScene2()) {

            data = StubAttribution.getAttributionData();

            if (data && StubAttribution.withinAttributionRate()) {
                StubAttribution.requestAuthentication(data);
            }
        }
    };

    window.Mozilla.StubAttribution = StubAttribution;
})();
