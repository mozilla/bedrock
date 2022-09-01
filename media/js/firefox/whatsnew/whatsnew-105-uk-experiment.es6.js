/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';

const href = window.location.href;

const initTrafficCop = () => {
    if (href.indexOf('v=') !== -1) {
        if (href.indexOf('v=1') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'no-variant',
                'data-ex-name': 'wnp-105-uk-experiment'
            });
        } else if (href.indexOf('v=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'discover',
                'data-ex-name': 'wnp-105-uk-experiment'
            });
        }
    } else if (TrafficCop) {
        const acab = new TrafficCop({
            id: 'exp-wnp-105-uk',
            cookieExpires: 0,
            variations: {
                'v=1': 50,
                'v=2': 50
            }
        });
        acab.init();
    }
};

// Avoid entering automated tests into random experiments.
if (href.indexOf('automation=true') === -1) {
    initTrafficCop();
}
