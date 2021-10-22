/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    if (
        typeof Mozilla.Client === 'undefined' ||
        typeof Mozilla.UITour === 'undefined'
    ) {
        return;
    }

    var client = Mozilla.Client;

    function checkUpToDate() {
        // bug 1419573 - only show "Congrats! You’re using the latest version of Firefox." if it's the latest version.
        if (client.isFirefoxDesktop) {
            client.getFirefoxDetails(function (data) {
                if (data.isUpToDate) {
                    document
                        .querySelector('.c-page-header')
                        .classList.add('is-up-to-date');
                } else {
                    document
                        .querySelector('.c-page-header')
                        .classList.add('is-out-of-date');
                }
            });
        }
    }

    Mozilla.UITour.ping(function () {
        checkUpToDate();
    });
})();
