/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('cta_experimentation=vpn-landing-page-cta-change&cta_variation=') !== -1) {
            if (href.indexOf('cta_variation=a') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'a',
                    'data-ex-name': 'vpn-landing-page-cta-change'
                });
            } else if (href.indexOf('cta_variation=b') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'b',
                    'data-ex-name': 'vpn-landing-page-cta-change'
                });
            }
        } else {
            var cop = new Mozilla.TrafficCop({
                id: 'vpn-landing-page-cta-change-experiment',
                variations: {
                    'cta_experimentation=vpn-landing-page-cta-change&cta_variation=a': 50,
                    'cta_experimentation=vpn-landing-page-cta-change&cta_variation=b': 50,
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
