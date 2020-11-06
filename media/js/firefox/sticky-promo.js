/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var StickyPromo = {};
    var stickyPromoCookieID = 'firefoxStickyPromo';

    StickyPromo.setCookie = function() {
        var date = new Date();
        var cookieDuration = 1 * 24 * 60 * 60 * 1000; // 1 day expiration
        date.setTime(date.getTime() + cookieDuration); // 1 day expiration
        Mozilla.Cookies.setItem(stickyPromoCookieID, true, date.toUTCString(), '/');
    };

    StickyPromo.hasCookie = function() {
        return Mozilla.Cookies.hasItem(stickyPromoCookieID);
    };

    StickyPromo.show = function (){
        document.addEventListener('DOMContentLoaded', Mzp.StickyPromo.open);

        // Set Close Button event
        var stickyBtnClose = document.querySelector('.mzp-c-sticky-promo-close');

        stickyBtnClose.addEventListener('click', function(){
            StickyPromo.setCookie(stickyPromoCookieID);
        });
    };

    // Check on page load
    var cookiesEnabled = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();

    if (cookiesEnabled && !StickyPromo.hasCookie()) {
        StickyPromo.show();
    }

})(window.Mozilla);
