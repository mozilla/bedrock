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
            window.dataLayer.push({
                'data-ex-variant': 'wnp119-boxes-open',
                'data-ex-name': 'wnp-119-experiment-eu'
            });
        } else if (href.indexOf('v=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp117-boxes-closed',
                'data-ex-name': 'wnp-119-experiment-eu'
            });
        } else if (href.indexOf('v=3') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp119-relay',
                'data-ex-name': 'wnp-119-experiment-eu'
            });
        }
    } else if (TrafficCop) {
        const murtaugh = new TrafficCop({
            id: 'wnp-119-experiment-eu',
            cookieExpires: 0,
            variations: {
                'v=1': 33, // Three boxes, open
                'v=2': 33, // Three boxes, closed
                'v=3': 33 // Relay page
            }
        });
        murtaugh.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
