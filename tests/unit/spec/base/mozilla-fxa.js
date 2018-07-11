/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect */

describe('mozilla-fxa.js', function() {
    'use strict';

    describe('FxaState.applyStateToBody', function() {

        beforeEach(function() {
            $('body').attr('class', 'js state-fxa-default');
        });

        afterEach(function() {
            $('body').removeAttr('class');
        });

        it('should add the supplied value to the body class list', function() {
            Mozilla.FxaState.applyStateToBody('state-fxa-android');
            expect($('body').attr('class')).toContain('state-fxa-android');
        });

        it('should remove state-default from the body class list', function() {
            Mozilla.FxaState.applyStateToBody('state-fxa-android');
            expect($('body').attr('class')).not.toContain('state-fxa-default');
        });
    });

    describe('FxaState.getStateClassAndDo', function() {

        it('should fire the callback function with a stateClass', function() {
            var callback1 = jasmine.createSpy('callback1');

            // mock details, isFirefoxiOS, and getFxaDetails
            var details = {
                'firefox': false,
                'legacy': false,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            spyOn(Mozilla.Client, 'getFxaDetails').and.callFake(function(callback) {
                callback(details);
            });

            // call getStateClassAndDo and pass in the callback
            Mozilla.FxaState.getStateClassAndDo(callback1);
            // check callback was called with expected stateClass
            expect(callback1).toHaveBeenCalledWith('state-fxa-not-fx');
        });
    });

    describe('FxaState.convertFxaDetailsToStateAndDo', function() {
        beforeEach(function() {
            // mock
            Mozilla.Client.isFirefoxiOS = false;
            // watch
            spyOn(Mozilla.FxaState, 'applyStateToBody');
        });

        // not Firefox
        it('should set the appropriate body class when not firefox', function() {
            var details = {
                'firefox': false,
                'legacy': false,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(details, Mozilla.FxaState.applyStateToBody);
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith('state-fxa-not-fx');
        });

        // Firefox Android
        it('should set the appropriate body class when Firefox Android', function() {
            var details = {
                'firefox': true,
                'legacy': false,
                'mobile': 'android',
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(details, Mozilla.FxaState.applyStateToBody);
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith('state-fxa-android');
        });

        // Firefox iOS
        it('should set the appropriate body class when Firefox iOS', function() {
            var details = {
                'firefox': true,
                'legacy': false,
                'mobile': 'ios',
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(details, Mozilla.FxaState.applyStateToBody);
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith('state-fxa-ios');
        });

        // Firefox < 29
        it('should set the appropriate body class when pre UITour Firefox', function() {
            var details = {
                'firefox': true,
                'legacy': true,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(details, Mozilla.FxaState.applyStateToBody);
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith('state-fxa-unsupported');
        });

        // Firefox < FxALastSupported, logged out
        it('should set the appropriate body class when Legacy Firefox', function() {
            var details = {
                'firefox': true,
                'legacy': true,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(details, Mozilla.FxaState.applyStateToBody);
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith('state-fxa-unsupported');
        });

        // Firefox < FxALastSupported, logged out
        it('should set the appropriate body class when Legacy Firefox logged out', function() {
            var details = {
                'firefox': true,
                'legacy': true,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(details, Mozilla.FxaState.applyStateToBody);
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith('state-fxa-unsupported');
        });

        // Firefox Desktop < FxALastSupported, logged in
        it('should set the appropriate body class when Legacy Firefox logged in', function() {
            var details = {
                'firefox': true,
                'legacy': true,
                'mobile': false,
                'setup': true,
                'desktopDevices': 'unknown',
                'mobileDevices': 'unknown'
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(details, Mozilla.FxaState.applyStateToBody);
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith('state-fxa-unsupported');
        });

        // Firefox Desktop < 50, logged out
        it('should set the appropriate body class when Firefox pre device count logged out', function() {
            var details = {
                'firefox': true,
                'legacy': false,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(details, Mozilla.FxaState.applyStateToBody);
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith('state-fxa-supported-signed-out');
        });

        // Firefox Desktop < 50, logged in
        it('should set the appropriate body class when Firefox pre device count logged in', function() {
            var details = {
                'firefox': true,
                'legacy': false,
                'mobile': false,
                'setup': true,
                'desktopDevices': 'unknown',
                'mobileDevices': 'unknown'
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(details, Mozilla.FxaState.applyStateToBody);
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith('state-fxa-supported-signed-in');
        });

        // Firefox Desktop Current, logged out
        it('should set the appropriate body class when Current Firefox Desktop logged out', function() {
            var details = {
                'firefox': true,
                'legacy': false,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(details, Mozilla.FxaState.applyStateToBody);
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith('state-fxa-supported-signed-out');
        });

        // Firefox Desktop Current, logged in
        it('should set the appropriate body class when Current Firefox Desktop logged in', function() {
            var details = {
                'firefox': true,
                'legacy': false,
                'mobile': false,
                'setup': true,
                'desktopDevices': 2,
                'mobileDevices': 1
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(details, Mozilla.FxaState.applyStateToBody);
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith('state-fxa-supported-signed-in');
        });
    });
});
