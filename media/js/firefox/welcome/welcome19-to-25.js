/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    const firefoxReleaseCTA = document.getElementById('update-firefox');
    const firefoxEsrCTA = document.getElementById('update-firefox-esr');

    Mozilla.UITour.getConfiguration('appinfo', function (details) {
        if (details.defaultUpdateChannel === 'esr') {
            firefoxEsrCTA.style.display = 'block';
            firefoxReleaseCTA.style.display = 'none';
        }
    });
})();
