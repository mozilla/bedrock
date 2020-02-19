/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global sinon */
/* eslint camelcase: [2, {properties: "never"}] */
/* eslint new-cap: [2, {"capIsNewExceptions": ["Deferred"]}] */

describe('yandex-scene1.js', function() {
    'use strict';

    beforeEach(function() {
        // stub out Mozilla.Cookie lib
        window.Mozilla.Cookies = sinon.stub();
        window.Mozilla.Cookies.enabled = sinon.stub().returns(true);
        window.Mozilla.Cookies.setItem = sinon.stub();
        window.Mozilla.Cookies.getItem = sinon.stub();
        window.Mozilla.Cookies.hasItem = sinon.stub();

        // stub out google tag manager
        window.dataLayer = sinon.stub();
        window.dataLayer.push = sinon.stub();
    });

    describe('getLocation', function() {

        var xhr;
        var xhrRequests = [];

        beforeEach(function() {
            spyOn(Mozilla.Yandex, 'onRequestComplete');

            xhr = sinon.useFakeXMLHttpRequest();
            xhr.onCreate = function(req) {
                xhrRequests.push(req);
            };
        });

        afterEach(function() {
            xhr.restore();
            xhrRequests = [];
        });

        it('should pass country to onRequestComplete if server makes a response', function() {
            var country = 'ru';

            Mozilla.Yandex.getLocation();

            xhrRequests[0].respond(200, {'Content-Type': 'application/json'}, '{"country_code": "' + country + '"}');

            expect(Mozilla.Yandex.onRequestComplete).toHaveBeenCalledWith(country);
        });

        it('should call onRequestComplete even if server errors out', function() {
            Mozilla.Yandex.getLocation();

            xhrRequests[0].respond(500, '', '');

            expect(Mozilla.Yandex.onRequestComplete).toHaveBeenCalledWith('none');
        });
    });

    describe('hasGeoOverride', function() {

        it('should return a geo value when supplied', function() {
            expect(Mozilla.Yandex.hasGeoOverride('/firefox/new/?geo=ru')).toEqual('ru');
        });

        it('should return false for no override', function() {
            expect(Mozilla.Yandex.hasGeoOverride('/firefox/new/')).toBeFalsy();
        });
    });

    describe('verifyLocation', function() {

        it('should return true if location is correct', function() {
            expect(Mozilla.Yandex.verifyLocation(Mozilla.Yandex.RUSSIA_COUNTRY_CODE)).toBeTruthy();
        });

        it('should return false if location is inocrrect', function() {
            expect(Mozilla.Yandex.verifyLocation('us')).toBeFalsy();
        });
    });

    describe('onRequestComplete', function() {

        var country = 'ru';

        beforeEach(function() {
            spyOn(Mozilla.Yandex, 'updatePageContent');
            spyOn(Mozilla.Yandex, 'setCookie');
        });

        it('should update page content on first call only and set a cookie', function() {
            Mozilla.Yandex.onRequestComplete(country);
            expect(Mozilla.Yandex.updatePageContent).toHaveBeenCalled();
            expect(Mozilla.Yandex.setCookie).toHaveBeenCalledWith(country);

            Mozilla.Yandex.onRequestComplete(country);
            expect(Mozilla.Yandex.updatePageContent).toHaveBeenCalledTimes(1);
            expect(Mozilla.Yandex.setCookie).toHaveBeenCalledTimes(1);
        });
    });

    describe('updatePageContent', function() {

        it('should show Yandex content for users in Russia', function() {
            spyOn(Mozilla.Yandex, 'shouldShowYandex').and.returnValue(true);
            spyOn(Mozilla.Yandex, 'showYandexContent');

            Mozilla.Yandex.updatePageContent();

            expect(Mozilla.Yandex.showYandexContent).toHaveBeenCalled();
        });

        it('should regular content for users not in Russia', function() {
            spyOn(Mozilla.Yandex, 'shouldShowYandex').and.returnValue(false);
            spyOn(Mozilla.Yandex, 'showRegularContent');

            Mozilla.Yandex.updatePageContent();

            expect(Mozilla.Yandex.showRegularContent).toHaveBeenCalled();
        });
    });

    describe('shouldShowYandex', function() {

        it('should return true if criteria is met', function() {
            spyOn(Mozilla.Yandex, 'verifyLocation').and.returnValue(true);

            expect(Mozilla.Yandex.shouldShowYandex()).toBeTruthy();
        });

        it('should return false if one or more of the criteria is not met', function() {
            spyOn(Mozilla.Yandex, 'verifyLocation').and.returnValue(false);

            expect(Mozilla.Yandex.shouldShowYandex()).toBeFalsy();
        });
    });

    describe('cookieExpiresDate', function() {

        it('should return a cookie expiry date 3 days in the future by default', function() {
            var expiry = Mozilla.Yandex.cookieExpiresDate(new Date(2018, 8, 1, 10, 15));
            var date = new Date(expiry);
            expect(date.getFullYear()).toBe(2018);
            expect(date.getMonth()).toBe(8);
            expect(date.getDate()).toBe(4);
        });
    });

    describe('setCookie', function() {

        it('should set session cookies as expected', function() {
            var country = 'ru';
            spyOn(Mozilla.Cookies, 'setItem');

            Mozilla.Yandex.setCookie(country);

            expect(Mozilla.Cookies.setItem).toHaveBeenCalledWith(Mozilla.Yandex.COOKIE_ID, country, jasmine.any(String));
        });
    });

    describe('getCookie', function() {

        it('should return an value as expected', function() {
            spyOn(Mozilla.Cookies, 'getItem');
            Mozilla.Yandex.getCookie(Mozilla.Yandex.COOKIE_ID);
        });
    });

    describe('hasCookie', function() {

        it('should return true if session cookie exists', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            var result = Mozilla.Yandex.hasCookie();
            expect(Mozilla.Cookies.hasItem).toHaveBeenCalledWith(Mozilla.Yandex.COOKIE_ID);
            expect(result).toBeTruthy();
        });

        it('should return false if session cookie does not exist', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(false);
            var result = Mozilla.Yandex.hasCookie();
            expect(result).toBeFalsy();
        });
    });

    describe('init', function() {
        var isDesktop;

        beforeEach(function() {
            isDesktop = Mozilla.Client.isDesktop;
        });

        afterEach(function() {
            Mozilla.Client.isDesktop = isDesktop;
        });

        it('should display Yandex content if override URL is set to Russia', function() {
            var country = 'ru';
            Mozilla.Client.isDesktop = true;
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(Mozilla.Yandex, 'hasGeoOverride').and.returnValue(country);
            spyOn(Mozilla.Yandex, 'verifyLocation').and.callThrough();
            spyOn(Mozilla.Yandex, 'showYandexContent');

            Mozilla.Yandex.init();

            expect(Mozilla.Yandex.verifyLocation).toHaveBeenCalledWith(country);
            expect(Mozilla.Yandex.showYandexContent).toHaveBeenCalled();
        });

        it('should display Regular content if override URL is set to any other value', function() {
            var country = 'us';
            Mozilla.Client.isDesktop = true;
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(Mozilla.Yandex, 'hasGeoOverride').and.returnValue(country);
            spyOn(Mozilla.Yandex, 'verifyLocation').and.callThrough();
            spyOn(Mozilla.Yandex, 'showRegularContent');

            Mozilla.Yandex.init();

            expect(Mozilla.Yandex.verifyLocation).toHaveBeenCalledWith(country);
            expect(Mozilla.Yandex.showRegularContent).toHaveBeenCalled();
        });

        it('should query geo-location if cookie does not exist', function () {
            Mozilla.Client.isDesktop = true;
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(Mozilla.Yandex, 'hasGeoOverride').and.returnValue(false);
            spyOn(Mozilla.Yandex, 'hasCookie').and.returnValue(false);
            spyOn(Mozilla.Yandex, 'getLocation');

            Mozilla.Yandex.init();

            expect(Mozilla.Yandex.getLocation).toHaveBeenCalled();
        });

        it('should only update content if cookie is already set', function () {
            Mozilla.Client.isDesktop = true;
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(Mozilla.Yandex, 'hasGeoOverride').and.returnValue(false);
            spyOn(Mozilla.Yandex, 'hasCookie').and.returnValue(true);
            spyOn(Mozilla.Yandex, 'updatePageContent');
            spyOn(Mozilla.Yandex, 'getLocation');

            Mozilla.Yandex.init();

            expect(Mozilla.Yandex.getLocation).not.toHaveBeenCalled();
            expect(Mozilla.Yandex.updatePageContent).toHaveBeenCalled();
        });

        it('should show regular content if minimum criteria is not met', function () {
            Mozilla.Client.isDesktop = false;
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(false);
            spyOn(Mozilla.Yandex, 'hasGeoOverride').and.returnValue(false);
            spyOn(Mozilla.Yandex, 'showRegularContent');

            Mozilla.Yandex.init();

            expect(Mozilla.Yandex.showRegularContent).toHaveBeenCalled();
        });
    });
});
