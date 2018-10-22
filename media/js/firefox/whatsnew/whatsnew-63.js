/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var client = Mozilla.Client;

    function checkUpToDate() {
        // bug 1419573 - only show "Your Firefox is up to date" if it's the latest version.
        if (client.isFirefoxDesktop) {
            client.getFirefoxDetails(function(data) {
                if (data.isUpToDate) {
                    document.querySelector('.c-page-header').classList.add('is-up-to-date');
                }
            });
        }
    }

    function bindOpenPrefs() {
        document.getElementById('privacy-prefs-link').addEventListener('click', function(e) {
            e.preventDefault();

            Mozilla.UITour.openPreferences('privacy');
        }, false);
    }

    Mozilla.UITour.ping(function() {
        checkUpToDate();
        bindOpenPrefs();
    });

})();
