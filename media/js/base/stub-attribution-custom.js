/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    /**
     * A custom stub attribution script that circumvents the normal stub
     * attribution logic, and instead authenticates custom data that can
     * be used to attribute first-party experiments on www.mozilla.org.
     */
    var CustomStubAttribution = {};

    CustomStubAttribution.setAttributionValues = function(params) {
        // preserve any existing utm params.
        var current = new window._SearchParams().utmParams();

        // if utm_content exists or utm_source is from AMO then don't modify anything.
        if (current.utm_content || current.utm_source === 'addons.mozilla.org') {
            return false;
        }

        // if custom attribution data is not fully formed then return false.
        if (!params.hasOwnProperty('utm_source') ||
            !params.hasOwnProperty('utm_medium') ||
            !params.hasOwnProperty('utm_campaign') ||
            !params.hasOwnProperty('utm_content')) {
            return false;
        }

        return {
            /* eslint-disable camelcase */
            utm_source: current.utm_source || params.utm_source,
            utm_medium: current.utm_medium || params.utm_medium,
            utm_campaign: current.utm_campaign || params.utm_campaign,
            utm_content: params.utm_content,
            referrer: document.referrer
            /* eslint-enable camelcase */
        };
    };

    CustomStubAttribution.init = function(params, callback) {
        if (typeof Mozilla.StubAttribution === 'undefined' || typeof window._SearchParams === 'undefined') {
            return;
        }

        // if we don't meet the usual requirements for stub attribution return false.
        if (!Mozilla.StubAttribution.meetsRequirements()) {
            return false;
        }

        // create our custom utm attribution data.
        var data = CustomStubAttribution.setAttributionValues(params);

        if (data) {
            // authenticate the custom data in the usual manner and let stub attribution do the rest.
            Mozilla.StubAttribution.requestAuthentication(data);

            // fire a callback if supplied (e.g. to fire a GA event).
            if (typeof callback === 'function') {
                callback();
            }
        } else {
            Mozilla.StubAttribution.init();
        }
    };

    window.Mozilla.CustomStubAttribution = CustomStubAttribution;

})(window.Mozilla);
