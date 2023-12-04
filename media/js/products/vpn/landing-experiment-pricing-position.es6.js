/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../base/experiment-utils.es6.js';

const href = window.location.href;

const initTrafficCop = () => {
    if (href.indexOf('entrypoint_variation=1') !== -1) {
        window.dataLayer.push({
            'data-ex-variant': 'pricing-bottom',
            'data-ex-name': 'vpn-pricing-position'
        });
    } else if (href.indexOf('entrypoint_variation=2') !== -1) {
        window.dataLayer.push({
            'data-ex-variant': 'pricing-top',
            'data-ex-name': 'vpn-pricing-position'
        });
    } else if (TrafficCop) {
        // Avoid entering automated tests into random experiments.
        if (isApprovedToRun()) {
            const briscoe = new TrafficCop({
                id: 'vpn-pricing-position',
                variations: {
                    'entrypoint_experiment=vpn-pricing-position&entrypoint_variation=1': 50, // control, pricing at bottom
                    'entrypoint_experiment=vpn-pricing-position&entrypoint_variation=2': 50 // pricing at top
                }
            });
            briscoe.init();
        }
    }
};

initTrafficCop();
