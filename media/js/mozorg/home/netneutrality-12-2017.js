(function($, Mozilla) {
    'use strict';

    var $promo = $('#promo-net-neutrality');
    var cookieDurationDays = 2;
    var cookiesOK = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();
    var storageKey = 'netneutrality-12-2017';
    var wasClosed = false;

    // see if visitor previously dismissed the banner
    if (cookiesOK) {
        wasClosed = Mozilla.Cookies.getItem(storageKey);
    }

    if (!wasClosed) {
        // show the banner
        $promo.css('display', 'block');

        // wire up close button
        $('#promo-close').one('click', function() {
            var d;

            $promo.remove();

            if (cookiesOK) {
                d = new Date();
                d.setTime(d.getTime() + (cookieDurationDays * 24 * 60 * 60 * 1000)); // 2 day expiration
                Mozilla.Cookies.setItem(storageKey, true, d.toUTCString(), '/');
            }
        });
    }

})(window.jQuery, window.Mozilla);
