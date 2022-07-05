/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';
    var TrafficCop = require('@mozmeao/trafficcop');
    var href = window.location.href;
    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=1') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'v1-coupon-promo',
                    'data-ex-name': 'vpn-coupon-promo-banner'
                });
            } else if (href.indexOf('v=2') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'v2-no-coupon-promo',
                    'data-ex-name': 'vpn-coupon-promo-banner'
                });
            }
        } else if (TrafficCop) {
            var cop = new TrafficCop({
                id: 'exp-vpn-coupon-promo-banner',
                cookieExpires: 0,
                variations: {
                    'v=1': 50,
                    'v=2': 50
                }
            });
            cop.init();
        }
    };
    // Avoid entering automated tests into random experiments.
    if (href.indexOf('automation=true') === -1) {
        initTrafficCop();
    }
})();
