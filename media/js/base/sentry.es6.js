/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { init } from '@sentry/browser';

// Respect Do Not Track
if (
    typeof window.Mozilla.dntEnabled === 'function' &&
    !window.Mozilla.dntEnabled()
) {
    // Get Data Source Name (DSN)
    const sentryDsn = document
        .getElementsByTagName('html')[0]
        .getAttribute('data-sentry-dsn');

    // Configure Sentry SDK
    if (sentryDsn) {
        init({
            dsn: sentryDsn,
            sampleRate: 0.1,
            ignoreErrors: [
                "SecurityError: Failed to execute 'open' on 'XMLHttpRequest'", // issue 10683
                'NetworkError when attempting to fetch resource', // issue 10683
                'Non-Error promise rejection captured with value' // issue 10380
            ],
            allowUrls: ['/media/js/', 'https://cdn-3.convertexperiments.com/'],
            beforeSend(event) {
                try {
                    // https://github.com/getsentry/sentry-javascript/issues/3147
                    if (
                        event.exception.values[0].stacktrace.frames[0]
                            .filename === '<anonymous>'
                    ) {
                        return null;
                    }
                } catch (e) {
                    // do nothing.
                }

                return event;
            }
        });
    }
}
