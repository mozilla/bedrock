/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';
    var prefix = 'vpn-download-link-';
    var win = document.getElementById(prefix + 'win');
    var mac = document.getElementById(prefix + 'mac');
    var link;

    // Check for download link on Windows or Mac download pages
    if (win) {
        link = win.href;
    } else if (mac) {
        link = mac.href;
    }

    // Trigger auto-download based on platform page
    Mozilla.Utils.onDocumentReady(function () {
        setTimeout(function () {
            if (link) {
                window.location.href = link;
            }
        }, 1000);
    });

    // Bug 1354334 - add a hint for test automation that page has loaded.
    document.getElementsByTagName('html')[0].classList.add('download-ready');
})();
