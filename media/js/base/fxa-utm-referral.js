/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';

    var UtmUrl = {};

    /**
     * Fetch and validate utm params from the page URL for FxA referral.
     * https://mozilla.github.io/application-services/docs/accounts/metrics.html#descriptions-of-metrics-related-query-parameters
     * @returns {Object} if one or more valit utms exist, else {null}.
     */
    UtmUrl.getAttributionData = function () {
        var params = new window._SearchParams().utmParams();
        var allowedChars = /^[\w/.%-]+$/;
        var finalParams = {};

        if (params.hasOwnProperty('utm_source') && (allowedChars).test(params['utm_source'])) {
            finalParams['utm_source'] = decodeURIComponent(params['utm_source']);
        }

        if (params.hasOwnProperty('utm_campaign') && (allowedChars).test(params['utm_campaign'])) {
            finalParams['utm_campaign'] = decodeURIComponent(params['utm_campaign']);
        }

        if (params.hasOwnProperty('utm_content') && (allowedChars).test(params['utm_content'])) {
            finalParams['utm_content'] = decodeURIComponent(params['utm_content']);
        }

        if (params.hasOwnProperty('utm_term') && (allowedChars).test(params['utm_term'])) {
            finalParams['utm_term'] = decodeURIComponent(params['utm_term']);
        }

        if (params.hasOwnProperty('utm_medium') && (allowedChars).test(params['utm_medium'])) {
            finalParams['utm_medium'] = decodeURIComponent(params['utm_medium']);
        }
        return Object.getOwnPropertyNames(finalParams).length >= 1 ? finalParams : null;
    };

    /**
     * Append an object of URL parameters to a given URL.
     * @param {String} URL to append parameters to.
     * @param {Object} data object consisting of one or more parameters.
     * @returns {String} URL containing updated parameters.
     */
    UtmUrl.appendToDownloadURL = function (url, data) {
        var finalParams;
        var linkParams;

        if (url.indexOf('?') > 0) {
            linkParams = window._SearchParams.queryStringToObject(url.split('?')[1]);
            finalParams = Object.assign(linkParams, data);
        } else {
            finalParams = data;
        }

        return url.split('?')[0] + '?' + window._SearchParams.objectToQueryString(finalParams);
    };

    /**
     * If there are valid utm params on the page URL, query the
     * DOM and update Firefox Account links with the new utm data
     */
    UtmUrl.getAttributionData.init = function (){
        var params = UtmUrl.getAttributionData();
        var ctaLinks = document.getElementsByClassName('js-fxa-cta-link');

        // If there are no utm params on the page, do nothing.
        if (!params) {
            return;
        }

        // feature detect support for object modification.
        if (typeof Object.assign !== 'function' || typeof Object.getOwnPropertyNames !== 'function') {
            return;
        }

        for (var i = 0; i < ctaLinks.length; i++) {
            // get the current FxA links.
            var oldAccountsLink = ctaLinks[i].href;
            var oldMozillaOnlineLink = ctaLinks[i].getAttribute('data-mozillaonline-link');

            // append our new UTM param data to create new FxA links.
            var newAccountsLink = UtmUrl.appendToDownloadURL(oldAccountsLink, params);

            // set the FxA button to use the new link.
            ctaLinks[i].href = newAccountsLink;

            // also handle mozilla-online links for FxA China Repack.
            if (oldMozillaOnlineLink) {
                var newMozillaOnlineLink = UtmUrl.appendToDownloadURL(oldMozillaOnlineLink, params);
                ctaLinks[i].setAttribute('data-mozillaonline-link', newMozillaOnlineLink);
            }
        }
    };

    UtmUrl.getAttributionData.init();

})();
