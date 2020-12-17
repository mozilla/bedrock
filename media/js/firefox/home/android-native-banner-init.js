// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

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

    // This is a slightly modified version of mozilla-banner.js that inserts the banner
    // right to the top of the viewport instead of in-page.
    var NativeBanner = {};

    NativeBanner.setCookie = function(id) {
        var date = new Date();
        var cookieDuration = 1 * 24 * 60 * 60 * 1000; // 1 day expiration
        date.setTime(date.getTime() + cookieDuration); // 1 day expiration
        Mozilla.Cookies.setItem(id, true, date.toUTCString(), '/');
    };

    NativeBanner.hasCookie = function(id) {
        return Mozilla.Cookies.hasItem(id);
    };

    NativeBanner.close = function() {
        // Remove the banner from the DOM.
        _pageBanner.parentNode.removeChild(_pageBanner);

        // Set a cookie to not display it again.
        NativeBanner.setCookie(NativeBanner.id);

        // Track the event in GA.
        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eLabel': 'Banner Dismissal',
            'data-banner-name': NativeBanner.id,
            'data-banner-dismissal': '1'
        });
    };

    NativeBanner.show = function() {
        // remove banner from bottom of page and reinsert at the top of the page, above the main navigation.
        _pageBanner = _pageBanner.parentNode.removeChild(_pageBanner);
        document.body.insertBefore(_pageBanner, document.body.firstChild);

        // display the banner
        _pageBanner.classList.add('c-banner-is-visible');

        // wire up close button
        _pageBanner.querySelector('.c-banner-close').addEventListener('click', NativeBanner.close, false);
    };

    NativeBanner.init = function(id) {
        var cookiesEnabled = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();

        _pageBanner = document.getElementById(id);

        /**
         * If the banner does not exist on a page,
         * or there's not a valid banner ID then do nothing.
         */
        if (!_pageBanner || typeof id !== 'string') {
            return false;
        }

        NativeBanner.id = id;

        // Show only if cookies enabled & banner not previously dismissed.
        if (cookiesEnabled && !NativeBanner.hasCookie(NativeBanner.id)) {
            NativeBanner.show();
        }
    };

    window.Mozilla.NativeBanner = NativeBanner;

})();


(function() {
    'use strict';

    function onLoad() {
        window.Mozilla.NativeBanner.init('native-android-banner');
    }

    window.Mozilla.run(onLoad);

})();
