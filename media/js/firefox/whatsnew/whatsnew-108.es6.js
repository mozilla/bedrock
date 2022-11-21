/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const POCKET_WEB_OAUTH_CLIENT_ID = '749818d3f2e7857f';

function showDefault() {
    document.querySelector('.js-default-cta').classList.add('show');
    document.querySelector('.js-alt-cta').classList.remove('show');

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-108',
        eLabel: 'pocket-false'
    });
}

function showAlt() {
    document.querySelector('.js-default-cta').classList.remove('show');
    document.querySelector('.js-alt-cta').classList.add('show');

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-108',
        eLabel: 'pocket-true'
    });
}

function init() {
    // If UITour is slow to respond, fallback to showing the default CTA after 2 seconds.
    const requestTimeout = window.setTimeout(showDefault, 2000);

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
                showAlt();
                return;
            }
        }

        // Else show the default call to action.
        showDefault();
    });
}

// Only initialize UITour on Firefox desktop.
if (
    typeof window.Mozilla.Client !== 'undefined' &&
    window.Mozilla.Client.isFirefoxDesktop
) {
    init();
} else {
    showDefault();
}
