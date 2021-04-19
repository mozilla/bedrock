/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=1') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'wnp-88-control',
                    'data-ex-name': 'wnp-88-experiment'
                });
            } else if (href.indexOf('v=2') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'wnp-88-v2',
                    'data-ex-name': 'wnp-88-experiment'
                });
            } else if (href.indexOf('v=3') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'wnp-88-v3',
                    'data-ex-name': 'wnp-88-experiment'
                });
            } else if (href.indexOf('v=4') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'wnp-88-v4',
                    'data-ex-name': 'wnp-88-experiment'
                });
            } else if (href.indexOf('v=5') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'wnp-88-v5',
                    'data-ex-name': 'wnp-88-experiment'
                });
            }
        } else {
            var cop = new Mozilla.TrafficCop({
                id: 'experiment-wnp-88',
                variations: {
                    'v=1': 5,
                    'v=2': 5,
                    'v=3': 5,
                    'v=4': 5,
                    'v=5': 5,
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
