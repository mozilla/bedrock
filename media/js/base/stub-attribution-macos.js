/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function (Mozilla) {
    'use strict';

    var StubAttributionMacOS = {};

    /**
     * Updates all download links pointing to /firefox/download/thanks/ on the page with
     * additional query params for stub attribution.
     * @param {Object} data - campaign, medium, source, content
     */
    StubAttributionMacOS.updateTransitionalLinks = function (data) {
        /**
         * If data is missing or the browser does not meet requirements for
         * stub attribution, then do nothing.
         */
        if (data === null || !StubAttributionMacOS.meetsRequirements()) {
            return;
        }

        var downloadLinks = document.getElementsByClassName('download-link');
        var url;

        for (var i = 0; i < downloadLinks.length; i++) {
            url = downloadLinks[i].href;

            // only alter links going to /firefox/download/thanks/
            if (url.indexOf('download/thanks/') > 0) {
                downloadLinks[i].href = Mozilla.StubAttributionMacOS.appendToDownloadURL(url, data);
            }
        }
    };

    /**
     * Appends stub attribution data as URL parameters.
     * @param {String} url - URL to append data to.
     * @param {Object} data - campaign, medium, source, content
     * @return {String} url + additional parameters.
     */
    StubAttributionMacOS.appendToDownloadURL = function (url, data) {
        var finalParams = data;
        var linkParams;

        // if the link has a querystring, merge it with the utm_ params in the current
        // URL
        // note: these links currently have no query params, so the code below is
        // essentially future-proofing against what could be a tough to track bug
        if (url.indexOf('?') > 0) {
            // create an object of query params on the current href
            linkParams = window._SearchParams.queryStringToObject(url.split('?')[1]);
            // properties in utmParams will be overwritten by those in linkParams
            // i.e. favor param values in the download link over those found in the
            // querystring of the current URL (if they share a key)
            finalParams = Object.assign(finalParams, linkParams);
        }

        return url.split('?')[0] + '?' + window._SearchParams.objectToQueryString(finalParams);
    };

    /**
     * Gets utm parameters from the current URL and ensures they meet the requirements
     * @return {Object} - Stub attribution data object containing four keys or null.
     */
    StubAttributionMacOS.getAttributionData = function () {
        var params = new window._SearchParams().utmParams();
        var finalParams = {};

        if (params.hasOwnProperty('utm_campaign') && params['utm_campaign'] === 'non-fx-button') {
            finalParams['campaign'] = 'non-fx-button';
        }

        if (params.hasOwnProperty('utm_medium') && params['utm_medium'] === 'referral') {
            finalParams['medium'] = 'referral';
        }

        if (params.hasOwnProperty('utm_source') && params['utm_source'] === 'addons.mozilla.org') {
            finalParams['source'] = 'addons.mozilla.org';
        }

        // utm_content should *always* start with "rta%3A", followed by alphanumeric characters
        if (params.hasOwnProperty('utm_content') && (/^rta%3A[a-zA-Z0-9_\-]+$/).test(params['utm_content'])) {
            // this value is already URI encoded, so we need to decode here as
            // it will get re-encoded in _SearchParams.objectToQueryString
            finalParams['content'] = decodeURIComponent(params['utm_content']);
        }

        return Object.getOwnPropertyNames(finalParams).length === 4 ? finalParams : null;
    };

    /**
     * Determines if requirements for stub attribution to work are satisfied.
     * Stub attribution is only applicable to macOS users with specific utm_ values in
     * the querystring.
     * @return {Boolean}.
     */
    StubAttributionMacOS.meetsRequirements = function () {

        if (typeof window.site === 'undefined') {
            return false;
        }

        if (window.site.platform !== 'osx') {
            return false;
        }

        if (Mozilla.dntEnabled()) {
            return false;
        }

        return true;
    };

    StubAttributionMacOS.init = function () {
        var data;

        if (!StubAttributionMacOS.meetsRequirements()) {
            return;
        }

        data = StubAttributionMacOS.getAttributionData();
        StubAttributionMacOS.updateTransitionalLinks(data);
    };

    window.Mozilla.StubAttributionMacOS = StubAttributionMacOS;

})(window.Mozilla);
