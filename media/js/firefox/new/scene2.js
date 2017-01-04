/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var isIELT9 = window.Mozilla.Client.platform === 'windows' && /MSIE\s[1-8]\./.test(navigator.userAgent);
    var $directDownloadLink = $('#direct-download-link');
    var $platformLink = $('#download-button-wrapper-desktop .download-list li:visible .download-link');
    var downloadURL;

    if ($platformLink.length) {
        downloadURL = $platformLink.attr('href');

        // Pull download link from the download button and add to the 'click here' link.
        // TODO: Remove and generate link in bedrock.
        $directDownloadLink.attr('href', downloadURL);

        // if user is not on an IE that blocks JS triggered downloads, start the
        // platform-detected download after window (read: images) have loaded.
        // only auto-start the download if a visible platform link is detected.
        if (!isIELT9) {
            $(window).on('load', function() {
                window.location.href = downloadURL;
            });
        }
    }

})(window.jQuery);
