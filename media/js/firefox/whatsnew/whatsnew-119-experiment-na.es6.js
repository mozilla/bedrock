/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../base/experiment-utils.es6.js';

const href = window.location.href;

const initTrafficCop = () => {
    if (href.indexOf('v=') !== -1) {
        if (href.indexOf('v=1') !== -1) {
            // UA
            window.dataLayer.push({
                'data-ex-variant': 'wnp119-boxes',
                'data-ex-name': 'wnp-119-experiment-na'
            });
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'wnp-119-experiment-na',
                variant: 'wnp119-boxes'
            });
        } else if (href.indexOf('v=2') !== -1) {
            // UA
            window.dataLayer.push({
                'data-ex-variant': 'wnp119-addons',
                'data-ex-name': 'wnp-119-experiment-na'
            });
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'wnp-119-experiment-na',
                variant: 'wnp119-addons'
            });
        }
    } else if (TrafficCop) {
        const riggs = new TrafficCop({
            id: 'wnp-119-experiment-na',
            cookieExpires: 0,
            variations: {
                'v=1': 50, // Three boxes
                'v=2': 50 // Addons
            }
        });
        riggs.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
