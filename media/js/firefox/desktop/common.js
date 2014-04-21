/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

var FirefoxDesktop = window.FirefoxDesktop || {};

(function($) {
    var $masthead_download_firefox = $('#masthead-download-firefox');

    FirefoxDesktop.isDesktopViewport = $(window).width() >= 1000;
    FirefoxDesktop.isSmallViewport = $(window).width() < 760;

    // if not Firefox
    if (!isFirefox()) {
        // show the top nav download button
        $masthead_download_firefox.fadeIn('fast');

        // hide the footer download button and extend email form to full width
        $('#download-wrapper').show();
        $('#subscribe-wrapper').addClass('columned');

        // show the download button on the overview page intro section
        $('#overview-intro-download-wrapper').fadeIn('fast');

        // if not IE, top nav download button can link directly to scene 2 of
        // /firefox/new/
        if (navigator.appVersion.indexOf('MSIE') === -1) {
            $masthead_download_firefox.attr('href', $masthead_download_firefox.attr('href') + '#download-fx');
        }
    }
})(window.jQuery);
