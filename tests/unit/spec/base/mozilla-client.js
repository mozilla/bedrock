/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn, jasmine */

describe('mozilla-client.js', function() {

    'use strict';

    describe('_getFirefoxVersion', function () {

        it('should return the firefox version number as a string', function () {
            expect(window.Mozilla.Client._getFirefoxVersion('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0')).toEqual('23.0');
        });

        it('should return 0 for non Firefox browsers', function () {
            expect(window.Mozilla.Client._getFirefoxVersion('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36')).toEqual('0');
        });

    });

    describe('_isFirefoxUpToDate', function () {

        var h = document.documentElement;

        beforeEach(function () {
            h.setAttribute('data-latest-firefox', '46.0.2');
            h.setAttribute('data-esr-versions', '38.8.0 45.1.0');
        });

        afterEach(function () {
            h.removeAttribute('data-latest-firefox');
            h.removeAttribute('data-esr-versions');
        });

        it('should consider up to date if user version is equal to latest version', function() {
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, false, '46.0.2')).toBeTruthy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, true, '38.8.0')).toBeTruthy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, true, '45.1.0')).toBeTruthy();
        });

        it('should consider up to date if user version is greater than latest version', function() {
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, false, '46.0.3')).toBeTruthy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, false, '47.0')).toBeTruthy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, true, '38.9.0')).toBeTruthy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, true, '45.2.0')).toBeTruthy();
        });

        it('should consider up to date if user version is slightly less than latest version but strict option is false', function() {
            expect(window.Mozilla.Client._isFirefoxUpToDate(false, false, '46.0.1')).toBeTruthy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(false, false, '46.0')).toBeTruthy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(false, true, '38.7.0')).toBeTruthy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(false, true, '45.0')).toBeTruthy();
        });

        it('should consider outdated if user version is slightly less than latest version and strict option is true', function() {
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, false, '46.0.1')).toBeFalsy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, false, '45.0')).toBeFalsy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, false, '38.7.0')).toBeFalsy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, false, '45.0')).toBeFalsy();
        });

        it('should consider outdated if user version is much less than latest version, regardless of strict option', function() {
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, false, '40.0.2')).toBeFalsy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(false, false, '40.0.2')).toBeFalsy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(true, true, '31.7.0')).toBeFalsy();
            expect(window.Mozilla.Client._isFirefoxUpToDate(false, true, '31.7.0')).toBeFalsy();
        });

    });

    describe('getFirefoxDetails', function () {

        var h = document.documentElement;

        beforeEach(function () {
            h.setAttribute('data-latest-firefox', '46.0.2');
            h.setAttribute('data-esr-versions', '38.8.0 45.1.0');
            jasmine.clock().install();
        });

        afterEach(function () {
            h.removeAttribute('data-latest-firefox');
            h.removeAttribute('data-esr-versions');
            delete window.Mozilla.Client.FirefoxDetails;
            jasmine.clock().uninstall();
        });

        it('should fire the callback function with a Firefox details object', function() {
            var callback1 = jasmine.createSpy('callback1');
            var callback2 = jasmine.createSpy('callback2');
            var result = {
                'accurate': false, // Because the mozUITour API doesn't get called in tests, this won't be true
                'version': '46.0.2',
                'channel': 'release',
                'isUpToDate': true,
                'isESR': false
            };

            spyOn(window.Mozilla.Client, '_isFirefoxUpToDate').and.returnValue(true);
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue('46.0.2');
            window.Mozilla.Client.getFirefoxDetails(callback1);
            jasmine.clock().tick(500);
            expect(callback1).toHaveBeenCalledWith(result);
            expect(window.Mozilla.Client.FirefoxDetails).toEqual(result);
            window.Mozilla.Client.getFirefoxDetails(callback2);
            jasmine.clock().tick(500);
            expect(callback2).toHaveBeenCalledWith(result);
            expect(window.Mozilla.Client._isFirefoxUpToDate.calls.count()).toEqual(1);
        });

    });

});
