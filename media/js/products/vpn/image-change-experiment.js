/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('entrypoint_experiment=vpn-image-change-image-change&entrypoint_variation=') !== -1) {
            if (href.indexOf('entrypoint_variation=current') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'current',
                    'data-ex-name': 'vpn-landing-page-image-change'
                });
            } else if(href.indexOf('entrypoint_variation=blur') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'blur',
                    'data-ex-name': 'vpn-landing-page-image-change'
                });
            }
        } else {
            var cop = new Mozilla.TrafficCop({
                id: 'vpn-landing-page-image-change-experiment',
                variations: {
                    'entrypoint_experiment=vpn-landing-page-image-change&entrypoint_variation=current': 50,
                    'entrypoint_experiment=vpn-landing-page-image-change&entrypoint_variation=blur': 50
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
