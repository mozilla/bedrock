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
                'data-ex-variant': 'wnp120-video',
                'data-ex-name': 'wnp-120-experiment-na'
            });
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'wnp-120-experiment-na',
                variant: 'wnp120-video'
            });
        } else if (href.indexOf('v=2') !== -1) {
            // UA
            window.dataLayer.push({
                'data-ex-variant': 'wnp120-no-video',
                'data-ex-name': 'wnp-120-experiment-na'
            });
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'wnp-120-experiment-na',
                variant: 'wnp120-no-video'
            });
        }
    } else if (TrafficCop) {
        const murtaugh = new TrafficCop({
            id: 'wnp-120-expiriment-na',
            cookieExpires: 0,
            variations: {
                'v=1': 0, // Fakespot video
                'v=2': 100 // no video
            }
        });
        murtaugh.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
