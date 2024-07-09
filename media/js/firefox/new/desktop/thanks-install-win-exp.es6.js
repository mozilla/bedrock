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
    if (
        href.indexOf('experiment=firefox-thanks-install-win&variation=1') !== -1
    ) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'firefox-thanks-install-win',
            variant: '1'
        });
    } else if (
        href.indexOf('experiment=firefox-thanks-install-win&variation=2') !== -1
    ) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'firefox-thanks-install-win',
            variant: '2'
        });
    } else if (TrafficCop) {
        /**
         * Experiment is targeted at Windows 10 or greater using Edge browser.
         */
        if (isApprovedToRun() && isWindows10Plus() && isEdgeBrowser()) {
            const cop = new TrafficCop({
                variations: {
                    'experiment=firefox-thanks-install-win&variation=1': 25, // control
                    'experiment=firefox-thanks-install-win&variation=2': 25 // install messaging
                }
            });
            cop.init();
        }
    }
};

initTrafficCop();
