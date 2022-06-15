/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';
    var TrafficCop = require('@mozmeao/trafficcop');
    /* update dataLayer with experiment info */
    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            if (href.indexOf('v=text') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-text',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            } else if (href.indexOf('v=image') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-image',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            } else if (href.indexOf('v=animation') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-animation',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            } else if (href.indexOf('v=header-text') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-header-text',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            }
        } else if (TrafficCop) {
            var cop = new TrafficCop({
                id: 'welcome8_experiment_hvt_visual',
                cookieExpires: 0,
                variations: {
                    'v=text': 3,
                    'v=image': 3,
                    'v=animation': 3,
                    'v=header-text': 3
                }
            });
            cop.init();
        }
    };
    initTrafficCop();
})();
