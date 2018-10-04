/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var client = window.Mozilla.Client;
    var quantum = 57;
    var htmlClassName = document.documentElement.className;

    if(client.isFirefoxDesktop === false || client.FirefoxVersion < quantum) {
        // case-not-firefox-desktop-current
        document.getElementById('case-firefox-desktop-current').classList.add('hidden');
        document.getElementById('case-not-firefox-desktop').classList.remove('hidden');
        if (htmlClassName.indexOf('oldwin') > -1 || htmlClassName.indexOf('oldmac') > -1  || (htmlClassName.indexOf('arm') > -1 ) && htmlClassName.indexOf('android') === -1) {
            // case-unsupported
            document.getElementById('case-unsupported').classList.remove('hidden');
        } else {
            // case-manual
            document.getElementById('case-manual').classList.remove('hidden');

            if(client.isFirefoxDesktop) {
                // case outofdate
                document.getElementById('case-outofdate').classList.remove('hidden');
                document.getElementById('case-download').classList.add('hidden');
            } else if (htmlClassName.indexOf('android') > -1  || htmlClassName.indexOf('ios') > -1 ) {
                // case-mobile
                document.getElementById('case-mobile').classList.remove('hidden');
                document.getElementById('case-download').classList.add('hidden');
            }
        }
    }
})();
