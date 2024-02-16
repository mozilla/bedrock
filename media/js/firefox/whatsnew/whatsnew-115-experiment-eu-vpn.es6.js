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
                'data-ex-variant': 'wnp115-coupon-code-welcome',
                'data-ex-name': 'wnp-115-experiment-eu-vpn'
            });
        } else if (href.indexOf('v=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp115-coupon-code-vpn',
                'data-ex-name': 'wnp-115-experiment-eu-vpn'
            });
        }
    } else if (TrafficCop) {
        const mcnulty = new TrafficCop({
            id: 'exp-wnp-115-eu-vpn',
            cookieExpires: 0,
            variations: {
                'v=1': 50, // coupon code WELCOME
                'v=2': 50 // coupon code VPN
            }
        });
        mcnulty.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
