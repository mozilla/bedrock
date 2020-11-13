/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // Check if promo exists on the page or if smaller than tablet.
    var matchMediaDesktop = window.matchMedia('(min-width: 768px)').matches;

    if (!document.querySelector('.mzp-c-sticky-promo') || !matchMediaDesktop) {
        return;
    }

    var StickyPromo = {};
    var STICKY_PROMO_COOKIE_ID = 'firefox-sticky-promo';

    StickyPromo.bindEvents = function() {
        var promo = document.querySelector('.mzp-c-sticky-promo');
        promo.addEventListener('animationend', function() {
            promo.classList.add('is-displayed');
        }, false);
    };

    StickyPromo.hasCookie = function() {
        return Mozilla.Cookies.hasItem(STICKY_PROMO_COOKIE_ID);
    };

    StickyPromo.setCookie = function() {
        var date = new Date();
        var cookieDuration = 1 * 24 * 60 * 60 * 1000; // 1 day expiration
        date.setTime(date.getTime() + cookieDuration); // 1 day expiration
        Mozilla.Cookies.setItem(STICKY_PROMO_COOKIE_ID, true, date.toUTCString(), '/');
    };

    StickyPromo.show = function (){
        // Open promo
        Mzp.StickyPromo.open();

        // Add modifier class to the footer to make sure the language selection drop-down is not obscured by the sticky promo
        var footer = document.querySelector('.mzp-c-footer');
        footer.classList.add('sticky-overlay');

        // Set Close Button event
        var stickyBtnClose = document.querySelector('.mzp-c-sticky-promo-close');

        stickyBtnClose.addEventListener('click', function(){
            StickyPromo.setCookie(STICKY_PROMO_COOKIE_ID);
        });
    };

    // Check on page load
    var cookiesEnabled = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();

    if (cookiesEnabled && !StickyPromo.hasCookie()) {
        StickyPromo.bindEvents();
        StickyPromo.show();
    }

})(window.Mozilla);
