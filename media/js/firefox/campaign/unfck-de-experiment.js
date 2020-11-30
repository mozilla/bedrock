/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    var href = window.location.href;
    var isFirefox = /\s(Firefox|FxiOS)/.test(navigator.userAgent) && !/Iceweasel|IceCat|SeaMonkey|Camino|like Firefox/i.test(navigator.userAgent);

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=1') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'unfck-de-control',
                    'data-ex-name': 'unfck-de-header-experiment'
                });
            } else if (href.indexOf('v=2') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'unfck-de-v2',
                    'data-ex-name': 'unfck-de-header-experiment'
                });
            }
        } else {
            var cop = new Mozilla.TrafficCop({
                id: 'experiment-unfck-de-header',
                variations: {
                    'v=1': 50,
                    'v=2': 50
                }
            });

            cop.init();
        }
    };

    // Avoid entering automated tests into random experiments.
    // Target audience is non-Firefox users.
    if (href.indexOf('automation=true') === -1 && !isFirefox) {
        initTrafficCop();
    }

})(window.Mozilla);
