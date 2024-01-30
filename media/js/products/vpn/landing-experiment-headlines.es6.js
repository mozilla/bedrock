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
        // UA
        window.dataLayer.push({
            'data-ex-variant': 'vpn-headline-v1',
            'data-ex-name': 'vpn-landing-headlines-test'
        });
        // GA4
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'vpn-landing-headlines-test',
            variant: 'vpn-headline-v1'
        });
    } else if (href.indexOf('entrypoint_variation=2') !== -1) {
        // UA
        window.dataLayer.push({
            'data-ex-variant': 'vpn-headline-v2',
            'data-ex-name': 'vpn-landing-headlines-test'
        });
        // GA4
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'vpn-landing-headlines-test',
            variant: 'vpn-headline-v2'
        });
    } else if (href.indexOf('entrypoint_variation=3') !== -1) {
        // UA
        window.dataLayer.push({
            'data-ex-variant': 'vpn-headline-v3',
            'data-ex-name': 'vpn-landing-headlines-test'
        });
        // GA4
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'vpn-landing-headlines-test',
            variant: 'vpn-headline-v3'
        });
    } else if (TrafficCop) {
        // Avoid entering automated tests into random experiments.
        if (isApprovedToRun()) {
            const fife = new TrafficCop({
                id: 'vpn-headlines',
                variations: {
                    'entrypoint_experiment=vpn-headlines&entrypoint_variation=1': 33, // control
                    'entrypoint_experiment=vpn-headlines&entrypoint_variation=2': 33, // v2
                    'entrypoint_experiment=vpn-headlines&entrypoint_variation=3': 33 // v3
                }
            });
            fife.init();
        }
    }
};

initTrafficCop();
