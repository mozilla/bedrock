/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../base/experiment-utils.es6.js';

const href = window.location.href;

const initTrafficCop = () => {
    if (
        href.indexOf(
            'entrypoint_experiment=vpn-landing-refresh&entrypoint_variation='
        ) !== -1
    ) {
        if (href.indexOf('entrypoint_variation=1') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'vpn-landing-control',
                'data-ex-name': 'vpn-landing-refresh'
            });
        } else if (href.indexOf('entrypoint_variation=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'vpn-landing-refresh',
                'data-ex-name': 'vpn-landing-refresh'
            });
        }
    } else if (TrafficCop) {
        const scully = new TrafficCop({
            id: 'vpn-landing-refresh-experiment',
            cookieExpires: 0,
            variations: {
                'entrypoint_experiment=vpn-landing-refresh&entrypoint_variation=1': 50, // Control, old page
                'entrypoint_experiment=vpn-landing-refresh&entrypoint_variation=2': 50 // Refreshed page
            }
        });
        scully.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
