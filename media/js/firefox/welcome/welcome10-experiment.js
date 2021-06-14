/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';
    /* update dataLayer with experiment info */
    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=1') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'welcome10-variant-1',
                    'data-ex-name': 'welcome10-copy-experiment'
                });
            } else if (href.indexOf('v=2') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'welcom10-variant-2',
                    'data-ex-name': 'welcome10-copy-experiment'
                });
            }
        } else if (Mozilla.TrafficCop) {
            var cop = new Mozilla.TrafficCop({
                id: 'welcome10_experiment_copy',
                cookieExpires: 0,
                variations: {
                    'v=1': 50,
                    'v=2': 50
                }
            });
            cop.init();
        }
    };

    if (href.indexOf('automation=true') {
        initTrafficCop();
    }

})(window.Mozilla);
