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

            expect(Mozilla.VPN.onRequestComplete).toHaveBeenCalledWith('none');
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
            spyOn(Mozilla.VPN, 'isAvailable').and.returnValue(false);
            spyOn(Mozilla.VPN, 'showJoinWaitList');
        });

        it('should show Join the Waitlist buttons if VPN is not available', function() {
            Mozilla.VPN.onRequestComplete(country);
            expect(Mozilla.VPN.showJoinWaitList).toHaveBeenCalled();

            Mozilla.VPN.onRequestComplete(country);
            expect(Mozilla.VPN.showJoinWaitList).toHaveBeenCalledTimes(1);
        });
    });

    describe('isAvailable', function() {

        var countries = '|ca|my|nz|sg|gb|gg|im|io|je|uk|vg|as|mp|pr|um|us|vi|';

        it('should return true if country code is found', function() {
            expect(Mozilla.VPN.isAvailable('us', countries)).toBeTruthy();
        });

        it('should return false if country code is found', function() {
            expect(Mozilla.VPN.isAvailable('de', countries)).toBeFalsy();
            expect(Mozilla.VPN.isAvailable(null, countries)).toBeFalsy();
            expect(Mozilla.VPN.isAvailable(undefined, countries)).toBeFalsy();
            expect(Mozilla.VPN.isAvailable(false, countries)).toBeFalsy();
        });
    });

    describe('init', function() {

        beforeEach(function() {
            spyOn(Mozilla.VPN, 'isAvailable').and.returnValue(false);
            spyOn(Mozilla.VPN, 'showJoinWaitList');
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
            expect(Mozilla.VPN.isAvailable).toHaveBeenCalledWith(country);
            expect(Mozilla.VPN.showJoinWaitList).toHaveBeenCalled();
        });
    });
});
