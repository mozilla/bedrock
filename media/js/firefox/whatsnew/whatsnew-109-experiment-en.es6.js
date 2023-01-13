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
                'data-ex-variant': 'wnp109-regular-en',
                'data-ex-name': 'wnp-109-experiment-en'
            });
        } else if (href.indexOf('v=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp109-features-en',
                'data-ex-name': 'wnp-109-experiment-en'
            });
        }
    } else if (TrafficCop) {
        const jeffords = new TrafficCop({
            id: 'exp-wnp-109-en',
            cookieExpires: 0,
            variations: {
                'v=1': 95,
                'v=2': 5
            }
        });
        jeffords.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
