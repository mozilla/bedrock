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

    if (client.isFirefoxDesktop && client._getFirefoxMajorVersion() >= 70) {
        // Intercept link clicks to open about:protections page using UITour.
        Mozilla.UITour.ping(function() {
            var protectionReportLink = document.querySelector('.js-open-about-protections');
            protectionReportLink.addEventListener('click', handleOpenProtectionReport, false);
        });
    }
})(window.Mozilla);
