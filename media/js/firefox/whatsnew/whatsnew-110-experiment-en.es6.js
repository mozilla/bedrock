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
                'data-ex-variant': 'wnp110-regular-en',
                'data-ex-name': 'wnp-110-experiment-en'
            });
        } else if (href.indexOf('v=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp110-features-en-vpn-bottom',
                'data-ex-name': 'wnp-110-experiment-en'
            });
        } else if (href.indexOf('v=3') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp110-features-en-vpn-top',
                'data-ex-name': 'wnp-110-experiment-en'
            });
        }
    } else if (TrafficCop) {
        const boyle = new TrafficCop({
            id: 'exp-wnp-110-en',
            cookieExpires: 1344, // 8 weeks
            variations: {
                'v=1': 96, // no variant
                'v=2': 2, // cross-sell on bottom
                'v=3': 2 // cross-sell on top
            }
        });
        boyle.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
