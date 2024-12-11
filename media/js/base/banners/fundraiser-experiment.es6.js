/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../experiment-utils.es6';

const href = window.location.href;

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

const init = () => {
    if (href.indexOf('v=a') !== -1) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'home-fundraiser-eoy-2024',
            variant: 'home-fundraiser-eoy-2024-va'
        });
    } else if (href.indexOf('v=b') !== -1) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'home-fundraiser-eoy-2024',
            variant: 'home-fundraiser-eoy-2024-vb'
        });
    } else if (href.indexOf('v=c') !== -1) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'home-fundraiser-eoy-2024',
            variant: 'home-fundraiser-eoy-2024-vc'
        });
    } else if (TrafficCop) {
        if (isApprovedToRun()) {
            const cop = new TrafficCop({
                variations: {
                    'v=a': 33,
                    'v=b': 33,
                    'v=c': 33
                }
            });
            cop.init();
        }
    }
};

init();
