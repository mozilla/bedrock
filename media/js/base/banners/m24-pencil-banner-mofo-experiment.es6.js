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
        if (href.indexOf('v=a') !== -1) {
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'pencil-banner-MOFO-donation',
                variant: 'mofo-donation-a'
            });
        } else if (href.indexOf('v=b') !== -1) {
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'pencil-banner-MOFO-donation',
                variant: 'mofo-donation-b'
            });
        } else if (href.indexOf('v=c') !== -1) {
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'pencil-banner-MOFO-donation',
                variant: 'mofo-donation-c'
            });
        }
    } else if (TrafficCop) {
        const cop = new TrafficCop({
            variations: {
                'v=a': 33, // MoFo donate (version 1)
                'v=b': 34, // MoFo donate (version 2)
                'v=c': 33 // MoFo donate (version 3)
            }
        });
        cop.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
