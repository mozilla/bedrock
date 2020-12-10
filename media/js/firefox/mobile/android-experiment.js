/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    var isAndroid = document.getElementsByTagName('html')[0].classList.contains('android');
    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=1') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'firefox-mobile-android-control',
                    'data-ex-name': 'firefox-mobile-android-experiment'
                });
            } else if (href.indexOf('v=2') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'firefox-mobile-android-v2',
                    'data-ex-name': 'firefox-mobile-android-experiment'
                });
            }
        } else {
            var cop = new Mozilla.TrafficCop({
                id: 'experiment-firefox-mobile-android',
                variations: {
                    'v=1': 12,
                    'v=2': 12,
                    'v=3': 12,
                    'v=4': 12,
                    'v=5': 12,
                }
            });

            cop.init();
        }
    };

    // Avoid entering automated tests into random experiments.
    // Target audience is Android mobile users.
    if (href.indexOf('automation=true') && isAndroid) {
        initTrafficCop();
    }

})(window.Mozilla);
