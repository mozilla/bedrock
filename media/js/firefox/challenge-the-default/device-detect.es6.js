/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MzpNotification from '@mozilla-protocol/core/protocol/js/notification-bar';

const compareTable = document.querySelector('.comparison-table');
const setDefaultButtons = document.querySelectorAll('.is-not-default');
let timer;

function detectDevice() {
    const ua = navigator.userAgent;
    if (/MSIE|Trident/i.test(ua)) {
        return 'edge';
    }

    if (/Edg|Edge/i.test(ua)) {
        return 'edge';
    }

    if (/Chrome/.test(ua)) {
        return 'chrome';
    }

    // got this far without picking, now choose based on OS
    // could be Firefox/Safari/Brave/Opera/Android Browser/etc.

    if (/osx/.test(window.site.platform)) {
        return 'safari';
    }

    if (/windows/.test(window.site.platform)) {
        return 'edge';
    }

    if (/android/.test(window.site.platform)) {
        return 'chrome';
    }
}
const browser = detectDevice();
compareTable.dataset.selectedBrowser = browser;

// Pulled A lot of the functions here from firefox/set-as-default/thanks.js
// but needed to use them slightly differently
function isSupported() {
    return Mozilla.Client.isFirefoxDesktop && 'Promise' in window;
}

function isDefaultBrowser() {
    return new window.Promise(function (resolve, reject) {
        Mozilla.UITour.getConfiguration('appinfo', function (details) {
            if (details.defaultBrowser) {
                resolve(details);
            } else {
                reject(details.canSetDefaultBrowserInBackground);
            }
        });
    });
}

// only add the class to <main> if it isn't already there.
function onDefaultSwitch(e) {
    if (
        !document.querySelector('main').classList.contains('is-firefox-default')
    ) {
        document.querySelector('main').classList.add('is-firefox-default');
    }
    MzpNotification.init(
        e.target,
        {
            title: 'Du hast entschieden, was Standard ist',
            hasDismiss: true,
            isSticky: true,
            className: 'mzp-t-success'
        },
        false
    );
}

function checkForDefaultSwitch(e) {
    isDefaultBrowser()
        .then(function () {
            onDefaultSwitch(e);
            clearInterval(timer);
        })
        .catch(function () {
            // do nothing.
        });
}

function trySetDefaultBrowser() {
    Mozilla.UITour.setConfiguration('defaultBrowser');
}

// check, on load if firefox is already the default browser
window.addEventListener('load', function () {
    if (isSupported()) {
        const main = document.querySelector('main');
        main.classList.add('set-default-supported');
        isDefaultBrowser().then(function () {
            main.classList.add('is-firefox-default');
        });
    }
});

for (let index = 0; index < setDefaultButtons.length; index++) {
    const button = setDefaultButtons[index];
    button.addEventListener('click', function (e) {
        isDefaultBrowser().then((details) => {
            if (details.canSetDefaultBrowserInBackground) {
                trySetDefaultBrowser();
                onDefaultSwitch(e);
            } else {
                window.setTimeout(function () {
                    trySetDefaultBrowser();
                    timer = setInterval(checkForDefaultSwitch(e), 1000);
                }, 1500);
            }
        });
    });
}
