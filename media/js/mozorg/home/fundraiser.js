// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

(function(Mozilla) {
    'use strict';

    var fundraiser = document.getElementById('fundraiser');
    var fundraiserClose = document.getElementById('fundraiser-close');
    var cookieDurationDays = 1;
    var cookiesOK = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();
    var storageKey = 'fundraiser-jun2019';
    var wasClosed = false;

    // see if visitor previously dismissed the banner
    if (cookiesOK) {
        wasClosed = Mozilla.Cookies.getItem(storageKey);
    }

    if (!wasClosed) {
        // show the banner
        fundraiser.style.display = 'block';

        // wire up close button
        fundraiserClose.addEventListener('click', function() {
            var d;

            fundraiser.parentNode.removeChild(fundraiser);

            if (cookiesOK) {
                d = new Date();
                d.setTime(d.getTime() + (cookieDurationDays * 24 * 60 * 60 * 1000)); // 1 day expiration
                Mozilla.Cookies.setItem(storageKey, true, d.toUTCString(), '/');
            }
        }, false);
    }

})(window.Mozilla);