(function(Mozilla) {
    'use strict';

    var fundraiser = document.getElementById('fundraiser');
    var fundraiserClose = document.getElementById('fundraiser-close');
    var cookieDurationDays = 2;
    var cookiesOK = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();
    var storageKey = 'fundraiser-eoy2018';
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
                d.setTime(d.getTime() + (cookieDurationDays * 24 * 60 * 60 * 1000)); // 2 day expiration
                Mozilla.Cookies.setItem(storageKey, true, d.toUTCString(), '/');
            }
        }, false);
    }

})(window.Mozilla);
