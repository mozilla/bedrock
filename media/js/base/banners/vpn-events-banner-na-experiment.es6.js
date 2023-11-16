/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../experiment-utils.es6.js';

const href = window.location.href;

const initTrafficCop = () => {
    if (href.indexOf('entrypoint_variation=') !== -1) {
        if (href.indexOf('entrypoint_variation=1') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'vpn-holidays-na-test-v1',
                'data-ex-name': 'vpn-holidays-na-test'
            });
        } else if (href.indexOf('entrypoint_variation=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'vpn-holidays-na-test-v2',
                'data-ex-name': 'vpn-holidays-na-test'
            });
        }
    } else if (TrafficCop) {
        const cop = new TrafficCop({
            id: 'vpn-holidays-na-test',
            variations: {
                'entrypoint_variation=1': 50,
                'entrypoint_variation=2': 50
            }
        });
        cop.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
