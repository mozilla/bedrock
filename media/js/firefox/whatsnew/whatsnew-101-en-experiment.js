/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function (Mozilla) {
    'use strict';

    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=1') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'vpn-desktop',
                    'data-ex-name': 'wnp-101-en-experiment'
                });
            } else if (href.indexOf('v=2') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'vpn-mobile-qr-b',
                    'data-ex-name': 'wnp-101-en-experiment'
                });
            } else if (href.indexOf('v=3') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'vpn-mobile-qr-c',
                    'data-ex-name': 'wnp-101-en-experiment'
                });
            }
        } else if (Mozilla.TrafficCop) {
            var acab = new Mozilla.TrafficCop({
                id: 'exp-wnp-101-en',
                cookieExpires: 0,
                variations: {
                    'v=1': 86,
                    'v=2': 7,
                    'v=3': 7
                }
            });
            acab.init();
        }
    };

    // Avoid entering automated tests into random experiments.
    if (href.indexOf('automation=true') === -1) {
        initTrafficCop();
    }
})(window.Mozilla);
