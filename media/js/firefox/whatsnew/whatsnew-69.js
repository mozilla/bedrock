/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // Prevent double-requesting Flow IDs. Inits signed out button even on non-firefox browsers (highly unlikely on this page, but you never know).
    if (Mozilla.Client.isFirefoxDesktop) {
        Mozilla.Client.getFxaDetails(function(details) {
            if (details.setup) {
                Mozilla.MonitorButton.init('monitor-button-signed-in');
            } else {
                Mozilla.MonitorButton.init('monitor-button-signed-out');
            }
        });
    } else {
        Mozilla.MonitorButton.init('monitor-button-signed-out');
    }
})();
