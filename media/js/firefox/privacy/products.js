/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var client = Mozilla.Client;

    function handleOpenProtectionReport(e) {
        e.preventDefault();
        Mozilla.UITour.showProtectionReport();

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'See what Firefox has blocked for you'
        });
    }

    if (client.isFirefoxDesktop) {
        if (client._getFirefoxMajorVersion() >= 70) {
            // show "See what Firefox has blocked for you" links.
            document.querySelector('main').classList.add('state-firefox-desktop-70');

            // Intercept link clicks to open about:protections page using UITour.
            Mozilla.UITour.ping(function() {
                var protectionReportLinks = document.querySelectorAll('.js-open-about-protections');
                var pictoCardTitles = document.querySelectorAll('.privacy-products-etp .mzp-c-card-picto-title');

                for (var i = 0; i < protectionReportLinks.length; i++) {
                    // Hide the fallback SUMO linke.
                    protectionReportLinks[i].href = 'about:protections';
                    protectionReportLinks[i].addEventListener('click', handleOpenProtectionReport, false);
                }

                for (var j = 0; j < pictoCardTitles.length; j++) {
                    // Make picto card titles click and keyboard accessible.
                    pictoCardTitles[j].setAttribute('role', 'link');
                    pictoCardTitles[j].setAttribute('tabindex', 0);
                    pictoCardTitles[j].addEventListener('click', handleOpenProtectionReport, false);
                    pictoCardTitles[j].addEventListener('keydown', function(e) {
                        if (e.key === 'Enter') {
                            e.preventDefault();
                            handleOpenProtectionReport(e);
                        }
                    });
                }
            });
        } else {
            // show "Update your Firefox browser" links.
            document.querySelector('main').classList.add('state-firefox-desktop-old');
        }
    }

})(window.Mozilla);
