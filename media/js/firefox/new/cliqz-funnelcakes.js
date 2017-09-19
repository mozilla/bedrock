/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    // TODO: verify these are the funnelcakes with a custom privacy policy link
    var cliqzFunnelcakesNewPrivacyPolicy = '121|122';
    var hasFunnelcake = /^.*\?.*f=(\d{3}).*/.exec(window.location.search);
    var theFunnelcake = (hasFunnelcake && hasFunnelcake.length > 1) ? hasFunnelcake[1] : null;
    var privacyLink;

    // if currently on one of the pre-selected funnelcakes, we need to link to a
    // different privacy policy
    if (cliqzFunnelcakesNewPrivacyPolicy.indexOf(theFunnelcake) > -1) {
        privacyLink = $('.fx-privacy-link a');
        // TODO: the google doc also has a link to an english version of this
        // page (https://www.mozilla.org/en-US/privacy/firefox-cliqz/), but i'm
        // not sure why we'd need that if we're restricting this test to both
        // de locale and geo.
        privacyLink.attr('href', '/de/privacy/firefox-cliqz/');
    }
})(window.jQuery);
