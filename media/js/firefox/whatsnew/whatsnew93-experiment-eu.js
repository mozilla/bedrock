/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';
    /* update dataLayer with experiment info */
    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=2') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'whatsnew93-variant-2',
                    'data-ex-name': 'whatsnew93-experiment'
                });
            } else if (href.indexOf('v=3') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'whatsnew93-variant-3',
                    'data-ex-name': 'whatsnew93-experiment'
                });
            }
        } else if (Mozilla.TrafficCop) {
            var cop = new Mozilla.TrafficCop({
                id: 'whatsnew93_experiment',
                cookieExpires: 0,
                variations: {
                    'v=2': 5,
                    'v=3': 5
                }
            });
            cop.init();
        }
    };

    if (href.indexOf('automation=true') === -1) {
        initTrafficCop();
    }

})(window.Mozilla);
