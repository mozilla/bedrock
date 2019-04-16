/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var $platformLink = $('#download-button-wrapper-desktop .download-list li:visible .download-link');
    var directDownloadLink = document.getElementById('direct-download-link');
    var continueDownloadLink = document.getElementById('continue-download-direct');
    var downloadURL;

    function startDownload() {
        if (downloadURL) {
            window.location.href = downloadURL;
        }
    }

    function showNewsletterThankYouMessage() {
        document.querySelector('.thank-you-download .newsletter-download').style.display = 'block';
    }

    function showMobileButtons() {
        document.querySelector('.thank-you-download .mobile-download').style.display = 'block';
    }

    function showThankYouMessage() {
        // Hide all the things.
        document.querySelector('.content-main .headline').classList.add('hidden');
        document.querySelector('.content-main .tagline').classList.add('hidden');
        document.querySelector('.mzp-c-newsletter').style.display = 'none';
        document.querySelector('.mzp-c-newsletter-thanks').style.display = 'none';

        // Show thank you message.
        document.querySelector('.thank-you-download').classList.remove('hidden');

        // Hide this last of all, should any unforseen error occur.
        continueDownloadLink.style.display = 'none';

        // Start the download.
        startDownload();
    }

    // Only auto-start the download if a visible platform link is detected.
    if ($platformLink.length) {
        downloadURL = $platformLink.attr('href');

        // Pull download link from the download button and add to the 'Continue Firefox Download' link.
        continueDownloadLink.setAttribute('href', downloadURL);

        // Pull download link from the download button and add to the 'Try downloading again link.
        directDownloadLink.setAttribute('href', downloadURL);

        // Listen for the newsletter sucess event
        document.addEventListener('newsletterSuccess', function() {
            showThankYouMessage();
            showNewsletterThankYouMessage();
        }, false);

        continueDownloadLink.addEventListener('click', function(e) {
            e.preventDefault();
            showThankYouMessage();
            showMobileButtons();
        }, false);
    }

    // Bug 1354334 - add a hint for test automation that page has loaded.
    document.getElementsByTagName('html')[0].classList.add('download-ready');
})();
