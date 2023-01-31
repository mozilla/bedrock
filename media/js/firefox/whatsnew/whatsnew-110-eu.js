/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const POCKET_WEB_OAUTH_CLIENT_ID = '749818d3f2e7857f';

function pocketTrue() {
    'use strict';

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-110',
        eLabel: 'pocket-true'
    });
}

function pocketFalse() {
    'use strict';

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-110',
        eLabel: 'pocket-false'
    });
}

function init() {
    'use strict';

    // If UITour is slow to respond, fallback to assuming user does not have pocket.
    const requestTimeout = window.setTimeout(pocketFalse, 2000);

    Mozilla.UITour.getConfiguration('fxaConnections', (data) => {
        // Clear timeout as soon as we get a response.
        window.clearTimeout(requestTimeout);

        // If user has accessed Pocket via FxA, show alternate call to action.
        if (Object.prototype.hasOwnProperty.call(data, 'accountServices')) {
            if (
                Object.prototype.hasOwnProperty.call(
                    data.accountServices,
                    POCKET_WEB_OAUTH_CLIENT_ID
                )
            ) {
                pocketTrue();
                return;
            }
        }

        pocketFalse();
    });
}

// Only initialize UITour on Firefox desktop.
if (
    typeof window.Mozilla.Client !== 'undefined' &&
    window.Mozilla.Client.isFirefoxDesktop
) {
    init();
}
