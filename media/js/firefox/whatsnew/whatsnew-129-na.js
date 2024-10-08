/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function defaultTrue() {
    'use strict';

    document.querySelector('.cta-holder').classList.add('hide');
    document.querySelector('.fx-not-default').classList.add('hide');
    document.querySelector('.fx-is-default').classList.add('show');

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-129-na',
        eLabel: 'default-true'
    });
}

function defaultFalse() {
    'use strict';

    document.querySelector('.cta-holder').classList.add('hide');
    document.querySelector('.fx-is-default').classList.add('hide');
    document.querySelector('.fx-not-default').classList.add('show');

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-129-na',
        eLabel: 'default-false'
    });
}

function init() {
    'use strict';

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

    Mozilla.UITour.forceShowReaderIcon();

    // show reader mode icon again on visibility change
    // see https://github.com/mozilla/bedrock/issues/14975
    document.addEventListener(
        'visibilitychange',
        () => {
            if (!document.hidden) {
                Mozilla.UITour.forceShowReaderIcon();
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
} else {
    // Fall back to learn more CTA if other checks fail
    document.querySelector('.cta-holder').classList.add('hide');
    document.querySelector('.fx-not-default').classList.add('hide');
    document.querySelector('.fx-is-default').classList.add('show');
}

// Log account status
Mozilla.Client.getFxaDetails((details) => {
    'use strict';

    if (details.setup) {
        // GA4
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_signed_in: true
        });
    } else {
        // GA4
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_signed_in: false
        });
    }
});

// Log default status
Mozilla.UITour.getConfiguration('appinfo', (details) => {
    'use strict';

    if (details.defaultBrowser) {
        // GA4
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_default: true
        });
    } else {
        // GA4
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_default: false
        });
    }
});
