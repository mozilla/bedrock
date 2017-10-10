/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var cliqzFunnelcakesNewPrivacyPolicy = '121|122';
    var funnelcakeId = $('main').data('funnelcakeId');
    var privacyLink;

    // if currently on one of the pre-selected funnelcakes, we need to link to a
    // different privacy policy
    if (funnelcakeId && cliqzFunnelcakesNewPrivacyPolicy.indexOf(funnelcakeId) > -1) {
        privacyLink = $('.fx-privacy-link a');
        privacyLink.attr('href', '/de/privacy/firefox-cliqz/');
    }
})(window.jQuery);
