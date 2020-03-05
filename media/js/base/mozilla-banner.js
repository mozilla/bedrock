// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    var _fundraiser;

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
        _fundraiser.parentNode.removeChild(_fundraiser);

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
        // display the banner
        _fundraiser.classList.add('c-banner-is-visible');

        // wire up close button
        document.getElementById('page-banner-close').addEventListener('click', Banner.close, false);
    };

    Banner.init = function(id) {
        var cookiesEnabled = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();

        _fundraiser = document.getElementById('page-banner');

        /**
         * If the banner does not exist on a page,
         * or there's not a valid banner ID then do nothing.
         */
        if (!_fundraiser || typeof id !== 'string') {
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
