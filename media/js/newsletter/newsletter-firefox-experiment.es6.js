/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../base/experiment-utils.es6.js';

const href = window.location.href;

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

const init = () => {
    if (href.indexOf('v=1') !== -1) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'experiment-newsletter-firefox',
            variant: 'experiment-newsletter-firefox-v1'
        });
    } else if (href.indexOf('v=2') !== -1) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'experiment-newsletter-firefox',
            variant: 'experiment-newsletter-firefox-v2'
        });
    } else if (TrafficCop) {
        if (isApprovedToRun()) {
            const cop = new TrafficCop({
                variations: {
                    'v=1': 50,
                    'v=2': 50
                }
            });
            cop.init();
        }
    }
};

init();
