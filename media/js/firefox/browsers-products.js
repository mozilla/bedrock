/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    // lockwise link opens lockwise menu in Firefox
    var client = window.Mozilla.Client;
    var version = client._getFirefoxMajorVersion();

    if (client.isFirefox && version >= '70') {
        var menuItem = document.getElementById('js-lockwise-desktop');
        if (menuItem !== null) {
            menuItem.classList.remove('hidden');

            var lockwiseButton = document.getElementById('lockwise-button');
            if (lockwiseButton !== null) {
                lockwiseButton.addEventListener('click', function () {
                    Mozilla.UITour.showHighlight('logins');
                });
            }
        }
    }

    // init menus on page
    window.MzpDetails.init('.mzp-c-menu-list-title');
})();
