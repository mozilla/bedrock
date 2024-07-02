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
            return;
        } else if (href.indexOf('v=2') !== -1) {
            return;
        } else if (href.indexOf('v=3') !== -1) {
            return;
        }
    } else if (TrafficCop) {
        const cop = new TrafficCop({
            variations: {
                'v=1': 80, // add-ons (version A)
                'v=2': 10, // MoFo donate (version B) -- only for DE, FR, GB
                'v=3': 10 // MoFo donate (version C) -- only for DE, FR, GB
            }
        });
        cop.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
