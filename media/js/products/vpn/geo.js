/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    var VPN = {};
    VPN.countryCode = null;

    var _geoTimeout;
    var _requestComplete = false;

    // Euro pricing
    var EURO_COUNTRIES = ['at', 'be', 'de', 'es', 'fr', 'it'];

    // Swiss Francs (CHF) pricing
    var CHF_COUNTRIES = ['ch'];

    VPN.getLocation = function() {
        // should /country-code.json be slow to load,
        // just show the regular messaging after 15 seconds waiting.
        var timeoutValue = 15000;
        _geoTimeout = setTimeout(VPN.onRequestComplete, timeoutValue);

        var xhr = new window.XMLHttpRequest();

        xhr.onload = function(r) {
            var country = null;

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
        xhr.timeout = timeoutValue;
        xhr.send();
    };

    /**
     * Helper used to facilitate easier debugging for page state dependent on geo-location.
     * @param {String} location e.g. 'https://www-dev.allizom.org/en-US/products/vpn/?geo=de'
     */
    VPN.hasGeoOverride = function(location) {
        var loc = location || window.location.href;
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
        clearTimeout(_geoTimeout);

        VPN.countryCode = typeof data === 'string' ? data : null;
        var availability = VPN.getAvailability(VPN.countryCode);

        if (!_requestComplete) {
            _requestComplete = true;
            VPN.setAvailability(availability);
        }
    };

    VPN.getAvailability = function(countryCode, countries) {
        var html = document.getElementsByTagName('html')[0];
        var availableCountries = html.getAttribute('data-vpn-country-codes');

        availableCountries = typeof availableCountries === 'string' ? availableCountries : countries;

        // If we can't determine someone's country then return early.
        if (!countryCode || typeof availableCountries !== 'string') {

            window.dataLayer.push({
                'event': 'non-interaction',
                'eAction': 'vpn-availability',
                'eLabel': 'unknown'
            });

            return 'unknown';
        }

        // Countries where VPN is available.
        if (countryCode && availableCountries.indexOf('|' + countryCode + '|') !== -1) {

            window.dataLayer.push({
                'event': 'non-interaction',
                'eAction': 'vpn-availability',
                'eLabel': 'available'
            });

            return 'available';
        }

        // Countries where we should show the waitlist links.
        window.dataLayer.push({
            'event': 'non-interaction',
            'eAction': 'vpn-availability',
            'eLabel': 'not-available'
        });

        return 'not-available';
    };

    VPN.setAvailability = function(availability) {
        if (availability === 'not-available') {
            // If VPN is not available in country then show "Join the Waitlist" state.
            VPN.showJoinWaitList();
        } else {
            // Else show the subscription plan options.
            VPN.showPricing();
        }
    };

    VPN.showJoinWaitList = function() {
        document.body.classList.add('show-vpn-waitlist');
        VPN.renderJoinWaitlistButtons();
    };

    VPN.showPricing = function() {
        document.body.classList.add('show-vpn-pricing');
        VPN.setDisplayPrice();
        VPN.setSubscriptionButtons();

        // support custom callback for geo-location check
        if (typeof VPN.onGeoReadyCallback === 'function') {
            VPN.onGeoReadyCallback(VPN.countryCode);
        }

        // initiate FxA flow metrics after subscription URLs have been set.
        if (typeof Mozilla.FxaProductButton !== 'undefined') {
            Mozilla.FxaProductButton.init();
        }
    };

    // Updates subscription `plan` URL parameter based on geo-location.
    VPN.setSubscriptionButtons = function() {
        var subscribeLinks = document.querySelectorAll('.vpn-pricing-variable-plans .js-fxa-product-button, .vpn-pricing-offer .js-fxa-product-button'
        );

        if (typeof VPN.countryCode !== 'string') {
            return;
        }

        for (var i = 0; i < subscribeLinks.length; i++) {
            var href = subscribeLinks[i].href;
            var plan;

            // Try and get country plan, else fallback to US plan.
            plan = subscribeLinks[i].getAttribute('data-plan-' + VPN.countryCode);

            if (!plan) {
                plan = subscribeLinks[i].getAttribute('data-plan-us');
            }

            subscribeLinks[i].href = VPN.updateSubscriptionURL(plan, href);
        }
    };

    VPN.updateSubscriptionURL = function(plan, href) {
        var params;

        if (typeof plan === 'string' && typeof href === 'string') {
            params = new window._SearchParams(href.split('?')[1]);

            if (params.has('plan')) {
                params.set('plan', plan);
                return href.split('?')[0] + '?' + params.toString();
            }
        }

        return href;
    };

    VPN.getCurrency = function(country) {
        if (EURO_COUNTRIES.indexOf(country) !== -1) {
            return 'euro';
        } else if (CHF_COUNTRIES.indexOf(country) !== -1) {
            return 'chf';
        }

        return 'usd';
    };

    // Sets the displayed subscription price based on geo-location.
    VPN.setDisplayPrice = function() {
        var displayPrice = document.querySelectorAll('.js-vpn-monthly-price-display, .js-vpn-total-price-display, .js-vpn-saving-display');

        if (typeof VPN.countryCode !== 'string') {
            return;
        }

        var currency = VPN.getCurrency(VPN.countryCode);

        for (var i = 0; i < displayPrice.length; i++) {
            var price;

            // Use Euro plan for DE/FR else fallback to US$ pricing.
            if (currency === 'euro') {
                price = displayPrice[i].getAttribute('data-price-euro');
            } else if (currency === 'chf') {
                price = displayPrice[i].getAttribute('data-price-chf');
            } else {
                price = displayPrice[i].getAttribute('data-price-usd');
            }

            if (price) {
                displayPrice[i].innerHTML = price;
            }
        }
    };

    VPN.renderJoinWaitlistButtons = function() {
        var template = document.getElementById('join-waitlist-template');
        var primaryTarget = document.querySelector('.js-target-primary-cta');
        var secondaryTargets = document.querySelectorAll('.js-target-secondary-cta');
        var navigationTarget = document.querySelector('.js-target-navigation-cta');
        var footerTarget = document.querySelector('.js-target-footer-cta');
        var content = template.content || template;
        var clone;
        var button;

        if (!template || !content) {
            return;
        }

        if (primaryTarget) {
            clone = content.querySelector('.js-vpn-waitlist').cloneNode(true);
            button = clone.querySelector('.mzp-c-button');
            button.classList.add('mzp-t-xl');
            button.setAttribute('data-cta-position', 'primary');
            primaryTarget.appendChild(clone);
        }

        if (navigationTarget) {
            clone = content.querySelector('.js-vpn-waitlist').cloneNode(true);
            button = clone.querySelector('.mzp-c-button');
            button.classList.add('mzp-t-secondary');
            button.classList.add('mzp-t-md');
            button.setAttribute('data-cta-position', 'navigation');
            navigationTarget.appendChild(button);
        }

        for (var i = 0; i < secondaryTargets.length; i++) {
            clone = content.querySelector('.js-vpn-waitlist').cloneNode(true);
            button = clone.querySelector('.mzp-c-button');
            button.classList.add('mzp-t-xl');
            button.setAttribute('data-cta-position', 'secondary');
            secondaryTargets[i].appendChild(clone);
        }

        if (footerTarget) {
            clone = content.querySelector('.js-vpn-waitlist').cloneNode(true);
            button = clone.querySelector('.mzp-c-button');
            button.classList.add('mzp-t-xl');
            button.setAttribute('data-cta-position', 'secondary');
            footerTarget.appendChild(clone);
        }
    };

    VPN.init = function() {
        var override = VPN.hasGeoOverride();

        // if override URL is used, skip doing anything with geo-location and show expected content.
        if (override) {
            VPN.countryCode = override;
            var availability = VPN.getAvailability(VPN.countryCode);
            VPN.setAvailability(availability);
        } else {
            VPN.getLocation();
        }
    };

    window.Mozilla.VPN = VPN;

})();
