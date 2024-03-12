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
                'data-ex-variant': 'wnp124-na-video',
                'data-ex-name': 'wnp124-experiment-na'
            });
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'wnp124-experiment-na',
                variant: 'wnp124-na-video'
            });
        } else if (href.indexOf('v=2') !== -1) {
            // UA
            window.dataLayer.push({
                'data-ex-variant': 'wnp124-na-static',
                'data-ex-name': 'wnp124-experiment-na'
            });
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'wnp124-experiment-na',
                variant: 'wnp124-na-static'
            });
        }
    } else if (TrafficCop && isApprovedToRun()) {
        const cop = new TrafficCop({
            id: 'wnp124-experiment-na',
            cookieExpires: 0,
            variations: {
                'v=1': 70, // Video
                'v=2': 30 // Static image
            }
        });
        cop.init();
    }
};

initTrafficCop();
