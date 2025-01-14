/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function defaultTrue() {
    document.querySelector('.wnp-loading').classList.add('hide');
    document.querySelector('.wnp-default').classList.add('hide');
    document.querySelector('.wnp-editor').classList.add('show');

    // UA
    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-135-na',
        eLabel: 'default-true'
    });

    // GA4
    window.dataLayer.push({
        event: 'dimension_set',
        firefox_is_default: true
    });
}

function defaultFalse() {
    document.querySelector('.wnp-loading').classList.add('hide');
    document.querySelector('.wnp-editor').classList.add('hide');
    document.querySelector('.wnp-default').classList.add('show');

    // UA
    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-135-na',
        eLabel: 'default-false'
    });

    // GA4
    window.dataLayer.push({
        event: 'dimension_set',
        firefox_is_default: false
    });
}

function init() {
    // If UITour is slow to respond, fallback to assuming Fx is not default.
    const requestTimeout = window.setTimeout(defaultFalse, 2000);

    Mozilla.UITour.getConfiguration('appinfo', function (details) {
        // Clear timeout as soon as we get a response.
        window.clearTimeout(requestTimeout);

        // If Firefox is already the default, show alternate call to action.
        if (details.defaultBrowser) {
            defaultTrue();
            return;
        }

        defaultFalse();
    });

    // Log account status
    Mozilla.Client.getFxaDetails((details) => {
        if (details.setup) {
            // UA
            window.dataLayer.push({
                event: 'non-interaction',
                eAction: 'whatsnew-135-na',
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
                eAction: 'whatsnew-135-na',
                eLabel: 'firefox-signed-out'
            });

            // GA4
            window.dataLayer.push({
                event: 'dimension_set',
                firefox_is_signed_in: false
            });
        }
    });
}

if (
    typeof window.Mozilla.Client !== 'undefined' &&
    typeof window.Mozilla.UITour !== 'undefined' &&
    window.Mozilla.Client.isFirefoxDesktop
) {
    init();
} else {
    // Fall back to PDF editor page if other checks fail
    document.querySelector('.wnp-loading').classList.add('hide');
    document.querySelector('.wnp-default').classList.add('hide');
    document.querySelector('.wnp-editor').classList.add('show');
}
