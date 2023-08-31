/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../base/experiment-utils.es6.js';

const href = window.location.href;

const initTrafficCop = () => {
    if (TrafficCop) {
        const odo = new TrafficCop({
            id: 'vpn-refresh-pricing-experiment',
            cookieExpires: 0,
            variations: {
                'entrypoint_experiment=vpn-refresh-pricing&entrypoint_variation=1': 50, // Pricing in columns
                'entrypoint_experiment=vpn-refresh-pricing&entrypoint_variation=2': 50 // Pricing in rows
            }
        });
        odo.init();
    }
};

const init = function () {
    if (
        href.indexOf(
            'entrypoint_experiment=vpn-refresh-pricing&entrypoint_variation='
        ) !== -1
    ) {
        if (href.indexOf('entrypoint_variation=1') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'vpn-refresh-pricing-columns',
                'data-ex-name': 'vpn-refresh-pricing'
            });
        } else if (href.indexOf('entrypoint_variation=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'vpn-refresh-pricing-rows',
                'data-ex-name': 'vpn-refresh-pricing'
            });
        }
    } else if (isApprovedToRun()) {
        // Avoid entering automated tests into random experiments.
        initTrafficCop();
    }
};

init();
