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
                'data-ex-variant': 'new-home-no-vpn-promo',
                'data-ex-name': 'new-homepage-vpn-promo'
            });
        } else if (href.indexOf('v=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'new-home-vpn-promo',
                'data-ex-name': 'new-homepage-vpn-promo'
            });
        }
    } else if (TrafficCop) {
        const cop = new TrafficCop({
            id: 'exp-new-homepage-promo',
            cookieExpires: 0,
            variations: {
                'v=1': 50, // no promo visible
                'v=2': 50 // VPN promo visible
            }
        });
        cop.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
