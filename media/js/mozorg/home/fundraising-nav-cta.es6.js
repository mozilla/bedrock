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
            event: 'experiment_view',
            id: 'fundraising-nav-cta-july2024',
            variant: 'fundraising-nav-cta-v1'
        });
    } else if (href.indexOf('v=2') !== -1) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'fundraising-nav-cta-july2024',
            variant: 'fundraising-nav-cta-v2'
        });
    } else if (TrafficCop) {
        // Avoid entering automated tests into random experiments.
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
