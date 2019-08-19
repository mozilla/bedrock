/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $directDownloadLink = $('#direct-download-link');
    var $platformLink = $('#download-button-wrapper-desktop .download-list li:visible .download-link');
    var downloadURL;

    // Bug 1354334 - add a hint for test automation that page has loaded.
    $('html').addClass('download-ready');

    // Only auto-start the download if a visible platform link is detected.
    if ($platformLink.length) {
        downloadURL = $platformLink.attr('href');

        // Pull download link from the download button and add to the 'click here' link.
        // TODO: Remove and generate link in bedrock.
        $directDownloadLink.attr('href', downloadURL);

        // Start the platform-detected download a second after DOM ready event.
        // We don't rely on the window load event as we have third-party tracking pixels.
        $(function() {
            setTimeout(function() {
                window.location.href = downloadURL;
            }, 1000);
        });
    }

})(window.jQuery);
