/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // Respect Do Not Track
    if (typeof Mozilla.dntEnabled === 'function' && !Mozilla.dntEnabled()) {

        // Get Data Source Name (DSN)
        var sentryDsn = document.getElementsByTagName('html')[0].getAttribute('data-sentry-dsn');

        // Configure Sentry SDK
        if (typeof window.Sentry !== 'undefined' && sentryDsn) {
            window.Sentry.init({
                dsn: sentryDsn ,
                sampleRate: 0.10,
                denyUrls: [
                    // Chrome extensions
                    /extensions\//i,
                    /^chrome:\/\//i,
                    // Firefox extensions
                    /^resource:\/\//i
                ]
            });
        }
    }

})();
