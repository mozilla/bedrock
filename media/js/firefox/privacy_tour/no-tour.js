/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    // enable video
    Mozilla.FirefoxAnniversaryVideo.enableEmbed();

    Mozilla.PrivacyTour.modalEnabled = true;

    // wait until doc ready to start ripples animation
    $(function() {
        Mozilla.PrivacyTour.animateRipples(0);
    });
})(window.jQuery, window.Mozilla);
