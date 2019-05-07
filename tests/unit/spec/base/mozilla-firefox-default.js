/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, it, expect, sinon, spyOn, jasmine */

describe('mozilla-firefox-default.js', function() {

    'use strict';

    beforeEach(function () {
        Mozilla.UITour = sinon.stub();
        Mozilla.UITour.getConfiguration = sinon.stub();
        Mozilla.UITour.setConfiguration = sinon.stub();
    });

    describe('isDefaultBrowser', function() {

        it('should throw an error if no callback is provided', function() {
            spyOn(Mozilla.UITour, 'getConfiguration');
            expect(function() {
                Mozilla.FirefoxDefault.isDefaultBrowser();
            }).toThrowError('isDefaultBrowser: first argument is not a function');
        });

        it('should call getConfiguration to query "appinfo"', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    defaultUpdateChannel: 'aurora',
                    version: '41.0a2',
                    defaultBrowser: true
                });
            });
            Mozilla.FirefoxDefault.isDefaultBrowser(function() {
                // eslint-disable-line no-empty-function
            });
            expect(Mozilla.UITour.getConfiguration).toHaveBeenCalledWith('appinfo', jasmine.any(Function));
        });

        it('should return "yes" when Firefox is the default browser', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    defaultUpdateChannel: 'aurora',
                    version: '41.0a2',
                    defaultBrowser: true
                });
            });
            Mozilla.FirefoxDefault.isDefaultBrowser(function(isDefault) {
                expect(isDefault).toEqual('yes');
            });
        });

        it('should return "no" when Firefox is not the default browser', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    defaultUpdateChannel: 'aurora',
                    version: '41.0a2',
                    defaultBrowser: false
                });
            });
            Mozilla.FirefoxDefault.isDefaultBrowser(function(isDefault) {
                expect(isDefault).toEqual('no');
            });
        });

        it('should return "unknown" when defaultBrowser is null', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    defaultUpdateChannel: 'aurora',
                    version: '41.0a2',
                    defaultBrowser: null
                });
            });
            Mozilla.FirefoxDefault.isDefaultBrowser(function(isDefault) {
                expect(isDefault).toEqual('unknown');
            });
        });

        it('should return "unknown" when defaultBrowser is undefined', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    defaultUpdateChannel: 'aurora',
                    version: '41.0a2',
                    defaultBrowser: undefined
                });
            });
            Mozilla.FirefoxDefault.isDefaultBrowser(function(isDefault) {
                expect(isDefault).toEqual('unknown');
            });
        });

        it('should return "unknown" when defaultBrowser is not returned', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    defaultUpdateChannel: 'aurora',
                    version: '41.0a2'
                });
            });
            Mozilla.FirefoxDefault.isDefaultBrowser(function(isDefault) {
                expect(isDefault).toEqual('unknown');
            });
        });
    });

    describe('setDefaultBrowser', function() {

        it('should call setConfiguration correctly', function() {
            spyOn(Mozilla.UITour, 'setConfiguration');
            Mozilla.FirefoxDefault.setDefaultBrowser();
            expect(Mozilla.UITour.setConfiguration).toHaveBeenCalledWith('defaultBrowser');
        });
    });
});
