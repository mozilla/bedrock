/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../base/experiment-utils.es6.js';

const href = window.location.href;

const init = () => {
    if (href.indexOf('v=1') !== -1) {
        window.dataLayer.push({
            'data-ex-variant': 'exp-home-fundraising-banner-v1',
            'data-ex-name': 'exp-home-fundraising-banner'
        });
    } else if (href.indexOf('v=2') !== -1) {
        window.dataLayer.push({
            'data-ex-variant': 'exp-home-fundraising-banner-v2',
            'data-ex-name': 'exp-home-fundraising-banner'
        });
    } else if (href.indexOf('v=3') !== -1) {
        window.dataLayer.push({
            'data-ex-variant': 'exp-home-fundraising-banner-v3',
            'data-ex-name': 'exp-home-fundraising-banner'
        });
    } else if (TrafficCop) {
        // Avoid entering automated tests into random experiments.
        if (isApprovedToRun()) {
            const cop = new TrafficCop({
                id: 'exp-home-fundraising-banner',
                cookieExpires: 0,
                variations: {
                    'v=1': 33,
                    'v=2': 33,
                    'v=3': 33
                }
            });
            cop.init();
        }
    }
};

init();
