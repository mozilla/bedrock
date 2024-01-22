/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    let timeout;

    function isDefaultBrowser() {
        return new window.Promise((resolve, reject) => {
            window.Mozilla.UITour.getConfiguration('appinfo', (details) => {
                if (details.defaultBrowser) {
                    resolve();
                } else {
                    reject();
                }
            });
        });
    }

    function showDefault() {
        clearTimeout(timeout);
        document.querySelector('.wnp-loading').classList.add('hide');
        document.querySelector('.is-not-default').classList.add('hide');
        document.querySelector('.is-default').classList.add('show');

        // UA
        window.dataLayer.push({
            event: 'non-interaction',
            eAction: 'whatsnew-122',
            eLabel: 'firefox-default'
        });

        // GA4
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_default: true
        });
    }

    function showNotDefault() {
        clearTimeout(timeout);
        document.querySelector('.wnp-loading').classList.add('hide');
        document.querySelector('.is-default').classList.add('hide');
        document.querySelector('.is-not-default').classList.add('show');

        // UA
        window.dataLayer.push({
            event: 'non-interaction',
            eAction: 'whatsnew-122',
            eLabel: 'firefox-not-default'
        });

        // GA4
        window.dataLayer.push({
            event: 'dimension_set',
            firefox_is_default: false
        });
    }

    function initDefault() {
        // show not default CTA after 2 seconds as a fallback.
        timeout = window.setTimeout(showNotDefault, 2000);

        isDefaultBrowser().then(showDefault).catch(showNotDefault);
    }

    if (
        typeof window.Mozilla.Client !== 'undefined' &&
        typeof window.Mozilla.UITour !== 'undefined' &&
        window.Mozilla.Client.isFirefoxDesktop
    ) {
        initDefault();
    } else {
        // Fall back to the 'see more' button if other checks fail
        document.querySelector('.wnp-loading').classList.add('hide');
        document.querySelector('.is-not-default').classList.add('hide');
        document.querySelector('.is-default').classList.add('show');
    }
})();
