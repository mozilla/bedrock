/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';

    window.Mozilla.VPN.onGeoReadyCallback = function(country) {

        // Check that country code exists and meets ISO 2 char format.
        if (country && (/^[A-Z]{2}$/i).test(country)) {

            // Add country code to download URLs so experiment can differentiate clicks between countries.
            var downloadLinks = document.querySelectorAll('.js-download-first-url');

            for (var i = 0; i < downloadLinks.length; i++) {
                var separator = downloadLinks[i].href.indexOf('?') > 0 ? '&' : '?';

                downloadLinks[i].href += separator + 'geo=' + encodeURIComponent(country);
            }
        }
    };

})();
