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
                'data-ex-variant': 'wnp112-en-vpn',
                'data-ex-name': 'wnp-112-experiment-en'
            });
        } else if (href.indexOf('v=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp112-en-bundle',
                'data-ex-name': 'wnp-112-experiment-en'
            });
        } else if (href.indexOf('v=3') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp112-en-features-v3-pocket-first',
                'data-ex-name': 'wnp-112-experiment-en'
            });
        } else if (href.indexOf('v=4') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp112-en-features-v4-vpn-first',
                'data-ex-name': 'wnp-112-experiment-en'
            });
        } else if (href.indexOf('v=5') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp112-en-features-v5-pocket-second',
                'data-ex-name': 'wnp-112-experiment-en'
            });
        } else if (href.indexOf('v=6') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp112-en-features-v6-vpn-second',
                'data-ex-name': 'wnp-112-experiment-en'
            });
        }
    } else if (TrafficCop) {
        const holt = new TrafficCop({
            id: 'exp-wnp-112-en',
            cookieExpires: 1344, // 8 weeks
            variations: {
                'v=1': 75, // VPN
                'v=2': 20, // VPN + Relay bundle
                'v=3': 1.25, // Features, Pocket first
                'v=4': 1.25, // Features, VPN first
                'v=5': 1.25, // Features, Pocket second
                'v=6': 1.25 // Features, VPN second
            }
        });
        holt.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
