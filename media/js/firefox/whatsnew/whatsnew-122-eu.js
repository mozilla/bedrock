/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    // Log account status
    Mozilla.Client.getFxaDetails(function (details) {
        if (details.setup) {
            // UA
            window.dataLayer.push({
                event: 'non-interaction',
                eAction: 'whatsnew-122-eu',
                eLabel: 'firefox-signed-in'
            });

            // GA4
            window.dataLayer.push({
                event: 'dimension_set',
                firefox_is_signed_in: true
            });
        } else {
            // UA
            window.dataLayer.push({
                event: 'non-interaction',
                eAction: 'whatsnew-122-eu',
                eLabel: 'firefox-signed-out'
            });

            // GA4
            window.dataLayer.push({
                event: 'dimension_set',
                firefox_is_signed_in: false
            });
        }
    });

    // Log default status
    Mozilla.UITour.getConfiguration('appinfo', function (details) {
        if (details.defaultBrowser) {
            // UA
            window.dataLayer.push({
                event: 'non-interaction',
                eAction: 'whatsnew-122-eu',
                eLabel: 'firefox-default'
            });

            // GA4
            window.dataLayer.push({
                event: 'dimension_set',
                firefox_is_default: true
            });
        } else {
            // UA
            window.dataLayer.push({
                event: 'non-interaction',
                eAction: 'whatsnew-122-eu',
                eLabel: 'firefox-not-default'
            });

            // GA4
            window.dataLayer.push({
                event: 'dimension_set',
                firefox_is_default: false
            });
        }
    });
})();
