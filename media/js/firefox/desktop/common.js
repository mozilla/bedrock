/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(w, $) {
    'use strict';

    var client = w.Mozilla.Client;

    var $mastheadDownloadFirefox = $('#masthead-download-firefox');
    var $html = $('html');

    function showDownloadButtons() {
        // if not IE, top nav download button can link directly to scene 2 of /firefox/new/
        if (navigator.appVersion.indexOf('MSIE') === -1) {
            $mastheadDownloadFirefox.attr('href', $mastheadDownloadFirefox.attr('href') + '#download-fx');
        }

        var downloadVersion = 'Firefox for Desktop';
        // hide the footer download button and extend email form to full width
        $('#download-wrapper').show();
        $('#subscribe-wrapper').addClass('columned');

        // show the download button on the overview page intro section
        $('#overview-intro-download-wrapper').fadeIn('fast');

        // show download button in sticky nav on overview page
        $('#sticky-download-desktop').fadeIn('fast');

        // show the top nav download button and set up GA tracking
        $mastheadDownloadFirefox.attr({'data-interaction': 'download click - nav', 'data-download-version': downloadVersion}).fadeIn('fast');

        // Track clicks on Nav CTA
        $('#sticky-download-desktop .download-link').attr('data-interaction', 'download click - nav');

        // Track Firefox download click in overview intro section
        $('#firefox-desktop #intro .download-link').attr({'data-interaction': 'download click - primary', 'data-download-version': downloadVersion});

        // Track Firefox download click in footer
        $('#subscribe-download-wrapper .download-link').attr({'data-interaction': 'download click - bottom', 'data-download-version': downloadVersion});
    }

    // only show download buttons for users on desktop platforms, using either a non-Firefox browser
    // or an out of date version of Firefox
    if (client.isDesktop) {
        if (client.isFirefox) {
            client.getFirefoxDetails(function(data) {
                if (!data.isUpToDate) {
                    showDownloadButtons();
                }
            });
        } else {
            showDownloadButtons();
        }
    }

    $('.ga-section').waypoint(function(dir) {
        // only track scrolling down

        if (dir === 'down') {
            w.dataLayer.push({
                'event': 'scroll-section',
                'section': $(this.element).data('ga-label')
            });
        }
    }, {
        offset: 100
    });
})(window, window.jQuery);
