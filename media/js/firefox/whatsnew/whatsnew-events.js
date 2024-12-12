/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

function sendEvents() {
    'use strict';

    // Log account status
    window.Mozilla.Client.getFxaDetails((details) => {
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_signed_in: details.setup ? true : false
        });
    });

    // Log default status
    window.Mozilla.UITour.getConfiguration('appinfo', (details) => {
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_default: details.defaultBrowser ? true : false
        });
    });
}

if (typeof window.Mozilla.Client !== 'undefined') {
    sendEvents();
}
