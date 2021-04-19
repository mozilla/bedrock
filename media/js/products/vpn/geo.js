/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var VPN = {};
    VPN.countryCode = null;

    var _geoTimeout;
    var _requestComplete = false;

    VPN.getLocation = function() {
        // should /country-code.json be slow to load,
        // just show the regular messaging after 6 seconds waiting.
        _geoTimeout = setTimeout(VPN.onRequestComplete, 6000);

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
        xhr.timeout = 6000;
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
        clearTimeout(_geoTimeout);

        VPN.countryCode = typeof data === 'string' ? data : null;
        var availability = VPN.getAvailability(VPN.countryCode);

        if (!_requestComplete) {
            _requestComplete = true;
            VPN.setAvailability(availability);
        }
    };

    VPN.getAvailability = function(countryCode, fixedCountries, variableCountries) {
        var html = document.getElementsByTagName('html')[0];
        var fixedPriceCountries = html.getAttribute('data-vpn-fixed-price-country-codes');
        var variablePriceCountries = html.getAttribute('data-vpn-variable-price-country-codes');

        fixedPriceCountries = typeof fixedPriceCountries === 'string' ? fixedPriceCountries : fixedCountries;
        variablePriceCountries = typeof variablePriceCountries === 'string' ? variablePriceCountries : variableCountries;

        // If we can't determine someone's country then return early.
        if (!countryCode || typeof fixedPriceCountries !== 'string' || typeof variablePriceCountries !== 'string') {

            window.dataLayer.push({
                'event': 'non-interaction',
                'eAction': 'vpn-availability',
                'eLabel': 'unknown'
            });

            return 'unknown';
        }

        // Countries where fixed monthly subscription plan is available.
        if (countryCode && fixedPriceCountries.indexOf('|' + countryCode + '|') !== -1) {

            window.dataLayer.push({
                'event': 'non-interaction',
                'eAction': 'vpn-availability',
                'eLabel': 'fixed-price-available'
            });

            return 'fixed-price';
        }

        // Countries where variable monthly subscription plan is available.
        if (countryCode && variablePriceCountries.indexOf('|' + countryCode + '|') !== -1) {

            window.dataLayer.push({
                'event': 'non-interaction',
                'eAction': 'vpn-availability',
                'eLabel': 'variable-price-available'
            });

            return 'variable-price';
        }

        // Countries where we should show the waitlist links.
        window.dataLayer.push({
            'event': 'non-interaction',
            'eAction': 'vpn-availability',
            'eLabel': 'not-available'
        });

        return 'not-available';
    };

    VPN.setAvailability = function(availability, language) {
        if (availability === 'fixed-price') {
            // If VPN is available in countries that support fixed pricing,
            // show the fixed pricing subscribe links.
            VPN.showFixedPricing();
        } else if (availability === 'variable-price') {
            // If VPN is available in countries that support variable pricing,
            // show the subscription plan options.
            VPN.showVariablePricing();
        } else if (availability === 'not-available') {
            // If VPN is not available in country then show "Join the Waitlist" state.
            VPN.showJoinWaitList();
        } else {
            // If we can't determine someone's country then fall back to page language.
            // Both /de/ and /fr/ get variable pricing, and the rest get fixed.
            var lang = document.getElementsByTagName('html')[0].getAttribute('lang') || language;
            if (lang === 'de' || lang === 'fr') {
                VPN.showVariablePricing();
            } else {
                VPN.showFixedPricing();
            }
        }
    };

    VPN.showJoinWaitList = function() {
        document.body.classList.add('show-vpn-waitlist');
        VPN.renderJoinWaitlistButtons();
    };

    VPN.showFixedPricing = function() {
        document.body.classList.add('show-vpn-fixed-pricing');

        // initiate FxA flow metrics after subscription URLs have been set.
        if (typeof Mozilla.FxaProductButton !== 'undefined') {
            Mozilla.FxaProductButton.init();
        }
    };

    VPN.showVariablePricing = function() {
        document.body.classList.add('show-vpn-variable-pricing');
        VPN.renderScrollToPricingButtons();
        VPN.setSubscriptionButtons();

        // initiate FxA flow metrics after subscription URLs have been set.
        if (typeof Mozilla.FxaProductButton !== 'undefined') {
            Mozilla.FxaProductButton.init();
        }
    };

    // Updates subscription `plan` URL parameter based on geo-location.
    VPN.setSubscriptionButtons = function() {
        var subscribeLinks = document.querySelectorAll('.vpn-pricing-variable-plans .js-fxa-product-button');

        if (typeof VPN.countryCode !== 'string') {
            return;
        }

        for (var i = 0; i < subscribeLinks.length; i++) {
            var href = subscribeLinks[i].href;
            var plan = subscribeLinks[i].getAttribute('data-plan-' + VPN.countryCode);
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

    VPN.renderScrollToPricingButtons = function() {
        var template = document.getElementById('scroll-to-pricing-template');
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
            clone = content.querySelector('.js-vpn-variable-pricing').cloneNode(true);
            button = clone.querySelector('.mzp-c-button');
            button.classList.add('mzp-t-xl');
            button.setAttribute('data-cta-position', 'primary');
            primaryTarget.appendChild(clone);
        }

        if (navigationTarget) {
            clone = content.querySelector('.js-vpn-variable-pricing').cloneNode(true);
            button = clone.querySelector('.mzp-c-button');
            button.classList.add('mzp-t-secondary');
            button.classList.add('mzp-t-md');
            button.setAttribute('data-cta-position', 'navigation');
            navigationTarget.appendChild(button);
        }

        for (var i = 0; i < secondaryTargets.length; i++) {
            clone = content.querySelector('.js-vpn-variable-pricing').cloneNode(true);
            button = clone.querySelector('.mzp-c-button');
            button.classList.add('mzp-t-xl');
            button.setAttribute('data-cta-position', 'secondary');
            secondaryTargets[i].appendChild(clone);
        }

        if (footerTarget) {
            clone = content.querySelector('.js-vpn-variable-pricing').cloneNode(true);
            button = clone.querySelector('.mzp-c-button');
            button.classList.add('mzp-t-xl');
            button.setAttribute('data-cta-position', 'secondary');
            footerTarget.appendChild(clone);
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
