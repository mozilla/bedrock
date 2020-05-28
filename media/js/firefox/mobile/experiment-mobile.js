/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    /* update dataLayer with experiment info */
    var href = window.location.href;
    var platform = window.site.platform;
    var isMobile = /^(android|ios|fxos)$/.test(platform);

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=a') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'firefox-mobile-send-to-device-control',
                    'data-ex-name': 'CRO-Firefox-Mobile-Send-to-Device-Experiment'
                });
            } else if (href.indexOf('v=b') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'firefox-mobile-send-to-device-v1',
                    'data-ex-name': 'CRO-Firefox-Mobile-Send-to-Device-Experiment'
                });
            }
        } else {
            var cop = new Mozilla.TrafficCop({
                id: 'experiment_firefox_mobile',
                variations: {
                    'v=a': 23,
                    'v=b': 23
                }
            });

            cop.init();
        }
    };

    if (!isMobile) {
        initTrafficCop();
    }

})(window.Mozilla);
