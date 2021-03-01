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
                    // do nothing.
                }
            }

            VPN.onRequestComplete(country);
        };

        xhr.open('GET', '/country-code.json');
        // must come after open call above for IE 10 & 11
        xhr.timeout = 2000;
        xhr.send();
    };

    /**
     * Helper used to facilitate easier debugging for page state dependent on geo-location.
     * @param {String} location e.g. 'https://www-dev.allizom.org/en-US/products/vpn/?geo=de'
     */
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

            // If VPN is not available in country then show "Join the Waitlist" state.
            if (countryCode && countryCode !== 'none' && !VPN.isAvailable(countryCode)) {
                VPN.showJoinWaitList();
            }
        }
    };

    VPN.showJoinWaitList = function() {
        document.body.classList.add('vpn-not-available');
    };

    VPN.isAvailable = function(countryCode, countries) {
        var availableCountries = document.getElementsByTagName('html')[0].getAttribute('data-vpn-fixed-price-country-codes') || countries;
        if (countryCode && availableCountries.indexOf('|' + countryCode + '|') !== -1) {

            window.dataLayer.push({
                'event': 'non-interaction',
                'eAction': 'vpn-availability',
                'eLabel': 'available'
            });

            return true;
        }

        window.dataLayer.push({
            'event': 'non-interaction',
            'eAction': 'vpn-availability',
            'eLabel': 'not-available'
        });

        return false;
    };

    VPN.init = function() {
        var override = VPN.hasGeoOverride();

        // if override URL is used, skip doing anything with geo-location and show expected content.
        if (override) {
            if (!VPN.isAvailable(override)) {
                VPN.showJoinWaitList();
            }
        } else {
            VPN.getLocation();
        }
    };

    window.Mozilla.VPN = VPN;

})();
