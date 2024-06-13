/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../../base/experiment-utils.es6.js';

const href = window.location.href;

function isEdgeBrowser() {
    return (
        navigator.userAgent.indexOf('Edg') !== -1 ||
        navigator.userAgent.indexOf('Edge') !== -1
    );
}

function isWindows10Plus() {
    const match = navigator.userAgent.match(/Windows NT (\d+\.\d+)/);
    return match && parseFloat(match[1]) >= 10.0;
}

const initTrafficCop = () => {
    if (href.indexOf('v=1') !== -1) {
        // UA
        window.dataLayer.push({
            'data-ex-variant': '1',
            'data-ex-name': 'firefox-thanks-smoke-test'
        });
        // GA4
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'firefox-thanks-smoke-test',
            variant: '1'
        });
    } else if (href.indexOf('v=2') !== -1) {
        // UA
        window.dataLayer.push({
            'data-ex-variant': '2',
            'data-ex-name': 'firefox-thanks-smoke-test'
        });
        // GA4
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'firefox-thanks-smoke-test',
            variant: '2'
        });
    } else if (TrafficCop) {
        /**
         * Experiment is targeted at Windows 10 or greater using Edge browser.
         */
        if (isApprovedToRun() && isWindows10Plus() && isEdgeBrowser()) {
            const cop = new TrafficCop({
                variations: {
                    'v=1': 10,
                    'v=2': 10
                }
            });
            cop.init();
        }
    }
};

initTrafficCop();
