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

        var xhr;
        var xhrRequests = [];

        beforeEach(function() {
            spyOn(Mozilla.VPN, 'onRequestComplete');

            xhr = sinon.useFakeXMLHttpRequest();
            xhr.onCreate = function(req) {
                xhrRequests.push(req);
            };
        });

        afterEach(function() {
            xhr.restore();
            xhrRequests = [];
        });

        it('should pass country to onRequestComplete if server makes a response', function() {
            var country = 'ru';

            Mozilla.VPN.getLocation();

            xhrRequests[0].respond(200, {'Content-Type': 'application/json'}, '{"country_code": "' + country + '"}');

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

        var country = 'de';

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

        var fixedCountries = '|ca|my|nz|sg|gb|gg|im|io|je|uk|vg|as|mp|pr|um|us|vi|';
        var variableCountries = '|de|fr|';

        it('should return `fixed-pricce` if matching country code is found', function() {
            expect(Mozilla.VPN.getAvailability('us', fixedCountries, variableCountries)).toEqual('fixed-price');
            expect(Mozilla.VPN.getAvailability('gb', fixedCountries, variableCountries)).toEqual('fixed-price');
        });

        it('should return `variable-price` if matching country code is found', function() {
            expect(Mozilla.VPN.getAvailability('de', fixedCountries, variableCountries)).toEqual('variable-price');
            expect(Mozilla.VPN.getAvailability('fr', fixedCountries, variableCountries)).toEqual('variable-price');
        });

        it('should return `not-available` if no matching country code is found', function() {
            expect(Mozilla.VPN.getAvailability('cn', fixedCountries, variableCountries)).toEqual('not-available');
        });

        it('should return `unknown` if no country code is supplied', function() {
            expect(Mozilla.VPN.getAvailability(null, fixedCountries, variableCountries)).toEqual('unknown');
        });

        it('should return `unknown` if no country lists are supplied', function() {
            expect(Mozilla.VPN.getAvailability('us', null, null)).toEqual('unknown');
        });

        it('should return `not-available` if either country list is empty', function() {
            expect(Mozilla.VPN.getAvailability('us', '', variableCountries)).toEqual('not-available');
            expect(Mozilla.VPN.getAvailability('de', fixedCountries, '')).toEqual('not-available');
        });
    });

    describe('setAvailability', function() {

        beforeEach(function() {
            spyOn(Mozilla.VPN, 'showFixedPricing');
            spyOn(Mozilla.VPN, 'showVariablePricing');
            spyOn(Mozilla.VPN, 'showJoinWaitList');
        });

        it('should show fixed pricing as expected', function() {
            Mozilla.VPN.setAvailability('fixed-price');
            expect(Mozilla.VPN.showFixedPricing).toHaveBeenCalled();
        });

        it('should show variable pricing as expected', function() {
            Mozilla.VPN.setAvailability('variable-price');
            expect(Mozilla.VPN.showVariablePricing).toHaveBeenCalled();
        });

        it('should show join waitlist as expected', function() {
            Mozilla.VPN.setAvailability('not-available');
            expect(Mozilla.VPN.showJoinWaitList).toHaveBeenCalled();
        });

        it('should fallback to page language if availability is not known', function() {
            Mozilla.VPN.setAvailability('unknown', 'en-US');
            expect(Mozilla.VPN.showFixedPricing).toHaveBeenCalled();

            Mozilla.VPN.setAvailability('unknown', 'de');
            expect(Mozilla.VPN.showVariablePricing).toHaveBeenCalled();

            Mozilla.VPN.setAvailability('unknown', 'fr');
            expect(Mozilla.VPN.showVariablePricing).toHaveBeenCalled();
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
            var country = 'de';
            spyOn(Mozilla.VPN, 'hasGeoOverride').and.returnValue(country);

            Mozilla.VPN.init();

            expect(Mozilla.VPN.getLocation).not.toHaveBeenCalled();
            expect(Mozilla.VPN.getAvailability).toHaveBeenCalledWith(country);
            expect(Mozilla.VPN.setAvailability).toHaveBeenCalled();
        });
    });
});
