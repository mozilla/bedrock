/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FirefoxDefault from '../../base/fx-is-default.es6';

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

// check if firefox is set to default on startup
FirefoxDefault.init('main');
