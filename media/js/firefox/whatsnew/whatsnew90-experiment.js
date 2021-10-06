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
                    'data-ex-variant': 'whatsnew90-variant-1',
                    'data-ex-name': 'whatsnew90-cta-experiment'
                });
            } else if (href.indexOf('v=2') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'whatsnew90-variant-2',
                    'data-ex-name': 'whatsnew90-cta-experiment'
                });
            }
        } else if (Mozilla.TrafficCop) {
            var cop = new Mozilla.TrafficCop({
                id: 'whatsnew90_experiment_cta',
                cookieExpires: 0,
                variations: {
                    'v=1': 90,
                    'v=2': 10
                }
            });
            cop.init();
        }
    };

    if (href.indexOf('automation=true') === -1) {
        initTrafficCop();
    }
})(window.Mozilla);
