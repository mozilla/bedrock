/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    /* update dataLayer with experiment info */
    var href = window.location.href;
    var platform = window.site.platform;
    var isMobile = /^(android|ios|fxos)$/.test(platform);
    var isFirefox = /\s(Firefox|FxiOS)/.test(navigator.userAgent) && !/Iceweasel|IceCat|SeaMonkey|Camino|like Firefox/i.test(navigator.userAgent);

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=a') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'social-proof-control',
                    'data-ex-name': 'CRO-Social-Proof-Experiment'
                });
            } else if (href.indexOf('v=b') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'social-proof-v1',
                    'data-ex-name': 'CRO-Social-Proof-Experiment'
                });
            }
        } else {
            var cop = new Mozilla.TrafficCop({
                id: 'experiment_social_proof',
                variations: {
                    'v=a': 50,
                    'v=b': 50
                }
            });

            cop.init();
        }
    };

    if (!isMobile && !isFirefox) {
        initTrafficCop();
    }

})(window.Mozilla);
