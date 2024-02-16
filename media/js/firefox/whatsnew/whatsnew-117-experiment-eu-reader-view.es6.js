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
                'data-ex-variant': 'wnp117-eu-reader-view-v1',
                'data-ex-name': 'wnp117-eu-reader-view'
            });
        } else if (href.indexOf('v=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp117-eu-reader-view-v2',
                'data-ex-name': 'wnp117-eu-reader-view'
            });
        }
    } else if (TrafficCop) {
        const columbo = new TrafficCop({
            id: 'exp-wnp-117-eu-reader-view',
            cookieExpires: 0,
            variations: {
                'v=1': 50,
                'v=2': 50
            }
        });
        columbo.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
