/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var VPN = {};

    var _geoTimeout;
    var _requestComplete = false;

    VPN.getLocation = function() {
        // should /country-code.json be slow to load,
        // just show the regular messaging after 3 seconds waiting.
        _geoTimeout = setTimeout(VPN.onRequestComplete, 3000);

        var xhr = new window.XMLHttpRequest();

        xhr.onload = function(r) {
            var country = 'none';

            // make sure status is in the acceptable range
            if (r.target.status >= 200 && r.target.status < 300) {

                try {
                    country = JSON.parse(r.target.responseText).country_code.toLowerCase();
                } catch (e) {
                    country = 'none';
                }
            }

            VPN.onRequestComplete(country);
        };

        xhr.open('GET', '/country-code.json');
        // must come after open call above for IE 10 & 11
        xhr.timeout = 2000;
        xhr.send();
    };

    VPN.hasGeoOverride = function(location) {
        var loc = location || window.location.search;
        if (loc.indexOf('geo=') !== -1 && loc.indexOf('www.mozilla.org') === -1) {
            var urlRe = /geo=([a-z]{2})/i;
            var match = urlRe.exec(loc);
            if (match) {
                return match[1].toLowerCase();
            }
            return false;
        }
        return false;
    };

    VPN.onRequestComplete = function(data) {
        var countryCode = typeof data === 'string' ? data : 'none';

        clearTimeout(_geoTimeout);

        if (!_requestComplete) {
            _requestComplete = true;

            if (!VPN.isAvailable(countryCode)) {
                VPN.showJoinWaitList();
            }
        }
    };

    VPN.showJoinWaitList = function() {
        document.body.classList.add('vpn-not-available');
    };

    VPN.isAvailable = function(countryCode) {
        var availableCountries = document.getElementsByTagName('html')[0].getAttribute('data-vpn-allowed-country-codes');
        if (countryCode && availableCountries.indexOf('|' + countryCode + '|') !== -1) {
            return true;
        }

        return false;
    };

    VPN.init = function() {
        var override = VPN.hasGeoOverride();

        // if override URL is used, skip doing anything with cookies & show the expected content.
        if (override) {
            if (!VPN.isAvailable(override)) {
                VPN.showJoinWaitList();
            }
        } else {
            VPN.getLocation();
        }
    };

    window.Mozilla.VPN = VPN;

    VPN.init();

})();

(function() {
    'use strict';

    var hasMediaQueries = typeof window.matchMedia !== 'undefined';

    if (!hasMediaQueries || !window.matchMedia('(min-width: 768px)').matches) {
        return;
    }

    var index = 0;
    var heroImage = document.querySelector('.vpn-hero-image');
    setInterval(function () {
        index = (index + 1) % 5;
        heroImage.setAttribute('data-illustration', 'n-' + (index + 1));
    }, 5000);

})();
