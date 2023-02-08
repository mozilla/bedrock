/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function defaultTrue() {
    'use strict';

    document.querySelector('.wnp-loading').classList.add('hide');
    document.querySelector('.wnp-default').classList.add('hide');
    document.querySelector('.wnp-mobile').classList.add('show');

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-110-en',
        eLabel: 'default-true'
    });
}

function defaultFalse() {
    'use strict';

    document.querySelector('.wnp-loading').classList.add('hide');
    document.querySelector('.wnp-mobile').classList.add('hide');
    document.querySelector('.wnp-default').classList.add('show');

    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'whatsnew-110-en',
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
}

if (
    typeof window.Mozilla.Client !== 'undefined' &&
    typeof window.Mozilla.UITour !== 'undefined' &&
    window.Mozilla.Client.isFirefoxDesktop
) {
    init();
} else {
    // Fall back to mobile page if other checks fail
    document.querySelector('.wnp-loading').classList.add('hide');
    document.querySelector('.wnp-default').classList.add('hide');
    document.querySelector('.wnp-mobile').classList.add('show');
}
