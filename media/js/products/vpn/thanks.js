/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';
    var prefix = 'vpn-download-link-';
    var link;

    // Check for download link on Windows or Mac download pages
    if (document.getElementById(prefix + 'win') !== null) {
        link = document.getElementById(prefix + 'win').href;
    } else if (document.getElementById(prefix + 'mac') !== null) {
        link = document.getElementById(prefix + 'mac').href;
    }

    // Trigger auto-download based on platform page
    Mozilla.Utils.onDocumentReady(function () {
        setTimeout(function () {
            window.location.href = link;
        }, 1000);
    });

    // Bug 1354334 - add a hint for test automation that page has loaded.
    document.getElementsByTagName('html')[0].classList.add('download-ready');
})();
