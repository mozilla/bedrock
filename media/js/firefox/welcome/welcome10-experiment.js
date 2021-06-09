/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';
    /* update dataLayer with experiment info */
    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=a') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-variant-1',
                    'data-ex-name': 'experiment-headline-variant'
                });
            } else if (href.indexOf('v=b') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-variant-2',
                    'data-ex-name': 'experiment-headline-variant'
                });
            }
        } else if (Mozilla.TrafficCop) {
            var cop = new Mozilla.TrafficCop({
                id: 'welcome10_experiment_headline',
                cookieExpires: 0,
                variations: {
                    'v=1': 50,
                    'v=2': 50
                }
            });
            cop.init();
        }
    };
    initTrafficCop();

})(window.Mozilla);
