/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';
    var TrafficCop = require('@mozmeao/trafficcop');
    /* update dataLayer with experiment info */
    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=1') !== -1) {
                // UA
                window.dataLayer.push({
                    'data-ex-variant': 'v1-pointed',
                    'data-ex-name': 'firefox-set-as-default-experiment'
                });
                // GA4
                window.dataLayer.push({
                    event: 'experiment_view',
                    id: 'v1-pointed',
                    variant: 'firefox-set-as-default-experiment'
                });
            } else if (href.indexOf('v=2') !== -1) {
                // UA
                window.dataLayer.push({
                    'data-ex-variant': 'v2-privacy',
                    'data-ex-name': 'firefox-set-as-default-experiment'
                });
                // GA4
                window.dataLayer.push({
                    event: 'experiment_view',
                    id: 'v2-privacy',
                    variant: 'firefox-set-as-default-experiment'
                });
            } else if (href.indexOf('v=3') !== -1) {
                // UA
                window.dataLayer.push({
                    'data-ex-variant': 'v3-mission',
                    'data-ex-name': 'firefox-set-as-default-experiment'
                });
                // GA4
                window.dataLayer.push({
                    event: 'experiment_view',
                    id: 'v3-mission',
                    variant: 'firefox-set-as-default-experiment'
                });
            }
        } else if (TrafficCop) {
            var cop = new TrafficCop({
                id: 'exp-firefox-set-as-default',
                cookieExpires: 0,
                variations: {
                    'v=1': 33,
                    'v=2': 33,
                    'v=3': 33
                }
            });
            cop.init();
        }
    };
    initTrafficCop();
})();
