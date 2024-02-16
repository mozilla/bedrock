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
                'data-ex-variant': 'wnp117-vpn-page-link',
                'data-ex-name': 'wnp-117-experiment-na-vpn-relay'
            });
        } else if (href.indexOf('v=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp117-vpn-pricing-link',
                'data-ex-name': 'wnp-117-experiment-na-vpn-relay'
            });
        } else if (href.indexOf('v=3') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp117-relay',
                'data-ex-name': 'wnp-117-experiment-na-vpn-relay'
            });
        }
    } else if (TrafficCop) {
        const miller = new TrafficCop({
            id: 'exp-wnp-117-na-vpn-relay',
            cookieExpires: 0,
            variations: {
                'v=1': 48, // VPN page, regular link
                'v=2': 32, // VPN page, pricing link
                'v=3': 20 // Relay page
            }
        });
        miller.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
