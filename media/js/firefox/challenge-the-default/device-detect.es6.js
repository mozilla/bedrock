/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const compareTable = document.querySelector('.comparison-table');

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
compareTable.dataset.selectedBrowser = browser || 'chrome';

function isDefaultBrowser() {
    return new window.Promise(function (resolve, reject) {
        Mozilla.UITour.getConfiguration('appinfo', function (details) {
            if (details.defaultBrowser) {
                resolve();
            } else {
                reject();
            }
        });
    });
}

// Pulled A lot of the functions here from firefox/set-as-default/thanks.js
// but needed to use them slightly differently
function isSupported() {
    return Mozilla.Client.isFirefoxDesktop && 'Promise' in window;
}

// check if firefox is already the default browser
if (isSupported()) {
    const main = document.querySelector('main');
    main.classList.add('set-default-supported');
    isDefaultBrowser().then(function () {
        main.classList.add('is-firefox-default');
    });
}
