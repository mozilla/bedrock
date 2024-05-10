/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Log account status
Mozilla.Client.getFxaDetails((details) => {
    'use strict';

    if (details.setup) {
        // UA
        window.dataLayer.push({
            event: 'non-interaction',
            eAction: 'whatsnew-126',
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
            eAction: 'whatsnew-126',
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
Mozilla.UITour.getConfiguration('appinfo', (details) => {
    'use strict';

    if (details.defaultBrowser) {
        // UA
        window.dataLayer.push({
            event: 'non-interaction',
            eAction: 'whatsnew-126',
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
            eAction: 'whatsnew-126',
            eLabel: 'firefox-not-default'
        });

        // GA4
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_default: false
        });
    }
});
