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
            document.querySelector('.wnp-main-cta').classList.add('hide');
            document.querySelector('.wnp-alt-msg').classList.add('show');

            window.dataLayer.push({
                event: 'non-interaction',
                eAction: 'whatsnew-103',
                eLabel: 'firefox-default'
            });
        })
        .catch(function () {
            window.dataLayer.push({
                event: 'non-interaction',
                eAction: 'whatsnew-103',
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
}
