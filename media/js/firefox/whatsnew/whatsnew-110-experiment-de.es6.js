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
                'data-ex-variant': 'whatsnew-save-de',
                'data-ex-name': 'wnp-110-experiment-de'
            });
        } else if (href.indexOf('v=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'whatsnew-pod-de',
                'data-ex-name': 'wnp-110-experiment-de'
            });
        }
    } else if (TrafficCop) {
        const wigam = new TrafficCop({
            id: 'exp-wnp-110-de',
            cookieExpires: 0,
            variations: {
                'v=1': 50,
                'v=2': 50
            }
        });
        wigam.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
