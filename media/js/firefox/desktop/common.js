/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $masthead_download_firefox = $('#masthead-download-firefox');
    var $html = $('html');

    // only show download buttons for users on desktop platforms, using either a non-Firefox browser
    // or an out of date version of Firefox
    if ((!isFirefox() || !isFirefoxUpToDate()) && !$html.hasClass('android') && !$html.hasClass('ios') && !$html.hasClass('fxos')) {
        // if not IE, top nav download button can link directly to scene 2 of /firefox/new/
        if (navigator.appVersion.indexOf('MSIE') === -1) {
            $masthead_download_firefox.attr('href', $masthead_download_firefox.attr('href') + '#download-fx');
        }

        var trackDownloadButtonClick = function(a, position) {
            var href = a.href;

            gaTrack(['_trackEvent', 'Firefox Downloads', 'download click - ' + position, 'Firefox for Desktop'], function() {
                window.location = href;
            });
        };

        // hide the footer download button and extend email form to full width
        $('#download-wrapper').show();
        $('#subscribe-wrapper').addClass('columned');

        // show the download button on the overview page intro section
        $('#overview-intro-download-wrapper').fadeIn('fast');

        // show the top nav download button and set up GA tracking
        $masthead_download_firefox.fadeIn('fast').on('click', function(e) {
            e.preventDefault();

            trackDownloadButtonClick(this, 'nav');
        });

        // Track Firefox download click in overview intro section
        $('#firefox-desktop #intro .download-link').on('click', function(e) {
            e.preventDefault();

            trackDownloadButtonClick(this, 'primary');
        });

        // Track Firefox download click in footer
        $('#subscribe-download-wrapper .download-link').on('click', function(e) {
            e.preventDefault();

            trackDownloadButtonClick(this, 'bottom');
        });
    }

    // set up common GA tracking
    var trackOutboundLink = function(a) {
        var href = a.href;

        gaTrack(['_trackEvent', 'firefox/desktop/ Interactions', 'outbound link', href], function() {
            window.location = href;
        });
    };

    $('.ga-section').waypoint(function(dir) {
        // only track scrolling down
        if (dir === 'down') {
            gaTrack(['_trackEvent', 'firefox/desktop/ Interactions', 'scroll', $(this).data('ga-label')]);
        }
    }, {
        offset: 100
    });

    $('a[rel="external"]').on('click', function(e) {
        e.preventDefault();

        trackOutboundLink(this);
    });

    $('.ga-track-links a').on('click', function(e) {
        e.preventDefault();

        trackOutboundLink(this);
    });
})(window.jQuery);
