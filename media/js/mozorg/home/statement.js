/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Mozilla) {
    'use strict';

    var $promo = $('#promo-statement');
    var cookieDurationDays = 2;
    var cookiesOK = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();
    var storageKey = 'statement-04-2018';
    var wasClosed = false;
    var evtNamespace = 'promo-statement';
    var $doc = $(window.document);

    // see if visitor previously dismissed the banner
    if (cookiesOK) {
        wasClosed = Mozilla.Cookies.getItem(storageKey);
    }

    if (!wasClosed) {
        // show the banner
        $promo.css('display', 'block');

        // close with escape key
        $doc.on('keyup.' + evtNamespace, function(e) {
            if (e.keyCode === 27) {
                promoClose();
            }
        });

        // close with close button
        $('#promo-close').one('click', function() {
            promoClose();
        });
    }

    function promoClose() {
        var d;

        // unbind document listeners
        $doc.off('.' + evtNamespace);

        $promo.remove();

        if (cookiesOK) {
            d = new Date();
            d.setTime(d.getTime() + (cookieDurationDays * 24 * 60 * 60 * 1000)); // 2 day expiration
            Mozilla.Cookies.setItem(storageKey, true, d.toUTCString(), '/');
        }
    }

})(window.jQuery, window.Mozilla);
