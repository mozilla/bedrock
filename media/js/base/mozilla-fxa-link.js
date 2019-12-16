/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    var FxaLink = {};
    var client = Mozilla.Client;

    /**
     * Configures Sync for Firefox browsers.
     * Only Firefox < 71 requires `service=sync`.
     * @param href {String}
     * @returns href {String}
     */
    FxaLink.updateURL = function(href) {
        var userVer = parseFloat(client._getFirefoxVersion());
        var serviceParam = userVer < 71 ? 'service=sync' : null;
        var contextParam = 'context=fx_desktop_v3';
        var separator = href.indexOf('?') > 0 ? '&' : '?';

        if (serviceParam) {
            href += separator + contextParam + '&' + serviceParam;
        } else {
            href += separator + contextParam;
        }

        return href;
    };

    /**
     * Updates FxA links with Sync params.
     * Only applicable for Firefox desktop user agents.
     */
    FxaLink.init = function() {
        if (!client._isFirefoxDesktop()) {
            return;
        }

        var fxaSigninLink = document.querySelectorAll('.js-fxa-cta-link');

        for (var i = 0; i < fxaSigninLink.length; i++) {
            var link = fxaSigninLink[i];
            var mozillaOnlineLink = link.getAttribute('data-mozillaonline-link');

            // update link href.
            link.href = FxaLink.updateURL(link.href);

            // update china repack URL.
            if (mozillaOnlineLink) {
                link.setAttribute('data-mozillaonline-link', FxaLink.updateURL(mozillaOnlineLink));
            }
        }
    };

    window.Mozilla.FxaLink = FxaLink;

})();

