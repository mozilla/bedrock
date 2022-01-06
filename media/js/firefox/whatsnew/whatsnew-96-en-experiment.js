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
                    'data-ex-variant': 'v1-s2d-widget',
                    'data-ex-name': 'wnp-96-en-experiment'
                });
            } else if (href.indexOf('v=2') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'v2-qr-code',
                    'data-ex-name': 'wnp-96-en-experiment'
                });
            } else if (href.indexOf('v=3') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'v3-mozrally',
                    'data-ex-name': 'wnp-96-en-experiment'
                });
            }
        } else if (Mozilla.TrafficCop) {
            var cop = new Mozilla.TrafficCop({
                id: 'exp-wnp-96-en',
                cookieExpires: 0,
                variations: {
                    'v=1': 45,
                    'v=2': 45,
                    'v=3': 10
                }
            });
            cop.init();
        }
    };

    // Avoid entering automated tests into random experiments.
    if (href.indexOf('automation=true') === -1) {
        initTrafficCop();
    }
})(window.Mozilla);
