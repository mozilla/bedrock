/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var client = window.Mozilla.Client;
    var body = $('body');

    if (client._isFirefoxDesktop) {
        client.getFirefoxDetails(function(details) {
            if (details.isUpToDate && details.channel === 'release') {
                body.addClass('firefox-current');
            } else if (!details.isUpToDate && details.channel === 'release') {
                body.addClass('firefox-old');
            }
        });
    } else {
        body.addClass('not-firefox');
    }

})(window.jQuery);
