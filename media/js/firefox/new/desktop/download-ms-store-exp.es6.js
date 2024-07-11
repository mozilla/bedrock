/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../../base/experiment-utils.es6.js';

const href = window.location.href;

function isWindows10Plus() {
    const match = navigator.userAgent.match(/Windows NT (\d+\.\d+)/);
    return match && parseFloat(match[1]) >= 10.0;
}

function isFirefox() {
    return (
        /\s(Firefox|FxiOS)/.test(navigator.userAgent) &&
        !/Iceweasel|IceCat|SeaMonkey|Camino|like Firefox/i.test(
            navigator.userAgent
        )
    );
}

const initTrafficCop = () => {
    if (
        href.indexOf(
            'experiment=mozorg-firefox-vsinstaller-exp&variation=control'
        ) !== -1
    ) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'mozorg-firefox-vsinstaller-exp',
            variant: 'control'
        });
    } else if (
        href.indexOf(
            'experiment=mozorg-firefox-vsinstaller-exp&variation=treatment'
        ) !== -1
    ) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'mozorg-firefox-vsinstaller-exp',
            variant: 'treatment'
        });
    } else if (TrafficCop) {
        /**
         * Experiment is targeted at Windows 10 or greater and non-Firefox browsers.
         */
        if (isApprovedToRun() && isWindows10Plus() && !isFirefox()) {
            const cop = new TrafficCop({
                variations: {
                    'experiment=mozorg-firefox-vsinstaller-exp&variation=control': 25,
                    'experiment=mozorg-firefox-vsinstaller-exp&variation=treatment': 25
                }
            });
            cop.init();
        }
    }
};

initTrafficCop();
