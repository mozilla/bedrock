/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

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

function init() {
    'use strict';

    isDefaultBrowser()
        .then(function () {
            document.querySelector('.wnp-loading').classList.add('hide');
            document.querySelector('.wnp-default').classList.add('hide');
            document.querySelector('.wnp-mobile').classList.add('show');

            window.dataLayer.push({
                event: 'non-interaction',
                eAction: 'whatsnew-110-en',
                eLabel: 'firefox-default'
            });
        })
        .catch(function () {
            document.querySelector('.wnp-loading').classList.add('hide');
            document.querySelector('.wnp-mobile').classList.add('hide');
            document.querySelector('.wnp-default').classList.add('show');

            window.dataLayer.push({
                event: 'non-interaction',
                eAction: 'whatsnew-110-en',
                eLabel: 'firefox-not-default'
            });
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
