/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    var $masthead_download_firefox = $('#masthead-download-firefox');

    // if Firefox
    if (isFirefox()) {
        // hide the top nav download button
        $masthead_download_firefox.hide();
        $('#download-wrapper').hide();
        $('#subscribe-wrapper').removeClass('columned');
        $('#overview-intro-download-wrapper').hide();

        // hide the footer download button and extend email form to full width

    // if not IE and not Firefox, top nav download button can link directly
    // to scene 2 of /firefox/new/
    } else if (!isFirefox() && navigator.appVersion.indexOf('MSIE') === -1) {
        $masthead_download_firefox.attr('href', $masthead_download_firefox.attr('href') + '#download-fx');
    }
})(window.jQuery);
