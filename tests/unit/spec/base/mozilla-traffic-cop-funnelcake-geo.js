/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn */
/* eslint camelcase: [2, {properties: "never"}] */
/* eslint new-cap: [2, {"capIsNewExceptions": ["Deferred"]}] */

describe('mozilla-traffic-cop-funnelcake-geo.js', function() {
    'use strict';

    describe('checkInCohort', function() {
        it('should return true if user has the provided cookie', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            expect(Mozilla.TCFCGeoExp.checkInCohort('foo')).toBeTruthy();
        });

        it('should return false if user does not has the provided cookie', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(false);
            expect(Mozilla.TCFCGeoExp.checkInCohort('foo')).toBeFalsy();
        });
    });

    describe('checkGeoNonmatch', function() {
        it('should return false if user has the provided cookie', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            expect(Mozilla.TCFCGeoExp.checkGeoNonmatch('foo')).toBeFalsy();
        });

        it('should return true if user does not has the provided cookie', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(false);
            expect(Mozilla.TCFCGeoExp.checkGeoNonmatch('foo')).toBeTruthy();
        });
    });

    describe('preCheckGeo', function() {
        it('should return false if less than IE 9', function() {
            expect(Mozilla.TCFCGeoExp.preCheckGeo('Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)')).toBeFalsy();
        });

        it('should return false if like Firefox', function() {
            expect(Mozilla.TCFCGeoExp.preCheckGeo('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0 SeaMonkey/2.37a1')).toBeFalsy();
            expect(Mozilla.TCFCGeoExp.preCheckGeo('Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1')).toBeFalsy();
        });

        it('should return false if is Firefox', function() {
            expect(Mozilla.TCFCGeoExp.preCheckGeo('Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')).toBeFalsy();
            expect(Mozilla.TCFCGeoExp.preCheckGeo('Mozilla/5.0 (Mobile; rv:26.0) Gecko/26.0 Firefox/26.0')).toBeFalsy();
        });

        it('should return false if not on windows', function() {
            expect(Mozilla.TCFCGeoExp.preCheckGeo(null, 'osx')).toBeFalsy();
            expect(Mozilla.TCFCGeoExp.preCheckGeo(null, 'android')).toBeFalsy();
        });

        it('should return false if a funnelcake id is in the URL', function() {
            expect(Mozilla.TCFCGeoExp.preCheckGeo(null, null, '?f=111')).toBeFalsy();
            expect(Mozilla.TCFCGeoExp.preCheckGeo(null, null, '?foo=bar&f=111')).toBeFalsy();
            expect(Mozilla.TCFCGeoExp.preCheckGeo(null, null, '?f=111&bar=baz')).toBeFalsy();
        });

        it('should return false if DNT is enabled', function() {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(true);
            expect(Mozilla.TCFCGeoExp.preCheckGeo()).toBeFalsy();
        });

        it('should return true if all checks pass', function() {
            expect(Mozilla.TCFCGeoExp.preCheckGeo('Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36 Edge/12.0', 'windows', null)).toBeTruthy();
        });
    });

    describe('geoLookup', function() {
        var xhr;
        var xhrRequests = [];

        beforeEach(function() {
            spyOn(Mozilla.TCFCGeoExp, 'runExperiment').and.returnValue(true);
            spyOn(Mozilla.Cookies, 'setItem').and.returnValue(true);

            xhr = sinon.useFakeXMLHttpRequest();
            xhr.onCreate = function(req) {
                xhrRequests.push(req);
            };
        });

        afterEach(function() {
            xhr.restore();
            xhrRequests = [];
        });

        it('should do nothing if server errors out', function() {
            Mozilla.TCFCGeoExp.geoLookup('de', 'someCookie', {});

            xhrRequests[0].respond(500, '', '');

            expect(Mozilla.TCFCGeoExp.runExperiment).not.toHaveBeenCalled();
            expect(Mozilla.Cookies.setItem).not.toHaveBeenCalled();
        });

        it('should set a cookie if country does not match', function() {
            var someConfig = {experimentId: 'weapon-x'};

            Mozilla.TCFCGeoExp.geoLookup('de', 'someCookie', someConfig);

            xhrRequests[0].respond(200, {'Content-Type': 'application/json'}, '{"country_code": "us"}');

            expect(Mozilla.Cookies.setItem).toHaveBeenCalledWith('someCookie', 'us', jasmine.any(Date));
        });

        it('should call runExperiment if country matches', function() {
            var someConfig = {};

            Mozilla.TCFCGeoExp.geoLookup('de', 'someCookie', someConfig);

            xhrRequests[0].respond(200, {'Content-Type': 'application/json'}, '{"country_code": "de"}');

            expect(Mozilla.TCFCGeoExp.runExperiment).toHaveBeenCalledWith(someConfig);
        });
    });
});
