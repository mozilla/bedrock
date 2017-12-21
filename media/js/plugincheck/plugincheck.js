/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var client = window.Mozilla.Client;
    var body = $('body');

    if (client.isFirefoxDesktop) {
        client.getFirefoxDetails(function(details) {
            // set `strict` to `false`, so we only test against the major version number.
            var isUpToDate = client._isFirefoxUpToDate(false, details.isESR, details.version);
            if (isUpToDate) {
                body.addClass('firefox-current');
            } else {
                body.addClass('firefox-old');
            }
        });
    } else {
        body.addClass('not-firefox');
    }

})(window.jQuery);
