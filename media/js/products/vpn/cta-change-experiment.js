/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('entrypoint_experiment=vpn-landing-page-cta-change&entrypoint_variation=') !== -1) {
            if (href.indexOf('entrypoint_variation=a') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'a',
                    'data-ex-name': 'vpn-landing-page-cta-change'
                });
            } else if (href.indexOf('entrypoint_variation=b') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'b',
                    'data-ex-name': 'vpn-landing-page-cta-change'
                });
            }
        } else {
            var cop = new Mozilla.TrafficCop({
                id: 'vpn-landing-page-cta-change-experiment',
                variations: {
                    'entrypoint_experiment=vpn-landing-page-cta-change&entrypoint_variation=a': 10,
                    'entrypoint_experiment=vpn-landing-page-cta-change&entrypoint_variation=b': 10,
                }
            });

            cop.init();
        }
    };

    // Avoid entering automated tests into random experiments.
    if (href.indexOf('automation=true') === -1 && href.indexOf('utm_medium=cpc') === -1) {
        initTrafficCop();
    }

})(window.Mozilla);
