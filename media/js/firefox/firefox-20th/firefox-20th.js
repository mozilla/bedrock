/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    // Log account status
    Mozilla.Client.getFxaDetails((details) => {
        if (details.setup) {
            // GA4
            window.dataLayer.push({
                event: 'dimension_set',
                firefox_is_signed_in: true
            });
        } else {
            // GA4
            window.dataLayer.push({
                event: 'dimension_set',
                firefox_is_signed_in: false
            });
        }
    });

    // Log default status
    Mozilla.UITour.getConfiguration('appinfo', (details) => {
        if (details.defaultBrowser) {
            // GA4
            window.dataLayer.push({
                event: 'dimension_set',
                firefox_is_default: true
            });
        } else {
            // GA4
            window.dataLayer.push({
                event: 'dimension_set',
                firefox_is_default: false
            });
        }
    });
})();
