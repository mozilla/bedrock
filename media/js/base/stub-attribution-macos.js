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
     * Updates all download links on the page with additional query params for
     * stub attribution.
     * @param {Object} data - attribution_code, attribution_sig.
     */
    StubAttributionMacOS.updateTransitionalLinks = function (data) {
        /**
         * If data is missing or the browser does not meet requirements for
         * stub attribution, then do nothing.
         */
        if (Object.getOwnPropertyNames(data).length === 0 || !StubAttributionMacOS.meetsRequirements()) {
            return;
        }

        // if the href of the download link doesn't have any query params, finalParams will default to
        // the value of utmParams. otherwise, finalParams will be a merge of download link params and
        // utmParams.
        var downloadLinks = document.getElementsByClassName('download-link');
        var url;

        // merge the utm params from the current URL with any query params existing on in-page links
        // that point to /download/thanks/.
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
     * Note: data is already URI encoded when returned via the service.
     * @param {String url - URL to append data to.
     * @param {Object} data - attribution_code, attribution_sig.
     * @return {String} url + additional parameters.
     */
    StubAttributionMacOS.appendToDownloadURL = function (url, data) {
        var finalParams = data;
        var linkParams;

        // if the link has a querystring, merge it with the utm_ params in the current URL
        // note: these links currently have no query params, so the code below is
        // essentially future-proofing against what could be a tough to track bug
        if (url.indexOf('?') > 0) {
            // create an object of query params on the current href
            linkParams = window._SearchParams.queryStringToObject(url.split('?')[1]);
            // properties in utmParams will be overwritten by those in linkParams
            // i.e. favor param values in the download link over those found in the querystring of the current URL (if they share a key)
            finalParams = Object.assign(finalParams, linkParams);
        }

        return url.split('?')[0] + '?' + window._SearchParams.objectToQueryString(finalParams);
    };

    /**
     * Determines if requirements for stub attribution to work are satisfied.
     * Stub attribution is only applicable to Windows users who get the stub installer.
     * @return {Boolean}.
     */
    StubAttributionMacOS.meetsRequirements = function () {

        if (typeof window.site === 'undefined') {
            return false;
        }

        if (window.site.platform !== 'osx') {
            return false;
        }

        /*if (Mozilla.dntEnabled()) {
            return false;
        }*/

        return true;
    };

    /**
     * Determines whether to make a request to the stub authentication service.
     */
    StubAttributionMacOS.init = function () {
        var data;

        if (!StubAttributionMacOS.meetsRequirements()) {
            return;
        }

        /**
         * If cookie already exists, update download links on the page,
         * else make a request to the service if within attribution rate.
         */
        var params = new window._SearchParams();
        data = params.utmParamsUnprefixed();
        StubAttributionMacOS.updateTransitionalLinks(data);
    };

    window.Mozilla.StubAttributionMacOS = StubAttributionMacOS;

})(window.Mozilla);
