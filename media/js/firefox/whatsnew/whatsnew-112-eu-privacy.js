/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function defaultTrue() {
    'use strict';

    document.querySelector('.wnp-cta-default').classList.add('hide');
    document.querySelector('.wnp-cta-protections').classList.add('show');

    // Open about:protections using UITour when button is clicked.
    document
        .querySelector('.wnp-cta-protections > .mzp-c-button')
        .addEventListener(
            'click',
            (e) => {
                e.preventDefault();

                Mozilla.UITour.showProtectionReport();

                window.dataLayer.push({
                    event: 'in-page-interaction',
                    eAction: 'button click',
                    eLabel: 'See how Firefox protects you'
                });
            },
            false
        );

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-112-eu',
        eLabel: 'default-true'
    });
}

function defaultFalse() {
    'use strict';

    document.querySelector('.wnp-cta-default').classList.add('show');
    document.querySelector('.wnp-cta-protections').classList.add('hide');

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-112-eu',
        eLabel: 'default-false'
    });
}

function init() {
    'use strict';

    // If UITour is slow to respond, fallback to assuming Fx is not default.
    const requestTimeout = window.setTimeout(defaultFalse, 2000);

    Mozilla.UITour.getConfiguration(
        'appinfo',
        (details) => {
            // Clear timeout as soon as we get a response.
            window.clearTimeout(requestTimeout);

            // If Firefox is already the default, show alternate call to action.
            if (details.defaultBrowser) {
                defaultTrue();
                return;
            }

            defaultFalse();
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
} else {
    document.querySelector('.wnp-cta-default').classList.add('show');
    document.querySelector('.wnp-cta-protections').classList.add('hide');
}
