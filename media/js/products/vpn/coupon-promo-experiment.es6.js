/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../base/experiment-utils.es6.js';

const href = window.location.href;
const initTrafficCop = () => {
    if (
        href.indexOf(
            'entrypoint_experiment=vpn-coupon-promo-banner&entrypoint_variation='
        ) !== -1
    ) {
        if (href.indexOf('entrypoint_variation=1') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'v1-coupon-promo',
                'data-ex-name': 'vpn-coupon-promo-banner'
            });
        } else if (href.indexOf('entrypoint_variation=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'v2-no-coupon-promo',
                'data-ex-name': 'vpn-coupon-promo-banner'
            });
        }
    } else if (TrafficCop) {
        const cop = new TrafficCop({
            id: 'exp-vpn-coupon-promo-banner',
            cookieExpires: 0,
            variations: {
                'entrypoint_experiment=vpn-coupon-promo-banner&entrypoint_variation=1': 50,
                'entrypoint_experiment=vpn-coupon-promo-banner&entrypoint_variation=2': 50
            }
        });
        cop.init();
    }
};

// Avoid entering automated tests into random experiments.
if (isApprovedToRun()) {
    initTrafficCop();
}
