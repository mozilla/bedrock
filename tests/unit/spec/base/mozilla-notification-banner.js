/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon */

describe('mozilla-notification-banner.js', function() {

    'use strict';

    beforeEach(function() {
        // stub out Mozilla.Cookie lib
        window.Mozilla.Cookies = sinon.stub();
        window.Mozilla.Cookies.enabled = sinon.stub().returns(true);
        window.Mozilla.Cookies.setItem = sinon.stub();
        window.Mozilla.Cookies.getItem = sinon.stub();
        window.Mozilla.Cookies.hasItem = sinon.stub();
    });

    describe('init', function() {

        var options = {
            'id': 'fx-out-of-date-banner-copy1-direct-1',
            'name': 'fx-out-of-date',
            'experimentName': 'fx-out-of-date-banner-copy1',
            'experimentVariant': 'direct-1',
            'heading': 'Your browser security is at risk.',
            'message': 'Update Firefox now to protect yourself from the latest malware.',
            'confirm': 'Update now',
            'confirmAction': 'Update Firefox',
            'confirmLabel': 'Firefox for Desktop',
            'url': '/firefox/new/?scene=2',
            'close': 'Close',
            'closeLabel': 'Close'
        };

        it('should call show() if cookie does not exist', function() {
            spyOn(Mozilla.NotificationBanner, 'cutsTheMustard').and.returnValue(true);
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue(null);
            spyOn(Mozilla.NotificationBanner, 'show');
            Mozilla.NotificationBanner.init(options);
            expect(Mozilla.NotificationBanner.show).toHaveBeenCalled();
        });

        it('should call show() if cookie value does not equal "interacted', function() {
            spyOn(Mozilla.NotificationBanner, 'cutsTheMustard').and.returnValue(true);
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue('foo');
            spyOn(Mozilla.NotificationBanner, 'show');
            Mozilla.NotificationBanner.init(options);
            expect(Mozilla.NotificationBanner.show).toHaveBeenCalled();
        });

        it('should not call show() if cookie has value equals "interacted"', function() {
            spyOn(Mozilla.NotificationBanner, 'cutsTheMustard').and.returnValue(true);
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue(Mozilla.NotificationBanner.COOKIE_INTERACTION_VALUE);
            spyOn(Mozilla.NotificationBanner, 'show');
            Mozilla.NotificationBanner.init(options);
            expect(Mozilla.NotificationBanner.show).not.toHaveBeenCalled();
        });

        it('should not call show() if options is undefined', function() {
            spyOn(Mozilla.NotificationBanner, 'cutsTheMustard').and.returnValue(true);
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue('foo');
            spyOn(Mozilla.NotificationBanner, 'show');
            Mozilla.NotificationBanner.init(undefined);
            expect(Mozilla.NotificationBanner.show).not.toHaveBeenCalled();
        });

        it('should not call show() if browser is not supported', function() {
            spyOn(Mozilla.NotificationBanner, 'cutsTheMustard').and.returnValue(false);
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue('foo');
            spyOn(Mozilla.NotificationBanner, 'show');
            Mozilla.NotificationBanner.init(options);
            expect(Mozilla.NotificationBanner.show).not.toHaveBeenCalled();
        });

        it('should not call show() if options are not satisfied', function() {
            spyOn(Mozilla.NotificationBanner, 'cutsTheMustard').and.returnValue(true);
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue(null);
            spyOn(Mozilla.NotificationBanner, 'validateOptions').and.returnValue(false);
            spyOn(Mozilla.NotificationBanner, 'show');
            Mozilla.NotificationBanner.init(options);
            expect(Mozilla.NotificationBanner.show).not.toHaveBeenCalled();
        });
    });

    describe('validateOptions', function() {

        it('should return true if options are all satisfied', function() {
            var options = {
                'id': 'fx-out-of-date-banner-copy1-direct-1',
                'name': 'fx-out-of-date',
                'heading': 'Your browser security is at risk.',
                'message': 'Update Firefox now to protect yourself from the latest malware.',
                'confirm': 'Update now',
                'confirmAction': 'Update Firefox',
                'confirmLabel': 'Firefox for Desktop',
                'url': '/firefox/new/?scene=2',
                'close': 'Close',
                'closeLabel': 'Close'
            };

            expect(Mozilla.NotificationBanner.validateOptions(options)).toBeTruthy();
        });

        it('should return false if any options are not satisfied', function() {
            var options = {
                // id is missing
                'name': 'fx-out-of-date',
                'heading': 'Your browser security is at risk.',
                'message': 'Update Firefox now to protect yourself from the latest malware.',
                'confirm': 'Update now',
                'confirmAction': 'Update Firefox',
                'confirmLabel': 'Firefox for Desktop',
                'url': '/firefox/new/?scene=2',
                'close': 'Close',
                'closeLabel': 'Close'
            };

            expect(Mozilla.NotificationBanner.validateOptions(options)).toBeFalsy();
        });
    });

    describe('show', function() {

        it('should display the notification and set a cookie', function() {
            var options = {
                'id': 'fx-out-of-date-banner-copy1-direct-1',
                'name': 'fx-out-of-date',
                'experimentName': 'fx-out-of-date-banner-copy1',
                'experimentVariant': 'direct-1',
                'heading': 'Your browser security is at risk.',
                'message': 'Update Firefox now to protect yourself from the latest malware.',
                'confirm': 'Update now',
                'confirmAction': 'Update Firefox',
                'confirmLabel': 'Firefox for Desktop',
                'url': '/firefox/new/?scene=2',
                'close': 'Close',
                'closeLabel': 'Close'
            };

            spyOn(Mozilla.NotificationBanner, 'bind');
            spyOn(Mozilla.NotificationBanner, 'setCookie');
            spyOn(Mozilla.NotificationBanner, 'trackGAShow');
            Mozilla.NotificationBanner.show(options);

            var notification = document.querySelector('.notification-banner');

            expect(notification).not.toEqual(null);
            expect(Mozilla.NotificationBanner.bind).toHaveBeenCalled();
            expect(Mozilla.NotificationBanner.setCookie).toHaveBeenCalledWith(options.id);
            expect(Mozilla.NotificationBanner.trackGAShow).toHaveBeenCalledWith(options);
            document.body.removeChild(notification);
        });
    });

    describe('trackGAShow', function() {

        it('should push data to GA as expected', function() {
            var options = {
                'id': 'fx-out-of-date-banner-copy1-direct-1',
                'name': 'fx-out-of-date',
                'heading': 'Your browser security is at risk.',
                'message': 'Update Firefox now to protect yourself from the latest malware.',
                'confirm': 'Update now',
                'confirmAction': 'Update Firefox',
                'confirmLabel': 'Firefox for Desktop',
                'url': '/firefox/new/?scene=2',
                'close': 'Close',
                'closeLabel': 'Close'
            };

            spyOn(window.dataLayer, 'push');
            Mozilla.NotificationBanner.trackGAShow(options);
            expect(window.dataLayer.push).toHaveBeenCalledWith({
                'data-banner-name': 'fx-out-of-date',
                'data-banner-impression': '1',
                'event': 'non-interaction'
            });
        });

        it('should push extra data to GA for experiment tracking', function() {
            var options = {
                'id': 'fx-out-of-date-banner-copy1-direct-1',
                'name': 'fx-out-of-date',
                'experimentName': 'fx-out-of-date-banner-copy1',
                'experimentVariant': 'direct-1',
                'heading': 'Your browser security is at risk.',
                'message': 'Update Firefox now to protect yourself from the latest malware.',
                'confirm': 'Update now',
                'confirmAction': 'Update Firefox',
                'confirmLabel': 'Firefox for Desktop',
                'url': '/firefox/new/?scene=2',
                'close': 'Close',
                'closeLabel': 'Close'
            };

            spyOn(window.dataLayer, 'push');
            Mozilla.NotificationBanner.trackGAShow(options);
            expect(window.dataLayer.push).toHaveBeenCalledWith({
                'data-banner-name': 'fx-out-of-date',
                'data-banner-impression': '1',
                'event': 'non-interaction',
                'data-ex-variant': 'direct-1',
                'data-ex-experiment': 'fx-out-of-date-banner-copy1',
                'data-ex-present': 'true'
            });
        });
    });

    describe('create', function() {

        it('should return a properly formed notification DOM element', function() {
            var options = {
                'id': 'fx-out-of-date-banner-copy1-direct-1',
                'name': 'fx-out-of-date',
                'experimentName': 'fx-out-of-date-banner-copy1',
                'experimentVariant': 'direct-1',
                'heading': 'Your browser security is at risk.',
                'message': 'Update Firefox now to protect yourself from the latest malware.',
                'confirm': 'Update now',
                'confirmAction': 'Update Firefox',
                'confirmLabel': 'Firefox for Desktop',
                'url': '/firefox/new/?scene=2',
                'close': 'Close',
                'closeLabel': 'Close'
            };

            var notification = Mozilla.NotificationBanner.create(options);

            expect(notification.querySelector('h2').innerText).toEqual(options.heading);
            expect(notification.querySelector('p').innerText).toEqual(options.message);
            expect(notification.querySelector('a').innerText).toEqual(options.confirm);
            expect(notification.querySelector('a').href).toContain(options.url);
            expect(notification.querySelector('button').innerText).toEqual(options.close);
        });
    });

    describe('confirm', function() {

        it('should set a cookie before redirecting for regular click', function() {
            var event = {
                'metaKey': false,
                'ctrlKey': false,
                'target': '/firefox/new/?scene=2',
                'preventDefault': function () {}
            };

            spyOn(Mozilla.NotificationBanner, 'setCookie');
            spyOn(Mozilla.NotificationBanner, 'doRedirect');
            spyOn(Mozilla.NotificationBanner, 'trackGAConfirm');
            spyOn(event, 'preventDefault');
            Mozilla.NotificationBanner.confirm(event);
            expect(event.preventDefault).toHaveBeenCalled();
            expect(Mozilla.NotificationBanner.setCookie).toHaveBeenCalledWith(Mozilla.NotificationBanner.COOKIE_INTERACTION_VALUE);
            expect(Mozilla.NotificationBanner.doRedirect).toHaveBeenCalledWith(event.target);
            expect(Mozilla.NotificationBanner.trackGAConfirm).toHaveBeenCalled();
        });

        it('should only set cookie for control click', function() {
            var event = {
                'metaKey': false,
                'ctrlKey': true,
                'target': '/firefox/new/?scene=2',
                'preventDefault': function () {}
            };

            spyOn(Mozilla.NotificationBanner, 'setCookie');
            spyOn(Mozilla.NotificationBanner, 'doRedirect');
            spyOn(Mozilla.NotificationBanner, 'trackGAConfirm');
            spyOn(event, 'preventDefault');
            Mozilla.NotificationBanner.confirm(event);
            expect(event.preventDefault).not.toHaveBeenCalled();
            expect(Mozilla.NotificationBanner.setCookie).toHaveBeenCalledWith(Mozilla.NotificationBanner.COOKIE_INTERACTION_VALUE);
            expect(Mozilla.NotificationBanner.doRedirect).not.toHaveBeenCalled();
            expect(Mozilla.NotificationBanner.trackGAConfirm).toHaveBeenCalled();
        });

        it('should execute a callback if supplied', function() {
            var options = {
                'id': 'fx-out-of-date-banner-copy1-direct-1',
                'name': 'fx-out-of-date',
                'experimentName': 'fx-out-of-date-banner-copy1',
                'experimentVariant': 'direct-1',
                'heading': 'Your browser security is at risk.',
                'message': 'Update Firefox now to protect yourself from the latest malware.',
                'confirm': 'Update now',
                'confirmAction': 'Update Firefox',
                'confirmLabel': 'Firefox for Desktop',
                'url': '/firefox/new/?scene=2',
                'close': 'Close',
                'closeLabel': 'Close',
                confirmClick: function() {}
            };

            var event = {
                'metaKey': false,
                'ctrlKey': false,
                'target': '/firefox/new/?scene=2',
                'preventDefault': function () {}
            };

            spyOn(Mozilla.NotificationBanner, 'cutsTheMustard').and.returnValue(true);
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue(null);
            spyOn(Mozilla.NotificationBanner, 'show');
            spyOn(Mozilla.NotificationBanner, 'setCookie');
            spyOn(Mozilla.NotificationBanner, 'doRedirect');
            spyOn(Mozilla.NotificationBanner, 'trackGAConfirm');
            spyOn(event, 'preventDefault');
            spyOn(options, 'confirmClick');
            Mozilla.NotificationBanner.init(options);
            Mozilla.NotificationBanner.confirm(event);
            expect(event.preventDefault).toHaveBeenCalled();
            expect(options.confirmClick).toHaveBeenCalled();
            expect(Mozilla.NotificationBanner.setCookie).toHaveBeenCalledWith(Mozilla.NotificationBanner.COOKIE_INTERACTION_VALUE);
            expect(Mozilla.NotificationBanner.trackGAConfirm).toHaveBeenCalled();
            expect(Mozilla.NotificationBanner.doRedirect).not.toHaveBeenCalled();
        });
    });

    describe('close', function() {

        var notification;

        beforeEach(function() {
            var options = {
                'id': 'fx-out-of-date-banner-copy1-direct-1',
                'name': 'fx-out-of-date',
                'experimentName': 'fx-out-of-date-banner-copy1',
                'experimentVariant': 'direct-1',
                'heading': 'Your browser security is at risk.',
                'message': 'Update Firefox now to protect yourself from the latest malware.',
                'confirm': 'Update now',
                'confirmAction': 'Update Firefox',
                'confirmLabel': 'Firefox for Desktop',
                'url': '/firefox/new/?scene=2',
                'close': 'Close',
                'closeLabel': 'Close'
            };

            spyOn(Mozilla.NotificationBanner, 'bind');
            spyOn(Mozilla.NotificationBanner, 'trackGAClose');
            Mozilla.NotificationBanner.show(options);
            notification = document.querySelector('.notification-banner');
            expect(notification).not.toEqual(null);
            expect(Mozilla.NotificationBanner.bind).toHaveBeenCalled();
        });

        it('should remove the notification from the DOM and set a cookie', function() {
            spyOn(Mozilla.NotificationBanner, 'setCookie');
            Mozilla.NotificationBanner.close();
            expect(notification).not.toEqual(null);
            expect(Mozilla.NotificationBanner.setCookie).toHaveBeenCalledWith(Mozilla.NotificationBanner.COOKIE_INTERACTION_VALUE);
            expect(Mozilla.NotificationBanner.trackGAClose).toHaveBeenCalled();
        });
    });

    describe('setCookie', function() {

        it('should set a cookie as expected', function() {
            spyOn(Mozilla.Cookies, 'setItem');
            Mozilla.NotificationBanner.setCookie('foo');
            expect(Mozilla.Cookies.setItem).toHaveBeenCalledWith(Mozilla.NotificationBanner.COOKIE_CODE_ID, 'foo', jasmine.any(String), '/');
        });
    });

    describe('cookieExpiresDate', function() {

        it('should return a cookie expiry date 21 days in the future by default', function() {
            var expiry = Mozilla.NotificationBanner.cookieExpiresDate(new Date(2017, 6, 1, 10, 15));
            var date = new Date(expiry);
            expect(date.getFullYear()).toBe(2017);
            expect(date.getMonth()).toBe(6);
            expect(date.getDate()).toBe(22);
        });
    });

    describe('getCookie', function() {

        it('should return value if the cookie exists', function() {
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('foo');
            var cookie = Mozilla.NotificationBanner.getCookie();
            expect(Mozilla.Cookies.getItem).toHaveBeenCalledWith(Mozilla.NotificationBanner.COOKIE_CODE_ID);
            expect(cookie).toEqual('foo');
        });

        it('should return null if the cookie does not exist', function() {
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue(null);
            var cookie = Mozilla.NotificationBanner.getCookie();
            expect(Mozilla.Cookies.getItem).toHaveBeenCalledWith(Mozilla.NotificationBanner.COOKIE_CODE_ID);
            expect(cookie).toEqual(null);
        });
    });

    describe('setSampleRate', function() {

        afterEach(function() {
            Mozilla.NotificationBanner.setSampleRate(0);
        });

        it('should set the sample rate as expected', function() {
            Mozilla.NotificationBanner.setSampleRate(0.05);
            var result = Mozilla.NotificationBanner.getSampleRate();
            expect(result).toEqual(0.05);
        });

        it('should not set values less than 0 or exceeding 1', function() {
            Mozilla.NotificationBanner.setSampleRate(-1);
            var result = Mozilla.NotificationBanner.getSampleRate();
            expect(result).toEqual(0);

            Mozilla.NotificationBanner.setSampleRate(2);
            var result2 = Mozilla.NotificationBanner.getSampleRate();
            expect(result2).toEqual(1);
        });

        it('should not set invalid types', function() {
            Mozilla.NotificationBanner.setSampleRate(null);
            var result = Mozilla.NotificationBanner.getSampleRate();
            expect(result).toEqual(0);

            Mozilla.NotificationBanner.setSampleRate('foo');
            var result2 = Mozilla.NotificationBanner.getSampleRate();
            expect(result2).toEqual(0);

            Mozilla.NotificationBanner.setSampleRate(true);
            var result3 = Mozilla.NotificationBanner.getSampleRate();
            expect(result3).toEqual(0);

            Mozilla.NotificationBanner.setSampleRate('');
            var result4 = Mozilla.NotificationBanner.getSampleRate();
            expect(result4).toEqual(0);
        });
    });

    describe('withinSampleRate', function() {

        beforeEach(function() {
            Mozilla.NotificationBanner.setSampleRate(0.05);
        });

        afterEach(function() {
            Mozilla.NotificationBanner.setSampleRate(0);
        });

        it('should return true if within rate limit', function() {
            spyOn(Math, 'random').and.returnValue(0.04);
            var result = Mozilla.NotificationBanner.withinSampleRate();
            expect(result).toBeTruthy();
        });

        it('should return false if exceeding rate limit', function() {
            spyOn(Math, 'random').and.returnValue(0.06);
            var result = Mozilla.NotificationBanner.withinSampleRate();
            expect(result).toBeFalsy();
        });

        it('should return true if sample rate is not set', function() {
            Mozilla.NotificationBanner.setSampleRate(0);
            var result = Mozilla.NotificationBanner.withinSampleRate();
            expect(result).toBeTruthy();

            Mozilla.NotificationBanner.setSampleRate(null);
            var result1 = Mozilla.NotificationBanner.withinSampleRate();
            expect(result1).toBeTruthy();
        });
    });

    describe('getOptions', function() {

        var _options = [
            {
                'id': 'fx-out-of-date-banner-copy1-direct-1',
                'name': 'fx-out-of-date',
                'experimentName': 'fx-out-of-date-banner-copy1',
                'experimentVariant': 'direct-1',
                'heading': 'Your browser security is at risk.',
                'message': 'Update Firefox now to protect yourself from the latest malware.',
                'confirm': 'Update now',
                'confirmAction': 'Update Firefox',
                'confirmLabel': 'Firefox for Desktop',
                'url': '/firefox/new/?scene=2',
                'close': 'Close',
                'closeLabel': 'Close',
            },
            {
                'id': 'fx-out-of-date-banner-copy1-direct-2',
                'name': 'fx-out-of-date',
                'experimentName': 'fx-out-of-date-banner-copy1',
                'experimentVariant': 'direct-2',
                'heading': 'Your Firefox is out-of-date.',
                'message': 'Get the most recent version to keep browsing securely.',
                'confirm': 'Update Firefox',
                'confirmAction': 'Update Firefox',
                'confirmLabel': 'Firefox for Desktop',
                'url': '/firefox/new/?scene=2',
                'close': 'Close',
                'closeLabel': 'Close'
            },
            {
                'id': 'fx-out-of-date-banner-copy1-foxy-1',
                'name': 'fx-out-of-date',
                'experimentName': 'fx-out-of-date-banner-copy1',
                'experimentVariant': 'foxy-1',
                'heading': 'Psst… it’s time for a tune up',
                'message': 'Stay safe and fast with a quick update.',
                'confirm': 'Update Firefox',
                'confirmAction': 'Update Firefox',
                'confirmLabel': 'Firefox for Desktop',
                'url': '/firefox/new/?scene=2',
                'close': 'Close',
                'closeLabel': 'Close'
            }
        ];

        it('should return a config if a cookie exists', function() {
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue('fx-out-of-date-banner-copy1-foxy-1');
            var choice = Mozilla.NotificationBanner.getOptions(_options);
            expect(choice).toEqual(_options[2]);
        });

        it('should return null if a non-matching cookie exists', function() {
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue('foo');
            var choice = Mozilla.NotificationBanner.getOptions(_options);
            expect(choice).toEqual(null);
        });

        it('should return an options object if within rate limiting', function() {
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue(null);
            spyOn(Mozilla.NotificationBanner, 'withinSampleRate').and.returnValue(true);
            var choice = Mozilla.NotificationBanner.getOptions(_options, true);
            expect(choice).not.toEqual(null);
        });

        it('should return an null if exceeding rate limiting', function() {
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue(null);
            spyOn(Mozilla.NotificationBanner, 'withinSampleRate').and.returnValue(false);
            var choice = Mozilla.NotificationBanner.getOptions(_options, true);
            expect(choice).toEqual(null);
        });

        it('should return a randomly selected config', function() {
            spyOn(Mozilla.NotificationBanner, 'getCookie').and.returnValue(null);
            spyOn(Math, 'random').and.returnValue(1);
            var choice = Mozilla.NotificationBanner.getOptions(_options);
            expect(choice).toEqual(_options[3]);
        });
    });
});
