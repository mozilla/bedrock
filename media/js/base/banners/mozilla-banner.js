// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    var _pageBanner;

    var Banner = {};

    Banner.setCookie = function(id) {
        var date = new Date();
        var cookieDuration = 1 * 24 * 60 * 60 * 1000; // 1 day expiration
        date.setTime(date.getTime() + cookieDuration); // 1 day expiration
        Mozilla.Cookies.setItem(id, true, date.toUTCString(), '/');
    };

    Banner.hasCookie = function(id) {
        return Mozilla.Cookies.hasItem(id);
    };

    Banner.close = function() {
        // Remove the banner from the DOM.
        _pageBanner.parentNode.removeChild(_pageBanner);

        // Set a cookie to not display it again.
        Banner.setCookie(Banner.id);

        // Track the event in GA.
        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eLabel': 'Banner Dismissal',
            'data-banner-name': Banner.id,
            'data-banner-dismissal': '1'
        });
    };

    Banner.show = function() {
        var outerWrapper = document.getElementById('outer-wrapper');

        // if for some reason there's no outer-wrapper on the page, do nothing.
        if (!outerWrapper) {
            return;
        }

        // remove banner from bottom of page and reinsert at the top, after primary nav.
        _pageBanner = _pageBanner.parentNode.removeChild(_pageBanner);
        outerWrapper.insertBefore(_pageBanner, outerWrapper.firstChild);

        // display the banner
        _pageBanner.classList.add('c-banner-is-visible');

        // wire up close button
        _pageBanner.querySelector('.c-banner-close').addEventListener('click', Banner.close, false);
    };

    Banner.init = function(id) {
        var cookiesEnabled = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();

        _pageBanner = document.getElementById(id);

        /**
         * If the banner does not exist on a page,
         * or there's not a valid banner ID then do nothing.
         */
        if (!_pageBanner || typeof id !== 'string') {
            return false;
        }

        Banner.id = id;

        // Show only if cookies enabled & banner not previously dismissed.
        if (cookiesEnabled && !Banner.hasCookie(Banner.id)) {
            Banner.show();
        }
    };

    window.Mozilla.Banner = Banner;

})();
