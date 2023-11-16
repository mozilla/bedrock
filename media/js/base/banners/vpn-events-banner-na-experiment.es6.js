/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../experiment-utils.es6.js';

const href = window.location.href;

const init = () => {
    if (href.indexOf('entrypoint_variation=1') !== -1) {
        window.dataLayer.push({
            'data-ex-variant': 'vpn-holidays-na-test-v1',
            'data-ex-name': 'vpn-holidays-na-test'
        });
    } else if (href.indexOf('entrypoint_variation=2') !== -1) {
        // set cookie to prevent banner from showing
        const date = new Date();
        const cookieDuration = 1 * 24 * 60 * 60 * 1000; // 1 day expiration
        date.setTime(date.getTime() + cookieDuration); // 1 day expiration
        Mozilla.Cookies.setItem(
            'vpn-events-banner',
            true,
            date.toUTCString(),
            '/',
            undefined,
            false,
            'lax'
        );

        window.dataLayer.push({
            'data-ex-variant': 'vpn-holidays-na-test-v2',
            'data-ex-name': 'vpn-holidays-na-test'
        });
    } else if (TrafficCop) {
        // Avoid entering automated tests into random experiments.
        if (isApprovedToRun()) {
            const cop = new TrafficCop({
                id: 'vpn-holidays-na-test',
                variations: {
                    'entrypoint_variation=1': 50,
                    'entrypoint_variation=2': 50
                }
            });
            cop.init();
        }
    }
};

init();
