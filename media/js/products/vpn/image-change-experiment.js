/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('entrypoint_experiment=vpn-landing-page-image-change&entrypoint_variation=') !== -1) {
            if (href.indexOf('entrypoint_variation=current') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'current',
                    'data-ex-name': 'vpn-landing-page-image-change'
                });
            } else (href.indexOf('entrypoint_variation=en') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'en',
                    'data-ex-name': 'vpn-landing-page-image-change'
                });
            } else (href.indexOf('entrypoint_variation=fr') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'fr',
                    'data-ex-name': 'vpn-landing-page-image-change'
                });
            } else if (href.indexOf('entrypoint_variation=de') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'de',
                    'data-ex-name': 'vpn-landing-page-image-change'
                });
            }
        } else {
            var cop = new Mozilla.TrafficCop({
                id: 'vpn-landing-page-image-change-experiment',
                variations: {
                    'entrypoint_experiment=vpn-landing-page-image-change&entrypoint_variation=current': 10,
                    'entrypoint_experiment=vpn-landing-page-image-change&entrypoint_variation=en': 10,
                    'entrypoint_experiment=vpn-landing-page-image-change&entrypoint_variation=fr': 10,
                    'entrypoint_experiment=vpn-landing-page-image-change&entrypoint_variation=de': 10,
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
