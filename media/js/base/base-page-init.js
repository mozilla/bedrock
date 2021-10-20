/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * General DOM ready handler applied to all pages in base template.
 */
(function () {
    'use strict';

    if (typeof Mozilla.Utils !== 'undefined') {
        Mozilla.Utils.onDocumentReady(function () {
            var utils = Mozilla.Utils;

            utils.initMobileDownloadLinks();
            utils.trackDownloadThanksButton();

            /* Bug 1264843: In partner distribution of desktop Firefox, switch the
            downloads to corresponding partner build of Firefox for Android. */
            if (typeof Mozilla.Client !== 'undefined') {
                var client = Mozilla.Client;

                if (client.isFirefoxDesktop) {
                    client.getFirefoxDetails(
                        utils.maybeSwitchToChinaRepackImages
                    );
                }
            }
        });
    }

    // The `loaded` class is used mostly as a signal for functional tests to run.
    window.addEventListener(
        'load',
        function () {
            document.getElementsByTagName('html')[0].classList.add('loaded');
        },
        false
    );
})();
