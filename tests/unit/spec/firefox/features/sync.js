/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon */

describe('features-sync.js', function() {
    'use strict';

    describe('SyncPage.setBodyClass', function() {
        beforeEach(function() {
            $('body').attr('class', 'js state-default');
        });

        it('should add the supplied value to the body class list', function() {
            Mozilla.SyncPage.setBodyClass('state-fx-android');
            expect(Mozilla.SyncPage.body.getAttribute('class')).toContain('state-fx-android');
        });

        it('should remove state-default from the body class list', function() {
            Mozilla.SyncPage.setBodyClass('state-fx-31-signed-in');
            expect(Mozilla.SyncPage.body.getAttribute('class')).not.toContain('state-default');
        });
    });

    describe('SyncPage.trackPageState', function() {
        it('should contain an object with the supplied value', function() {
            Mozilla.SyncPage.trackPageState('illinois');
            expect(Mozilla.SyncPage.dataLayer).toContain({
                'event': 'page-load',
                'browser': 'illinois'
            });
        });
    });

    // tests for easy states:
    //  - not FX
    //  - Fx Android
    //  - Fx iOS
    //  - Fx <= 30
    describe('SyncPage.init not Fx 31+', function() {
        var config = {};

        beforeEach(function() {
            var $ctaSync = '<button id="cta-sync">Sync It!<button>';
            $('body').append($ctaSync);

            spyOn(Mozilla.SyncPage, 'setBodyClass');
            spyOn(Mozilla.SyncPage, 'trackPageState');
        });

        it('should set the appropriate body class and tracking when not firefox', function() {
            config.client = {
                isFirefox: false
            };

            Mozilla.SyncPage.init(config);
            expect(Mozilla.SyncPage.setBodyClass).toHaveBeenCalledWith('state-not-fx');
            expect(Mozilla.SyncPage.trackPageState).toHaveBeenCalledWith('Not Firefox');
        });

        it('should set the appropriate body class and tracking when fx android', function() {
            config.client = {
                isFirefox: true,
                isFirefoxAndroid: true
            };

            Mozilla.SyncPage.init(config);
            expect(Mozilla.SyncPage.setBodyClass).toHaveBeenCalledWith('state-fx-android');
            expect(Mozilla.SyncPage.trackPageState).toHaveBeenCalledWith('Firefox for Android');
        });

        it('should set the appropriate body class and tracking when fx ios', function() {
            config.client = {
                isFirefox: true,
                isFirefoxiOS: true
            };

            Mozilla.SyncPage.init(config);
            expect(Mozilla.SyncPage.setBodyClass).toHaveBeenCalledWith('state-fx-ios');
            expect(Mozilla.SyncPage.trackPageState).toHaveBeenCalledWith('Firefox for iOS');
        });

        it('should set the appropriate body class and tracking when fx <= 30', function() {
            config.client = {
                isFirefox: true,
                isFirefoxDesktop: true,
                FirefoxMajorVersion: 30
            };

            Mozilla.SyncPage.init(config);
            expect(Mozilla.SyncPage.setBodyClass).toHaveBeenCalledWith('state-fx-30-older');
            expect(Mozilla.SyncPage.trackPageState).toHaveBeenCalledWith('Firefox 30 or older');
        });
    });

    // tests for complex states (dependent on UITour):
    //  - fx 31+ signed in to sync
    //  - fx 31+ signed out of sync
    describe('SyncPage.init Fx 31+', function() {
        var config = {
            client: {
                isFirefox: true,
                isFirefoxDesktop: true,
                FirefoxMajorVersion: 31
            }
        };

        beforeEach(function() {
            spyOn(Mozilla.SyncPage, 'setBodyClass');
            spyOn(Mozilla.SyncPage, 'trackPageState');

            Mozilla.UITour.getConfiguration = sinon.stub();
        });

        it('should set the appropriate body class and tracking when signed in to sync', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    setup: true
                });
            });

            Mozilla.SyncPage.init(config);

            expect(Mozilla.SyncPage.setBodyClass).toHaveBeenCalledWith('state-fx-31-signed-in');
            expect(Mozilla.SyncPage.trackPageState).toHaveBeenCalledWith('Firefox 31 or Higher: Signed-In');
        });

        it('should set the appropriate body class and tracking when signed out of sync', function() {
            spyOn(Mozilla.UITour, 'getConfiguration').and.callFake(function(configName, callback) {
                callback({
                    setup: false
                });
            });

            Mozilla.SyncPage.init(config);

            expect(Mozilla.SyncPage.setBodyClass).toHaveBeenCalledWith('state-fx-31-signed-out');
            expect(Mozilla.SyncPage.trackPageState).toHaveBeenCalledWith('Firefox 31 or Higher: Signed-Out');
        });
    });

    describe('SyncPage.ctaSyncClick', function() {
        var config = {
            client: {
                isFirefox: true,
                isFirefoxAndroid: true
            }
        };

        beforeEach(function() {
            Mozilla.UITour.showFirefoxAccounts = sinon.stub();
            spyOn(Mozilla.UITour, 'showFirefoxAccounts');
        });

        it('should pass tracking info', function() {
            Mozilla.SyncPage.init(config);
            Mozilla.SyncPage.ctaSyncClick(new Event('test'));

            expect(Mozilla.SyncPage.dataLayer).toContain({
                event: 'sync-click',
                browser: 'Firefox for Android'
            });
        });

        it('should call showFirefoxAccounts', function() {
            Mozilla.SyncPage.init(config);
            Mozilla.SyncPage.ctaSyncClick(new Event('test'));

            expect(Mozilla.UITour.showFirefoxAccounts).toHaveBeenCalled();
        });
    });
});
