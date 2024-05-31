/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// Log account status
Mozilla.Client.getFxaDetails((details) => {
    'use strict';

    if (details.setup) {
        // UA
        window.dataLayer.push({
            event: 'non-interaction',
            eAction: 'whatsnew-127',
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
            eAction: 'whatsnew-127',
            eLabel: 'firefox-signed-out'
        });

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
        // UA
        window.dataLayer.push({
            event: 'non-interaction',
            eAction: 'whatsnew-127',
            eLabel: 'firefox-default'
        });

        // GA4
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_default: true
        });
    } else {
        // UA
        window.dataLayer.push({
            event: 'non-interaction',
            eAction: 'whatsnew-127',
            eLabel: 'firefox-not-default'
        });

        // GA4
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_default: false
        });
    }
});

function isDefaultBrowser() {
    'use strict';
    return new window.Promise(function (resolve, reject) {
        window.Mozilla.UITour.getConfiguration('appinfo', function (details) {
            if (details.defaultBrowser) {
                resolve();
            } else {
                reject();
            }
        });
    });
}

function initDefault() {
    'use strict';

    isDefaultBrowser()
        .then(function () {
            document.querySelector('.wnp-main-cta').classList.add('hide');
        })
        .catch(function () {
            document.querySelector('.wnp-main-cta').classList.add('show');
        });
}

if (
    typeof window.Mozilla.Client !== 'undefined' &&
    typeof window.Mozilla.UITour !== 'undefined' &&
    window.Mozilla.Client.isFirefoxDesktop
) {
    initDefault();
} else {
    // Hide the make default button if other checks fail
    document.querySelector('.wnp-default').classList.add('hide');
}
