/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn, jasmine */

describe('win10-welcome.js', function() {

    'use strict';

    beforeEach(function() {
        Mozilla.UITour = sinon.stub();
        Mozilla.UITour.getConfiguration = sinon.stub();
        Mozilla.UITour.setConfiguration = sinon.stub();
    });

    afterEach(function() {
        Mozilla.Win10Welcome.clearDefaultCheck();
        $(document).off('visibilitychange.win10');
    });

    describe('checkForDefaultSwitch', function() {

        it('should change page content when Firefox is set as default browser', function() {
            spyOn(Mozilla.Win10Welcome, 'onDefaultSwitch');
            spyOn(Mozilla.FirefoxDefault, 'isDefaultBrowser').and.callFake(function(callback) {
                callback('yes');
            });
            Mozilla.Win10Welcome.checkForDefaultSwitch();
            expect(Mozilla.Win10Welcome.onDefaultSwitch).toHaveBeenCalled();
        });

        it('should count the number of polls', function() {
            spyOn(Mozilla.FirefoxDefault, 'isDefaultBrowser').and.callFake(function(callback) {
                callback('no');
            });
            Mozilla.Win10Welcome.pollRetry = 0;
            Mozilla.Win10Welcome.checkForDefaultSwitch();
            expect(Mozilla.Win10Welcome.pollRetry).toEqual(1);
        });

        it('should only poll a set number of times', function() {
            spyOn(Mozilla.Win10Welcome, 'onDefaultSwitch');
            spyOn(Mozilla.Win10Welcome, 'clearDefaultCheck');
            spyOn(Mozilla.FirefoxDefault, 'isDefaultBrowser').and.callFake(function(callback) {
                callback('yes');
            });
            Mozilla.Win10Welcome.pollRetry = 999;
            Mozilla.Win10Welcome.checkForDefaultSwitch();
            expect(Mozilla.Win10Welcome.clearDefaultCheck).toHaveBeenCalled();
            expect(Mozilla.Win10Welcome.onDefaultSwitch).not.toHaveBeenCalled();
        });
    });

    describe('onDefaultSwitch', function() {

        it('should stop polling for changes', function() {
            spyOn(Mozilla.Win10Welcome, 'clearDefaultCheck');
            spyOn(window.dataLayer, 'push');
            Mozilla.Win10Welcome.onDefaultSwitch();
            expect(Mozilla.Win10Welcome.clearDefaultCheck).toHaveBeenCalled();
            expect(window.dataLayer.push).toHaveBeenCalledWith({
                'event': 'windows-10-welcome',
                'interaction': 'default-set',
            });
        });
    });

    describe('setDefaultCheck', function() {

        it('should start polling for changes', function() {
            spyOn(window, 'clearInterval');
            spyOn(window, 'setInterval');
            Mozilla.Win10Welcome.setDefaultCheck();
            expect(window.clearInterval).toHaveBeenCalled();
            expect(window.setInterval).toHaveBeenCalledWith(Mozilla.Win10Welcome.checkForDefaultSwitch, 2000);
        });
    });

    describe('clearDefaultCheck', function() {

        it('should stop polling for changes', function() {
            spyOn(window, 'clearInterval');
            Mozilla.Win10Welcome.pollRetry = 1;
            Mozilla.Win10Welcome.clearDefaultCheck();
            expect(window.clearInterval).toHaveBeenCalled();
            expect(Mozilla.Win10Welcome.pollRetry).toEqual(0);
        });
    });

    describe('setFirefoxAsDefault', function() {

        it('should prompt to set Firefox as default and poll for changes', function() {
            spyOn(Mozilla.FirefoxDefault, 'setDefaultBrowser');
            spyOn(Mozilla.Win10Welcome, 'setDefaultCheck');
            spyOn(Mozilla.Win10Welcome, 'clearDefaultCheck');
            spyOn(window.dataLayer, 'push');
            Mozilla.Win10Welcome.setFirefoxAsDefault();
            expect(Mozilla.Win10Welcome.setDefaultCheck).toHaveBeenCalled();
            expect(Mozilla.Win10Welcome.clearDefaultCheck).toHaveBeenCalled();
            expect(Mozilla.FirefoxDefault.setDefaultBrowser).toHaveBeenCalled();
            expect(window.dataLayer.push).toHaveBeenCalledWith({
                'event': 'windows-10-welcome',
                'interaction': 'set-default-cta-click',
            });
        });
    });

    describe('trackTabVisibility', function() {

        it('should track the event in GA', function() {
            spyOn(window.dataLayer, 'push');
            Mozilla.Win10Welcome.trackTabVisibility();
            expect(window.dataLayer.push).toHaveBeenCalledWith({
                'event': 'windows-10-welcome',
                'interaction': 'tab-visible',
            });
        });
    });

    describe('checkTabVisibility', function() {

        it('should track if the page is visible when called', function() {
            spyOn(Mozilla.Win10Welcome, 'trackTabVisibility');
            spyOn($.fn, 'one');
            Mozilla.Win10Welcome.checkTabVisibility(false);
            expect($.fn.one).not.toHaveBeenCalled();
            expect(Mozilla.Win10Welcome.trackTabVisibility).toHaveBeenCalled();
        });

        it('should bind visibility event if page is not visible', function() {
            spyOn(Mozilla.Win10Welcome, 'trackTabVisibility');
            spyOn($.fn, 'one');
            Mozilla.Win10Welcome.checkTabVisibility(true);
            expect($.fn.one).toHaveBeenCalledWith('visibilitychange.win10', Mozilla.Win10Welcome.trackTabVisibility);
            expect(Mozilla.Win10Welcome.trackTabVisibility).not.toHaveBeenCalled();
        });
    });

    describe('initPage', function() {

        it('should show CTA if Firefox is not the default browser', function() {
            spyOn(Mozilla.Win10Welcome, 'setDefaultCheck');
            spyOn(Mozilla.Win10Welcome, 'showNonDefaultContent');
            spyOn(Mozilla.Win10Welcome, 'showDefaultContent');
            spyOn(Mozilla.Win10Welcome, 'checkTabVisibility');
            spyOn(window.dataLayer, 'push');
            spyOn(Mozilla.FirefoxDefault, 'isDefaultBrowser').and.callFake(function(callback) {
                callback('no');
            });
            Mozilla.Win10Welcome.initPage();
            expect(Mozilla.Win10Welcome.showNonDefaultContent).toHaveBeenCalled();
            expect(Mozilla.Win10Welcome.setDefaultCheck).toHaveBeenCalled();
            expect(Mozilla.Win10Welcome.showDefaultContent).not.toHaveBeenCalled();
            expect(Mozilla.Win10Welcome.checkTabVisibility).toHaveBeenCalled();
            expect(window.dataLayer.push).toHaveBeenCalledWith({
                'event': 'windows-10-welcome',
                'interaction': 'default-no'
            });
        });

        it('should show links if Firefox is the default browser', function() {
            spyOn(Mozilla.Win10Welcome, 'setDefaultCheck');
            spyOn(Mozilla.Win10Welcome, 'showNonDefaultContent');
            spyOn(Mozilla.Win10Welcome, 'showDefaultContent');
            spyOn(Mozilla.Win10Welcome, 'checkTabVisibility');
            spyOn(window.dataLayer, 'push');
            spyOn(Mozilla.FirefoxDefault, 'isDefaultBrowser').and.callFake(function(callback) {
                callback('yes');
            });
            Mozilla.Win10Welcome.initPage();
            expect(Mozilla.Win10Welcome.showDefaultContent).toHaveBeenCalled();
            expect(Mozilla.Win10Welcome.showNonDefaultContent).not.toHaveBeenCalled();
            expect(Mozilla.Win10Welcome.setDefaultCheck).not.toHaveBeenCalled();
            expect(Mozilla.Win10Welcome.checkTabVisibility).toHaveBeenCalled();
            expect(window.dataLayer.push).toHaveBeenCalledWith({
                'event': 'windows-10-welcome',
                'interaction': 'default-yes'
            });
        });
    });
});
