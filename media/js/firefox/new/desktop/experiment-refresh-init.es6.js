/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../../base/experiment-utils.es6';

const href = window.location.href;

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}
const init = () => {
    if (href.indexOf('xv=refresh-new&v=a') !== -1) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'refresh-new',
            variant: 'refresh-new-control'
        });
    } else if (href.indexOf('xv=refresh-new&v=b') !== -1) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'refresh-new',
            variant: 'refresh-new-treatment'
        });
    } else if (TrafficCop) {
        if (isApprovedToRun()) {
            const cop = new TrafficCop({
                variations: {
                    'xv=refresh-new&v=a': 50,
                    'xv=refresh-new&v=b': 50
                }
            });
            cop.init();
        }
    }
};

init();
