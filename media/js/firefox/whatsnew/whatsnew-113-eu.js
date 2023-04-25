/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function fxaSignedIn() {
    'use strict';

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-113-eu',
        eLabel: 'fxa-signed-in'
    });
}

function fxaSignedOut() {
    'use strict';

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-113-eu',
        eLabel: 'fxa-signed-out'
    });
}

function init() {
    'use strict';

    // If UITour is slow to respond, fallback to assuming Fx is not default.
    const requestTimeout = window.setTimeout(fxaSignedOut, 2000);

    Mozilla.UITour.getConfiguration(
        'fxa',
        (details) => {
            // Clear timeout as soon as we get a response.
            window.clearTimeout(requestTimeout);

            if (details && details.setup) {
                fxaSignedIn();
            } else {
                fxaSignedOut();
            }
        },
        false
    );
}

if (
    typeof window.Mozilla.Client !== 'undefined' &&
    typeof window.Mozilla.UITour !== 'undefined' &&
    window.Mozilla.Client.isFirefoxDesktop
) {
    init();
}
