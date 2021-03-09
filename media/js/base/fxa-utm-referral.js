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

    var allowedList = [
        'https://accounts.firefox.com/',
        'https://accounts.firefox.com.cn/',
        'https://accounts.stage.mozaws.net/',
        'https://monitor.firefox.com/',
        'https://getpocket.com/',
        'https://latest.dev.lcip.org/',
        'https://stable.dev.lcip.org/',
        'https://vpn.mozilla.org/',
        'https://stage-vpn.guardian.nonprod.cloudops.mozgcp.net/'
    ];

    var utms = ['utm_source', 'utm_campaign', 'utm_content', 'utm_term', 'utm_medium'];
    var entrypointParams = ['entrypoint_experiment', 'entrypoint_variation'];
    var acceptedParams = utms.concat(entrypointParams);

    /**
     * Returns the hostname for a given URL.
     * @param {String} url.
     * @returns {String} hostname.
     */
    UtmUrl.getHostName = function(url) {
        var matches = url.match(/^https?:\/\/(?:[^/?#]+)(?:[/?#]|$)/i);
        return matches && matches[0];
    };

    /**
     * Fetch and validate accepted params from the page URL for FxA referral.
     * https://mozilla.github.io/application-services/docs/accounts/metrics.html#descriptions-of-metrics-related-query-parameters
     * @returns {Object} if params are valid, else {null}.
     */
    UtmUrl.getAttributionData = function (params) {
        var allowedChars = /^[\w/.%-]+$/;
        var finalParams = {};

        for (var i = 0; i < acceptedParams.length; i++) {
            var acceptedParam = acceptedParams[i];
            if (Object.prototype.hasOwnProperty.call(params, acceptedParam)) {
                var foundParam = decodeURIComponent(params[acceptedParam]);
                if ((allowedChars).test(foundParam)) {
                    finalParams[acceptedParam] = foundParam;
                }
            }
        }

        // Both utm_source and utm_campaign are considered required, so only pass through referral data if they exist.
        // Alternatively, pass through entrypoint_experiment and entrypoint_variation independently.
        if ((Object.prototype.hasOwnProperty.call(finalParams, 'utm_source') && Object.prototype.hasOwnProperty.call(finalParams, 'utm_campaign')) ||
            (Object.prototype.hasOwnProperty.call(finalParams, 'entrypoint_experiment') && Object.prototype.hasOwnProperty.call(finalParams, 'entrypoint_variation'))) {
            return finalParams;
        }

        return null;
    };

    /**
     * Append an object of accepted parameters to a given URL.
     * Object parameters will erase all existing accepted parameters, whether present or not.
     * @param {String} URL to append parameters to.
     * @param {Object} data object consisting of one or more parameters.
     * @returns {String} URL containing updated parameters.
     */
    UtmUrl.appendToDownloadURL = function (url, data) {
        var finalParams;
        var linkParams;

        if (url.indexOf('?') > 0) {
            linkParams = window._SearchParams.queryStringToObject(url.split('?')[1]);

            // If we have utm parameters then remove them from the target URL,
            // as we don't want to muddle data from different campaign sources.
            if (Object.prototype.hasOwnProperty.call(data, 'utm_source') && Object.prototype.hasOwnProperty.call(data, 'utm_campaign')) {
                for (var i = 0; i < utms.length; i++) {
                    var utmParam = utms[i];
                    if (Object.prototype.hasOwnProperty.call(linkParams, utmParam)) {
                        delete linkParams[utmParam];
                    }
                }
            }

            // In principle, experiments should never clobber eachother(!). However, if we have
            // new entrypoint_* parameters then assume they take precedence in the target URL.
            if (Object.prototype.hasOwnProperty.call(data, 'entrypoint_experiment') && Object.prototype.hasOwnProperty.call(data, 'entrypoint_variation')) {
                for (var j = 0; j < entrypointParams.length; j++) {
                    var entryPointParam = entrypointParams[j];
                    if (Object.prototype.hasOwnProperty.call(linkParams, entryPointParam)) {
                        delete linkParams[entryPointParam];
                    }
                }
            }

            finalParams = Object.assign(linkParams, data);
        } else {
            finalParams = data;
        }

        return url.split('?')[0] + '?' + window._SearchParams.objectToQueryString(finalParams);
    };

    /**
     * If there are validated referral params on the page URL, query the
     * DOM and update Firefox Account links with the new param data.
     */
    UtmUrl.init = function (urlParams) {
        var params = UtmUrl.getAttributionData(urlParams);
        var ctaLinks = document.getElementsByClassName('js-fxa-cta-link');

        // If there are no accepted params on the page URL, do nothing.
        if (!params) {
            return;
        }

        // feature detect support for object modification.
        if (typeof Object.assign !== 'function') {
            return;
        }

        for (var i = 0; i < ctaLinks.length; i++) {
            // get the link off the element
            var oldAccountsLink =  ctaLinks[i].hasAttribute('href') ? ctaLinks[i].href : null ;

            if (oldAccountsLink) {
                var hostName = UtmUrl.getHostName(oldAccountsLink);
                // check if link is in the FxA referral allowedList list.
                if (hostName && allowedList.indexOf(hostName) !== -1) {
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

    window.Mozilla.UtmUrl = UtmUrl;
})();
