/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn, done */

describe('whatsnew/whatsnew-zh-tw-49.js', function() {
    'use strict';

    var searchEngineMap = {
        'tw': 'searchy-AA',
        'hk': 'searchy-AA-BB'
    };

    describe('versionChannelCheck', function() {
        it('should match for 49.0', function() {
            var isMatch = Mozilla.HkTwWhatsNew.versionCheck('49.0');
            expect(isMatch).toBeTruthy();
        });

        it('should not match for earlier version', function() {
            var isMatch = Mozilla.HkTwWhatsNew.versionCheck('48.0');
            expect(isMatch).toBeFalsy();
        });

        it('should not match for later version', function() {
            var isMatch = Mozilla.HkTwWhatsNew.versionCheck('49.1');
            expect(isMatch).toBeFalsy();

            isMatch = Mozilla.HkTwWhatsNew.versionCheck('50.0', 'release');
            expect(isMatch).toBeFalsy();
        });
    });

    describe('geoCheck', function() {
        it('should return true if country matches', function(done) {
            var geoCheckPromise = Mozilla.HkTwWhatsNew.geoCheck('tw', searchEngineMap);

            geoCheckPromise.then(function() {
                done();
            }, function() {
                done.fail('country is not a match');
            });

            var geoCheckPromise2 = Mozilla.HkTwWhatsNew.geoCheck('hk', searchEngineMap);

            geoCheckPromise2.then(function() {
                done();
            }, function() {
                done.fail('country is not a match');
            });
        });

        it('should return false if country does not match', function() {
            var geoCheckPromise = Mozilla.HkTwWhatsNew.geoCheck('us', searchEngineMap);

            geoCheckPromise.then(function() {
                done.fail('country is not a match, but promise resolved');
            }, function() {
                done();
            });
        });
    });

    describe('searchCheck', function() {
        beforeEach(function() {
            Mozilla.UITour = sinon.stub();
            Mozilla.UITour.getConfiguration = sinon.stub();

            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    // always return 'searchy-AA' (from map above) as search engine
                    searchEngineIdentifier: 'searchy-AA'
                });
            });
        });

        it('should resolve if search engine matches country', function(done) {
            var searchCheckPromise = Mozilla.HkTwWhatsNew.searchCheck('tw', searchEngineMap);

            searchCheckPromise.then(function() {
                done();
            }, function() {
                done.fail('search engine did not match country');
            });
        });

        it('should not resolve if search engine does not match country', function(done) {
            var searchCheckPromise = Mozilla.HkTwWhatsNew.searchCheck('hk', searchEngineMap);

            searchCheckPromise.then(function() {
                done.fail('search engine did not match country, but promise resolved');
            }, function() {
                done();
            });
        });
    });
});
