/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Log account status
Mozilla.Client.getFxaDetails((details) => {
    'use strict';

    window.dataLayer.push({
        event: 'dimension_set',
        firefox_is_signed_in: details.setup ? true : false
    });
});

// Log default status
Mozilla.UITour.getConfiguration('appinfo', (details) => {
    'use strict';

    window.dataLayer.push({
        event: 'dimension_set',
        firefox_is_default: details.defaultBrowser ? true : false
    });
});
