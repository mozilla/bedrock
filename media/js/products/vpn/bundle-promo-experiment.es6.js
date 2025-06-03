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
    if (href.indexOf('entrypoint_experiment=') !== -1) {
        if (
            href.indexOf(
                'entrypoint_experiment=vpn-landing-bundle-promo&entrypoint_variation=a'
            ) !== -1
        ) {
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'vpn-landing-bundle-promo',
                variant: 'landing-refresh-page-control'
            });
        } else if (
            href.indexOf(
                'entrypoint_experiment=vpn-landing-bundle-promo&entrypoint_variation=b'
            ) !== -1
        ) {
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'vpn-landing-bundle-promo',
                variant: 'landing-refresh-page-experiment-b'
            });
        } else if (
            href.indexOf(
                'entrypoint_experiment=vpn-landing-bundle-promo&entrypoint_variation=c'
            ) !== -1
        ) {
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'vpn-landing-bundle-promo',
                variant: 'landing-refresh-page-experiment-c'
            });
        }
    } else if (TrafficCop) {
        const cop = new TrafficCop({
            variations: {
                'entrypoint_experiment=vpn-landing-bundle-promo&entrypoint_variation=a': 33, // landing refresh page control
                'entrypoint_experiment=vpn-landing-bundle-promo&entrypoint_variation=b': 33, // landing refresh page experiment b
                'entrypoint_experiment=vpn-landing-bundle-promo&entrypoint_variation=c': 33 // landing refresh page experiment c
            }
        });
        cop.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
