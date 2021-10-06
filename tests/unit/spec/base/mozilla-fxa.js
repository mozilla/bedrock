/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-fxa.js', function () {
    'use strict';

    describe('FxaState.applyStateToBody', function () {
        beforeEach(function () {
            document.body.classList.add('js', 'state-fxa-default');
        });

        afterEach(function () {
            document.body.classList.remove('js', 'state-fxa-default');
        });

        it('should add the supplied value to the body class list', function () {
            Mozilla.FxaState.applyStateToBody('state-fxa-android');
            expect(
                document.body.classList.contains('state-fxa-android')
            ).toBeTruthy();
        });

        it('should remove state-default from the body class list', function () {
            Mozilla.FxaState.applyStateToBody('state-fxa-android');
            expect(
                document.body.classList.contains('state-fxa-default')
            ).toBeFalsy();
        });
    });

    describe('FxaState.getStateClassAndDo', function () {
        it('should fire the callback function with a stateClass', function () {
            const callback1 = jasmine.createSpy('callback1');

            // mock details, isFirefoxiOS, and getFxaDetails
            const details = {
                firefox: false,
                legacy: false,
                mobile: false,
                setup: false,
                desktopDevices: false,
                mobileDevices: false
            };

            spyOn(Mozilla.Client, 'getFxaDetails').and.callFake((callback) => {
                callback(details);
            });

            // call getStateClassAndDo and pass in the callback
            Mozilla.FxaState.getStateClassAndDo(callback1);
            // check callback was called with expected stateClass
            expect(callback1).toHaveBeenCalledWith('state-fxa-not-fx');
        });
    });

    describe('FxaState.convertFxaDetailsToStateAndDo', function () {
        beforeEach(function () {
            // mock
            Mozilla.Client.isFirefoxiOS = false;
            // watch
            spyOn(Mozilla.FxaState, 'applyStateToBody');
        });

        // not Firefox
        it('should set the appropriate body class when not firefox', function () {
            const details = {
                firefox: false,
                legacy: false,
                mobile: false,
                setup: false,
                desktopDevices: false,
                mobileDevices: false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(
                details,
                Mozilla.FxaState.applyStateToBody
            );
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith(
                'state-fxa-not-fx'
            );
        });

        // Firefox Android
        it('should set the appropriate body class when Firefox Android', function () {
            const details = {
                firefox: true,
                legacy: false,
                mobile: 'android',
                setup: false,
                desktopDevices: false,
                mobileDevices: false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(
                details,
                Mozilla.FxaState.applyStateToBody
            );
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith(
                'state-fxa-android'
            );
        });

        // Firefox iOS
        it('should set the appropriate body class when Firefox iOS', function () {
            const details = {
                firefox: true,
                legacy: false,
                mobile: 'ios',
                setup: false,
                desktopDevices: false,
                mobileDevices: false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(
                details,
                Mozilla.FxaState.applyStateToBody
            );
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith(
                'state-fxa-ios'
            );
        });

        // Firefox < 29
        it('should set the appropriate body class when pre UITour Firefox', function () {
            const details = {
                firefox: true,
                legacy: true,
                mobile: false,
                setup: false,
                desktopDevices: false,
                mobileDevices: false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(
                details,
                Mozilla.FxaState.applyStateToBody
            );
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith(
                'state-fxa-unsupported'
            );
        });

        // Firefox < FxALastSupported, logged out
        it('should set the appropriate body class when Legacy Firefox', function () {
            const details = {
                firefox: true,
                legacy: true,
                mobile: false,
                setup: false,
                desktopDevices: false,
                mobileDevices: false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(
                details,
                Mozilla.FxaState.applyStateToBody
            );
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith(
                'state-fxa-unsupported'
            );
        });

        // Firefox < FxALastSupported, logged out
        it('should set the appropriate body class when Legacy Firefox logged out', function () {
            const details = {
                firefox: true,
                legacy: true,
                mobile: false,
                setup: false,
                desktopDevices: false,
                mobileDevices: false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(
                details,
                Mozilla.FxaState.applyStateToBody
            );
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith(
                'state-fxa-unsupported'
            );
        });

        // Firefox Desktop < FxALastSupported, logged in
        it('should set the appropriate body class when Legacy Firefox logged in', function () {
            const details = {
                firefox: true,
                legacy: true,
                mobile: false,
                setup: true,
                desktopDevices: 'unknown',
                mobileDevices: 'unknown'
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(
                details,
                Mozilla.FxaState.applyStateToBody
            );
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith(
                'state-fxa-unsupported'
            );
        });

        // Firefox Desktop < 50, logged out
        it('should set the appropriate body class when Firefox pre device count logged out', function () {
            const details = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: false,
                desktopDevices: false,
                mobileDevices: false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(
                details,
                Mozilla.FxaState.applyStateToBody
            );
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith(
                'state-fxa-supported-signed-out'
            );
        });

        // Firefox Desktop < 50, logged in
        it('should set the appropriate body class when Firefox pre device count logged in', function () {
            const details = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: true,
                desktopDevices: 'unknown',
                mobileDevices: 'unknown'
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(
                details,
                Mozilla.FxaState.applyStateToBody
            );
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith(
                'state-fxa-supported-signed-in'
            );
        });

        // Firefox Desktop Current, logged out
        it('should set the appropriate body class when Current Firefox Desktop logged out', function () {
            const details = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: false,
                desktopDevices: false,
                mobileDevices: false
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(
                details,
                Mozilla.FxaState.applyStateToBody
            );
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith(
                'state-fxa-supported-signed-out'
            );
        });

        // Firefox Desktop Current, logged in
        it('should set the appropriate body class when Current Firefox Desktop logged in', function () {
            const details = {
                firefox: true,
                legacy: false,
                mobile: false,
                setup: true,
                desktopDevices: 2,
                mobileDevices: 1
            };

            Mozilla.FxaState.convertFxaDetailsToStateAndDo(
                details,
                Mozilla.FxaState.applyStateToBody
            );
            expect(Mozilla.FxaState.applyStateToBody).toHaveBeenCalledWith(
                'state-fxa-supported-signed-in'
            );
        });
    });
});
