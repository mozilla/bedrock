/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function () {
    'use strict';

    var UtmUrl = {};
    var urlParams = new window._SearchParams().utmParams();

    /**
     * Fetch and validate utm params from the page URL for FxA referral.
     * https://mozilla.github.io/application-services/docs/accounts/metrics.html#descriptions-of-metrics-related-query-parameters
     * @returns {Object} if one or more valit utms exist, else {null}.
     */
    UtmUrl.getAttributionData = function (params) {
        var allowedChars = /^[\w/.%-]+$/;
        var finalParams = {};
        var utms = ['utm_source', 'utm_campaign', 'utm_content', 'utm_term', 'utm_medium'];

        for (var i = 0; i < utms.length; i++) {
            var utm = utms[i];
            if (Object.prototype.hasOwnProperty.call(params, utm)) {
                var param = decodeURIComponent(params[utm]);
                if ((allowedChars).test(param)) {
                    finalParams[utm] = param;
                }
            }
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
    UtmUrl.getAttributionData.init = function (urlParams){
        var params = UtmUrl.getAttributionData(urlParams);
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
            // get the link off the element
            var oldAccountsLink =  ctaLinks[i].hasAttribute('href') ? ctaLinks[i].href : null ;
            // verify this is a link to accounts.firefox.com or dev server, otherwise we shouldn't touch it
            if(oldAccountsLink) {
                if(oldAccountsLink.indexOf('https://accounts.firefox.com') === 0 || oldAccountsLink.indexOf('https://latest.dev.lcip.org') === 0) {
                    // get the China repack link, so that can be updated too
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
            }
        }
    };

    UtmUrl.getAttributionData.init(urlParams);

    window.Mozilla.UtmUrl = UtmUrl;
})();
