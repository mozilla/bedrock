/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var isIELT9 = window.Mozilla.Client.platform === 'windows' && /MSIE\s[1-8]\./.test(navigator.userAgent);
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

        // If user is not on an IE that blocks JS triggered downloads, start the
        // platform-detected download a second after DOM ready event. We don't rely on
        // the window load event as we have third-party tracking pixels.
        if (!isIELT9) {
            $(function() {
                setTimeout(function() {
                    window.location.href = downloadURL;
                }, 1000);
            });
        }
    }

    var $modalWrapper = $('.email-privacy');
    var $modalLink = $('.email-privacy-link');

    $modalLink.on('click', function(e) {
        e.preventDefault();
        Mozilla.Modal.createModal(this, $modalWrapper, {
            title: $(this).text()
        });

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'How will Mozilla use my email?'
        });
    });

})(window.jQuery);
