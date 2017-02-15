/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon */

describe('mozilla-traffic-cop.js', function () {
    'use strict';

    beforeEach(function() {
        // stub out Mozilla.Cookie lib
        window.Mozilla.Cookies = sinon.stub();
        window.Mozilla.Cookies.enabled = sinon.stub().returns(true);
        window.Mozilla.Cookies.setItem = sinon.stub().returns(true);
        window.Mozilla.Cookies.getItem = sinon.stub().returns(false);
        window.Mozilla.Cookies.hasItem = sinon.stub().returns(false);
    });

    describe('Mozilla.TrafficCop.init', function() {
        var cop = new Mozilla.TrafficCop({
            id: 'test123',
            variations: {
                'v=1': 20,
                'v=2': 40
            }
        });

        beforeEach(function() {
            spyOn(cop, 'verifyConfig');
        });

        it('should not initialize is user has DNT enabled', function() {
            spyOn(window, '_dntEnabled').and.returnValue(true);
            cop.init();
            expect(cop.verifyConfig).not.toHaveBeenCalled();
        });

        it('should initialize if user does not have DNT enabled', function() {
            spyOn(window, '_dntEnabled').and.returnValue(false);
            cop.init();
            expect(cop.verifyConfig).toHaveBeenCalled();
        });

        it('should initialize if DNT helper function is not available', function() {
            var dntBak = window._dntEnabled;
            window._dntEnabled = undefined;
            cop.init();
            expect(cop.verifyConfig).toHaveBeenCalled();
            window._dntEnabled = dntBak;
        });

        it('should not initialize is cookies are disabled', function() {
            spyOn(window.Mozilla.Cookies, 'enabled').and.returnValue(false);
            cop.init();
            expect(cop.verifyConfig).not.toHaveBeenCalled();
        });
    });

    describe('Mozilla.TrafficCop.verifyConfig', function() {
        it('should return true for valid id and variations', function() {
            var cop = new Mozilla.TrafficCop({
                id: 'test123',
                variations: {
                    'v=1': 20,
                    'v=2': 40
                }
            });

            expect(cop.verifyConfig()).toBeTruthy();
        });

        it('should return false when no id or variations are provided', function() {
            var cop = new Mozilla.TrafficCop();

            expect(cop.verifyConfig()).toBeFalsy();
        });

        it('should return false when no id is provided', function() {
            var cop = new Mozilla.TrafficCop({
                variations: {
                    'v=1': 80
                }
            });

            expect(cop.verifyConfig()).toBeFalsy();
        });

        it('should return false when no variations provided', function() {
            var cop = new Mozilla.TrafficCop({
                id: 'test123',
                variations: {}
            });

            expect(cop.verifyConfig()).toBeFalsy();
        });

        it('should return false when variation percentage is 0', function() {
            var cop = new Mozilla.TrafficCop({
                id: 'test123',
                variations: {
                    'v=1': 0,
                    'v=2': 0
                }
            });

            expect(cop.verifyConfig()).toBeFalsy();
        });

        it('should return false when variation percentage exceeds 100', function() {
            var cop = new Mozilla.TrafficCop({
                id: 'test123',
                variations: {
                    'v=1': 50,
                    'v=2': 60
                }
            });

            expect(cop.verifyConfig()).toBeFalsy();
        });

        it('should return true with a valid cookieExpires value', function() {
            var cop = new Mozilla.TrafficCop({
                id: 'test123',
                cookieExpires: 48,
                variations: {
                    'v=1': 20,
                    'v=2': 40
                }
            });

            expect(cop.verifyConfig()).toBeTruthy();
        });

        it('should return false with an invalid cookieExpires value', function() {
            var config1;
            var config2;
            var config3;

            config1 = config2 = config3 = {
                id: 'test123',
                variations: {
                    'v=1': 20,
                    'v=2': 40
                }
            };

            config1.cookieExpires = '2 days';
            config2.cookieExpires = null;
            config3.cookieExpires = [];

            var cop = new Mozilla.TrafficCop(config1);
            var cop2 = new Mozilla.TrafficCop(config2);
            var cop3 = new Mozilla.TrafficCop(config3);

            expect(cop.verifyConfig()).toBeFalsy();
            expect(cop2.verifyConfig()).toBeFalsy();
            expect(cop3.verifyConfig()).toBeFalsy();
        });
    });

    describe('Mozilla.TrafficCop.cookieExpiresDate', function() {
        var config = {
            id: 'test123',
            variations: {
                'v=1': 40,
                'v=2': 30
            }
        };

        it('should return a date 24 hours into the future when no hours are specified', function() {
            var cop = new Mozilla.TrafficCop(config);
            var expiry = cop.cookieExpiresDate(new Date(2017, 0, 1, 12, 30));
            expect(expiry.getFullYear()).toBe(2017);
            expect(expiry.getMonth()).toBe(0);
            expect(expiry.getDate()).toBe(2); // 24 hours default cookie length
        });

        it('should return an appropriate future date when hours are specified', function() {
            config.cookieExpires = 72;
            var cop = new Mozilla.TrafficCop(config);
            var expiry = cop.cookieExpiresDate(new Date(2017, 0, 1, 12, 30));
            expect(expiry.getFullYear()).toBe(2017);
            expect(expiry.getMonth()).toBe(0);
            expect(expiry.getDate()).toBe(4); // 72 hours = 3 days
        });

        it('should return null when 0 hours are specified', function() {
            config.cookieExpires = 0;
            var cop = new Mozilla.TrafficCop(config);
            expect(cop.cookieExpiresDate()).toBe(null);
        });
    });

    describe('Mozilla.TrafficCop.isVariation', function() {
        var cop = new Mozilla.TrafficCop({
            id: 'test123',
            variations: {
                'v=1': 40,
                'v=2': 30
            }
        });

        it('should return false if the current queryString does not contain a variation', function() {
            expect(cop.isVariation('?v=3')).toBeFalsy();
            expect(cop.isVariation('?fav=1')).toBeFalsy();
            expect(cop.isVariation('?v=3&fav=1')).toBeFalsy();
        });

        it('should return true if the current querystring contains a variation', function() {
            expect(cop.isVariation('?v=2')).toBeTruthy();
            expect(cop.isVariation('?foo=bar&v=2')).toBeTruthy();
            expect(cop.isVariation('?v=2&foo=bar')).toBeTruthy();
        });
    });

    describe('Mozilla.TrafficCop.generateRedirectUrl', function() {
        var cop = new Mozilla.TrafficCop({
            id: 'test123',
            variations: {
                'v=3': 30,
                'v=1': 20,
                'v=2': 25
            }
        });

        it('should not generate redirect if random number is greater than total percentages', function() {
            // random number >= 80 is greater than percentage total above (75)
            spyOn(window.Math, 'random').and.returnValue(0.8);

            expect(cop.generateRedirectUrl()).toBeFalsy();
        });

        it('should generate a redirect to the first variation when random number is at the start of the range', function() {
            // first variation is 30%, so 1-30
            spyOn(window.Math, 'random').and.returnValue(0.01);
            expect(cop.generateRedirectUrl('https://www.mozilla.org')).toEqual('https://www.mozilla.org?v=3');
        });

        it('should generate a redirect to the first variation when random number is at the end of the range', function() {
            // first variation is 30%, so 1-30
            spyOn(window.Math, 'random').and.returnValue(0.29);
            expect(cop.generateRedirectUrl('https://www.mozilla.org')).toEqual('https://www.mozilla.org?v=3');
        });

        it('should generate a redirect to the second variation when random number is at the start of the range', function() {
            // second variation is 20%, so 31-50
            spyOn(window.Math, 'random').and.returnValue(0.3);
            expect(cop.generateRedirectUrl('https://www.mozilla.org')).toEqual('https://www.mozilla.org?v=1');
        });

        it('should generate a redirect to the second variation when random number is at the end of the range', function() {
            // second variation is 20%, so 31-50
            spyOn(window.Math, 'random').and.returnValue(0.49);
            expect(cop.generateRedirectUrl('https://www.mozilla.org')).toEqual('https://www.mozilla.org?v=1');
        });

        it('should generate a redirect to the first variation when random number is at the start of the range', function() {
            // third variation is 25%, so 51-75
            spyOn(window.Math, 'random').and.returnValue(0.5);
            expect(cop.generateRedirectUrl('https://www.mozilla.org')).toEqual('https://www.mozilla.org?v=2');
        });

        it('should generate a redirect to the first variation when random number is at the end of the range', function() {
            // third variation is 25%, so 51-75
            spyOn(window.Math, 'random').and.returnValue(0.74);
            expect(cop.generateRedirectUrl('https://www.mozilla.org')).toEqual('https://www.mozilla.org?v=2');
        });

        it('should generate a redirect retaining the original querystring when present', function() {
            spyOn(window.Math, 'random').and.returnValue(0.74);
            expect(cop.generateRedirectUrl('https://www.mozilla.org?foo=bar')).toEqual('https://www.mozilla.org?foo=bar&v=2');
        });

        it('should generate a redirect retaining the original hash when present', function() {
            spyOn(window.Math, 'random').and.returnValue(0.74);
            expect(cop.generateRedirectUrl('https://www.mozilla.org#hash')).toEqual('https://www.mozilla.org?v=2#hash');
        });

        it('should generate a redirect retaining the original querystring and hash when present', function() {
            spyOn(window.Math, 'random').and.returnValue(0.74);
            expect(cop.generateRedirectUrl('https://www.mozilla.org?foo=bar#hash')).toEqual('https://www.mozilla.org?foo=bar&v=2#hash');
        });

        it('should use a valid variation stored in a cookie', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('v=2');

            expect(cop.generateRedirectUrl('https://www.mozilla.org')).toEqual('https://www.mozilla.org?v=2');
        });

        it('should pick a new variation if variation stored in cookie is invalid', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('v=5');
            spyOn(window.Math, 'random').and.returnValue(0.74);

            expect(cop.generateRedirectUrl('https://www.mozilla.org')).toEqual('https://www.mozilla.org?v=2');
        });

        it('should not choose a variation if user was placed into a no-variation cohort', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('novariation');

            expect(cop.generateRedirectUrl('https://www.mozilla.org')).toEqual('novariation');
        });
    });
});
