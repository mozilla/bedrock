/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    var client = Mozilla.Client;

    function handleOpenProtectionReport(e) {
        e.preventDefault();

        window.dataLayer.push({
            event: 'in-page-interaction',
            eAction: 'link click',
            eLabel: 'See what Firefox has blocked for you'
        });

        Mozilla.UITour.showProtectionReport();
    }

    if (client.isFirefoxDesktop) {
        if (client._getFirefoxMajorVersion() >= 70) {
            // show "See what Firefox has blocked for you" links.
            document
                .querySelector('main')
                .classList.add('state-firefox-desktop-70');

            // Intercept link clicks to open about:protections page using UITour.
            Mozilla.UITour.ping(function () {
                var protectionReportLinks = document.querySelectorAll(
                    '.js-open-about-protections'
                );

                for (var i = 0; i < protectionReportLinks.length; i++) {
                    protectionReportLinks[i].addEventListener(
                        'click',
                        handleOpenProtectionReport,
                        false
                    );
                }
            });
        } else {
            // show "Update your Firefox browser" links.
            document
                .querySelector('main')
                .classList.add('state-firefox-desktop-old');
        }
    }
})(window.Mozilla);
