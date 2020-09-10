/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var directDownloadLink = document.getElementById('direct-download-link');
    var downloadURL;

    // Only auto-start the download if a supported platform is detected.
    if (Mozilla.DownloadThanks.shouldAutoDownload(window.site.platform) && typeof Mozilla.Utils !== 'undefined') {
        downloadURL = Mozilla.DownloadThanks.getDownloadURL(window.site);

        if (downloadURL) {
            // Pull download link from the download button and add to the 'click here' link.
            directDownloadLink.href = downloadURL;

            // Start the platform-detected download a second after DOM ready event.
            // We don't rely on the window load event as we have third-party tracking pixels.
            Mozilla.Utils.onDocumentReady(function() {
                setTimeout(function() {
                    window.location.href = downloadURL;
                }, 1000);
            });
        }
    }

    // Bug 1354334 - add a hint for test automation that page has loaded.
    document.getElementsByTagName('html')[0].classList.add('download-ready');

})();
