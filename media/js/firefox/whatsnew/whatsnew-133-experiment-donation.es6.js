/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../base/experiment-utils.es6.js';

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

const href = window.location.href;

const initTrafficCop = () => {
    if (href.indexOf('v=') !== -1) {
        if (href.indexOf('v=2') !== -1) {
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'MOFO-donation',
                variant: 'mofo-donation-v2'
            });
        } else if (href.indexOf('v=3') !== -1) {
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'MOFO-donation',
                variant: 'mofo-donation-v3'
            });
        }
    } else if (TrafficCop) {
        const cop = new TrafficCop({
            variations: {
                'v=2': 50, // MoFo donate (version 2)
                'v=3': 50 // MoFo donate (version 3)
            }
        });
        cop.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
