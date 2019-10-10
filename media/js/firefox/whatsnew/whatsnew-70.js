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

    function handleOpenLockwise(e) {
        e.preventDefault();
        Mozilla.UITour.showHighlight('logins');

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'Update your Firefox browser'
        });
    }

    if (client.isFirefoxDesktop) {
        if (client._getFirefoxMajorVersion() >= 70) {
            // show "See what Firefox has blocked for you" links.
            document.querySelector('main').classList.add('state-firefox-desktop-70');

            // Intercept link clicks to open about:protections page using UITour.
            Mozilla.UITour.ping(function() {
                var protectionReportLinks = document.querySelectorAll('.js-open-about-protections');
                var lockwiseLinks = document.querySelectorAll('.js-open-lockwise');

                // For UI Tour CTAs, we will treat these more as an action rather than a page navigation.
                for (var i = 0; i < protectionReportLinks.length; i++) {
                    // Hide fallback links.
                    protectionReportLinks[i].href = 'about:protections';
                    protectionReportLinks[i].addEventListener('click', handleOpenProtectionReport, false);
                }

                for (var j = 0; j < lockwiseLinks.length; j++) {
                    lockwiseLinks[j].setAttribute('role', 'button');
                    lockwiseLinks[j].addEventListener('click', handleOpenLockwise, false);
                }
            });
        } else {
            // show "Update your Firefox browser" links.
            document.querySelector('main').classList.add('state-firefox-desktop-old');
        }
    }

})(window.Mozilla);
