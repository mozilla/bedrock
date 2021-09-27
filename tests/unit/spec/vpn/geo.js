/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global sinon */
/* eslint camelcase: [2, {properties: "never"}] */

describe('geo.js', function() {
    'use strict';

    beforeEach(function() {
        // stub out google tag manager
        window.dataLayer = sinon.stub();
        window.dataLayer.push = sinon.stub();
    });

    describe('getLocation', function() {

        let xhr;
        let xhrRequests = [];

        beforeEach(function() {
            spyOn(Mozilla.VPN, 'onRequestComplete');

            xhr = sinon.useFakeXMLHttpRequest();
            xhr.onCreate = (req) => {
                xhrRequests.push(req);
            };
        });

        afterEach(function() {
            xhr.restore();
            xhrRequests = [];
        });

        it('should pass country to onRequestComplete if server makes a response', function() {
            const country = 'ru';

            Mozilla.VPN.getLocation();

            xhrRequests[0].respond(200, {'Content-Type': 'application/json'}, `{"country_code": "${country}"}`);

            expect(Mozilla.VPN.onRequestComplete).toHaveBeenCalledWith(country);
        });

        it('should call onRequestComplete even if server errors out', function() {
            Mozilla.VPN.getLocation();

            xhrRequests[0].respond(500, '', '');

            expect(Mozilla.VPN.onRequestComplete).toHaveBeenCalledWith(null);
        });
    });

    describe('hasGeoOverride', function() {

        it('should return a geo value when supplied', function() {
            expect(Mozilla.VPN.hasGeoOverride('/products/vpn/?geo=de')).toEqual('de');
        });

        it('should return false for no override', function() {
            expect(Mozilla.VPN.hasGeoOverride('/products/vpn/')).toBeFalsy();
        });

        it('should return false if used in a production domain', function() {
            expect(Mozilla.VPN.hasGeoOverride('https://www.mozilla.org/en-US/products/vpn/?geo=de')).toBeFalsy();
        });
    });

    describe('onRequestComplete', function() {

        const country = 'de';

        beforeEach(function() {
            spyOn(Mozilla.VPN, 'getAvailability').and.returnValue('variable-price');
            spyOn(Mozilla.VPN, 'setAvailability');
        });

        it('should show Join the Waitlist buttons if VPN is not available', function() {
            Mozilla.VPN.onRequestComplete(country);
            expect(Mozilla.VPN.setAvailability).toHaveBeenCalledWith('variable-price');

            Mozilla.VPN.onRequestComplete(country);
            expect(Mozilla.VPN.setAvailability).toHaveBeenCalledTimes(1);
        });
    });

    describe('getAvailability', function() {

        const availableCountries = '|ca|my|nz|sg|gb|gg|im|io|je|uk|vg|as|mp|pr|um|us|vi|at|be|ch|de|es|fr|it|ie|nl|';

        it('should return `available` if matching country code is found', function() {
            expect(Mozilla.VPN.getAvailability('us', availableCountries)).toEqual('available');
            expect(Mozilla.VPN.getAvailability('gb', availableCountries)).toEqual('available');
            expect(Mozilla.VPN.getAvailability('at', availableCountries)).toEqual('available');
            expect(Mozilla.VPN.getAvailability('be', availableCountries)).toEqual('available');
            expect(Mozilla.VPN.getAvailability('ch', availableCountries)).toEqual('available');
            expect(Mozilla.VPN.getAvailability('de', availableCountries)).toEqual('available');
            expect(Mozilla.VPN.getAvailability('es', availableCountries)).toEqual('available');
            expect(Mozilla.VPN.getAvailability('fr', availableCountries)).toEqual('available');
            expect(Mozilla.VPN.getAvailability('it', availableCountries)).toEqual('available');
            expect(Mozilla.VPN.getAvailability('ie', availableCountries)).toEqual('available');
            expect(Mozilla.VPN.getAvailability('nl', availableCountries)).toEqual('available');
        });

        it('should return `not-available` if no matching country code is found', function() {
            expect(Mozilla.VPN.getAvailability('cn', availableCountries)).toEqual('not-available');
        });

        it('should return `unknown` if no country code is supplied', function() {
            expect(Mozilla.VPN.getAvailability(null, availableCountries)).toEqual('unknown');
        });

        it('should return `unknown` if no country list is supplied', function() {
            expect(Mozilla.VPN.getAvailability('us', null)).toEqual('unknown');
        });

        it('should return `not-available` if country list is empty', function() {
            expect(Mozilla.VPN.getAvailability('us', '')).toEqual('not-available');
        });
    });

    describe('setAvailability', function() {

        beforeEach(function() {
            spyOn(Mozilla.VPN, 'showPricing');
            spyOn(Mozilla.VPN, 'showJoinWaitList');
        });

        it('should show variable pricing as expected', function() {
            Mozilla.VPN.setAvailability('available');
            expect(Mozilla.VPN.showPricing).toHaveBeenCalled();
        });

        it('should show join waitlist as expected', function() {
            Mozilla.VPN.setAvailability('not-available');
            expect(Mozilla.VPN.showJoinWaitList).toHaveBeenCalled();
        });

        it('should show pricing if country is unknown (falling back to page language)', function() {
            Mozilla.VPN.setAvailability('unknown');
            expect(Mozilla.VPN.showPricing).toHaveBeenCalled();
        });
    });

    describe('updateSubscriptionURL', function() {

        it('should update the subscription plan ID as expected', function() {
            const result = Mozilla.VPN.updateSubscriptionURL('price_1IgnlcJNcmPzuWtRjrNa39W4', 'https://accounts.firefox.com/subscriptions/products/prod_FiJ42WCzZNRSbS?plan=price_1IgwblJNcmPzuWtRynC7dqQa&entrypoint=www.mozilla.org-vpn-product-page');
            expect(result).toEqual('https://accounts.firefox.com/subscriptions/products/prod_FiJ42WCzZNRSbS?plan=price_1IgnlcJNcmPzuWtRjrNa39W4&entrypoint=www.mozilla.org-vpn-product-page');
        });

        it('should not change the URL if there is no plan ID', function() {
            const result = Mozilla.VPN.updateSubscriptionURL(null, 'https://accounts.firefox.com/subscriptions/products/prod_FiJ42WCzZNRSbS?plan=price_1IgwblJNcmPzuWtRynC7dqQa&entrypoint=www.mozilla.org-vpn-product-page');
            expect(result).toEqual('https://accounts.firefox.com/subscriptions/products/prod_FiJ42WCzZNRSbS?plan=price_1IgwblJNcmPzuWtRynC7dqQa&entrypoint=www.mozilla.org-vpn-product-page');
        });

        it('should not change the URL if there is no plan query parameter', function() {
            const result = Mozilla.VPN.updateSubscriptionURL('price_1IgwblJNcmPzuWtRynC7dqQa', 'https://accounts.firefox.com/subscriptions/products?entrypoint=www.mozilla.org-vpn-product-page');
            expect(result).toEqual('https://accounts.firefox.com/subscriptions/products?entrypoint=www.mozilla.org-vpn-product-page');
        });
    });

    describe('getCurrency', function() {
        it('should return "euro" for EU countries', function() {
            expect(Mozilla.VPN.getCurrency('at')).toEqual('euro');
            expect(Mozilla.VPN.getCurrency('be')).toEqual('euro');
            expect(Mozilla.VPN.getCurrency('de')).toEqual('euro');
            expect(Mozilla.VPN.getCurrency('es')).toEqual('euro');
            expect(Mozilla.VPN.getCurrency('fr')).toEqual('euro');
            expect(Mozilla.VPN.getCurrency('it')).toEqual('euro');
            expect(Mozilla.VPN.getCurrency('ie')).toEqual('euro');
            expect(Mozilla.VPN.getCurrency('nl')).toEqual('euro');
        });

        it('should return "chf" for Switzerland', function() {
            expect(Mozilla.VPN.getCurrency('ch')).toEqual('chf');
        });

        it('should return "usd" for wave 1 countries', function() {
            expect(Mozilla.VPN.getCurrency('ca')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('my')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('nz')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('sg')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('gb')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('gg')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('im')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('io')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('je')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('uk')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('vg')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('as')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('mp')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('pr')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('um')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('us')).toEqual('usd');
            expect(Mozilla.VPN.getCurrency('vi')).toEqual('usd');
        });
    });

    describe('init', function() {

        beforeEach(function() {
            spyOn(Mozilla.VPN, 'getAvailability').and.callThrough();
            spyOn(Mozilla.VPN, 'setAvailability');
            spyOn(Mozilla.VPN, 'getLocation');
        });

        it('should query geo-location', function() {
            Mozilla.VPN.init();

            expect(Mozilla.VPN.getLocation).toHaveBeenCalled();
        });

        it('should override geo-location call if param exists', function() {
            const country = 'de';
            spyOn(Mozilla.VPN, 'hasGeoOverride').and.returnValue(country);

            Mozilla.VPN.init();

            expect(Mozilla.VPN.getLocation).not.toHaveBeenCalled();
            expect(Mozilla.VPN.getAvailability).toHaveBeenCalledWith(country);
            expect(Mozilla.VPN.setAvailability).toHaveBeenCalled();
        });
    });
});
