/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var client = window.Mozilla.Client;

    var $html = $(document.documentElement);
    var $downloadbar = $('#conditional-download-bar');

    // Dismiss the conditional download bar
    $downloadbar.on('click', '.btn-close', function() {
        $downloadbar.animate({
            top: '-' + ($downloadbar.height() + 10)
        }, 350, function() {
            $downloadbar.fadeOut('fast', function() {
                $downloadbar.remove();
            });
        });
    });

    // Check Firefox version
    // bug 1301721 only use major Firefox version until 49.0 is released
    if (client.isFirefoxDesktop || client.isFirefoxAndroid) {
        $html.addClass(client._isFirefoxUpToDate(false) ? 'firefox-latest' : 'firefox-old');
    } else {
        $html.addClass('nonfx');
    }

})(window.jQuery);
