/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var Sentry = require('@sentry/browser');

    // Respect Do Not Track
    if (typeof Mozilla.dntEnabled === 'function' && !Mozilla.dntEnabled()) {

        // Get Data Source Name (DSN)
        var sentryDsn = document.getElementsByTagName('html')[0].getAttribute('data-sentry-dsn');

        // Configure Sentry SDK
        if (sentryDsn) {
            Sentry.init({
                dsn: sentryDsn ,
                sampleRate: 0.10,
                ignoreErrors: [
                    'https://plugin.ucads.ucweb.com/api/flow/',
                    'Non-Error promise rejection captured with value' // issue 10380
                ],
                allowUrls: [
                    '/media/js/',
                    'https://www.googletagmanager.com/',
                    'https://www.google-analytics.com/',
                    'https://cdn-3.convertexperiments.com/'

                ]
            });
        }
    }

})();
