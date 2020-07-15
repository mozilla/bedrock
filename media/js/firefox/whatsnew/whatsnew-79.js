/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var client = Mozilla.Client;

    Mozilla.UITour.getConfiguration('appinfo', function(details) {
        if (details.defaultBrowser) {
            document.querySelector('body').classList.add('is-firefox-default');
        }
    });

    function handleOpenProtectionReport(e) {
        e.preventDefault();
        Mozilla.UITour.showProtectionReport();

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'See your Report'
        });
    }

    if (client.isFirefoxDesktop) {
        if (client._getFirefoxMajorVersion() >= 70) {
            // show "See what Firefox has blocked for you" links.
            document.querySelector('main').classList.add('state-firefox-desktop-70');

            // Intercept link clicks to open about:protections page using UITour.
            Mozilla.UITour.ping(function() {
                var protectionReportLinks = document.querySelectorAll('.js-open-about-protections');

                // For UI Tour CTAs, we will treat these more as an action rather than a page navigation.
                for (var i = 0; i < protectionReportLinks.length; i++) {
                    // Hide fallback links.
                    protectionReportLinks[i].addEventListener('click', handleOpenProtectionReport, false);
                }
            });
        } else {
            // show "Update your Firefox browser" links.
            document.querySelector('main').classList.add('state-firefox-desktop-old');
        }
    }

    // modal
    var content = document.querySelector('.mzp-u-modal-content');
    var trigger = document.querySelector('.js-modal-link');

    trigger.addEventListener('click', function(e) {
        e.preventDefault();
        Mzp.Modal.createModal(this, content, {
            closeText: window.Mozilla.Utils.trans('global-close'),
        });

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'Get Firefox for mobile'
        });
    }, false);

    // initialize send to device widget
    var form = new Mozilla.SendToDevice();
    form.init();

})(window.Mozilla);
