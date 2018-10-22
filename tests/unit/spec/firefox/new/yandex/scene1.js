/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon */
/* eslint camelcase: [2, {properties: "never"}] */
/* eslint new-cap: [2, {"capIsNewExceptions": ["Deferred"]}] */

describe('yandex-scene1.js', function() {
    'use strict';

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

        it('should update page content on first call and set a cookie', function() {
            Mozilla.Yandex.onRequestComplete(country);
            expect(Mozilla.Yandex.updatePageContent).toHaveBeenCalled();
            expect(Mozilla.Yandex.setCookie).toHaveBeenCalledWith(country);
        });

        it('should not update page content on second call', function() {
            Mozilla.Yandex.onRequestComplete(country);
            expect(Mozilla.Yandex.updatePageContent).not.toHaveBeenCalled();
            expect(Mozilla.Yandex.setCookie).not.toHaveBeenCalled();
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

    describe('showYandexContent', function() {

        it('should work as expected', function() {
            spyOn(Mozilla.Yandex, 'showYandexBrowserImage');
            spyOn(Mozilla.Yandex, 'showYandexMessaging');

            Mozilla.Yandex.showYandexContent();

            expect(Mozilla.Yandex.showYandexBrowserImage).toHaveBeenCalled();
            expect(Mozilla.Yandex.showYandexMessaging).toHaveBeenCalled();
        });
    });

    describe('showRegularContent', function() {

        it('should work as expected', function() {
            spyOn(Mozilla.Yandex, 'showRegularBrowserImage');
            spyOn(Mozilla.Yandex, 'initOtherPlatformsModal');

            Mozilla.Yandex.showRegularContent();

            expect(Mozilla.Yandex.showRegularBrowserImage).toHaveBeenCalled();
            expect(Mozilla.Yandex.initOtherPlatformsModal).toHaveBeenCalled();
        });
    });

    describe('shouldShowYandex', function() {

        it('should return true if criteria is met', function() {
            spyOn(Mozilla.Yandex, 'verifyLocation').and.returnValue(true);
            spyOn(Mozilla.Yandex, 'getCookie').and.returnValue('yes');

            expect(Mozilla.Yandex.shouldShowYandex()).toBeTruthy();
            expect(Mozilla.Yandex.getCookie).toHaveBeenCalledWith(Mozilla.Yandex.COOKIE_YANDEX_COHORT);
        });

        it('should return false if one or more of the criteria is not met', function() {
            spyOn(Mozilla.Yandex, 'verifyLocation').and.returnValue(false);

            expect(Mozilla.Yandex.shouldShowYandex()).toBeFalsy();
        });
    });

    describe('showYandexBrowserImage, showRegularBrowserImage', function() {

        var header;

        beforeEach(function() {
            var frag = document.createDocumentFragment();
            var image = document.createElement('img');
            header = document.createElement('div');

            header.className = 'header-image';
            image.src = '/img/placeholder.png';
            image.setAttribute('data-yandex-src', '/img/low-res.png');
            image.setAttribute('data-yandex-srcset', '/img/high-res.png');
            image.setAttribute('data-firefox-src', '/img/browser-windows.png');
            image.setAttribute('data-firefox-srcset', '/img/browser-windows-high-res.png');

            frag.appendChild(header);
            header.appendChild(image);

            document.body.appendChild(frag);
        });

        afterEach(function() {
            document.body.removeChild(header);
        });

        it('should update image for Yandex', function() {
            Mozilla.Yandex.showYandexBrowserImage();

            var image = document.querySelector('.header-image > img');
            expect(image.src).toContain('/img/low-res.png');
            expect(image.srcset).toContain('/img/high-res.png');
        });

        it('should update image for regular firefox', function() {
            Mozilla.Yandex.showRegularBrowserImage();

            var image = document.querySelector('.header-image > img');
            expect(image.src).toContain('/img/browser-windows.png');
            expect(image.srcset).toContain('/img/browser-windows-high-res.png');
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
            spyOn(Mozilla.Yandex, 'isWithinSampleRate').and.returnValue(true);

            Mozilla.Yandex.setCookie(country);

            expect(Mozilla.Yandex.isWithinSampleRate).toHaveBeenCalled();
            expect(Mozilla.Cookies.setItem.calls.count()).toEqual(2);
            expect(Mozilla.Cookies.setItem).toHaveBeenCalledWith(Mozilla.Yandex.COOKIE_ID, country, jasmine.any(String));
            expect(Mozilla.Cookies.setItem).toHaveBeenCalledWith(Mozilla.Yandex.COOKIE_YANDEX_COHORT, 'yes', jasmine.any(String));
        });
    });

    describe('getCookie', function() {

        it('should return an value as expected', function() {
            spyOn(Mozilla.Cookies, 'getItem');
            Mozilla.Yandex.getCookie(Mozilla.Yandex.COOKIE_ID);
            expect(Mozilla.Cookies.getItem).toHaveBeenCalledWith(Mozilla.Yandex.COOKIE_ID);
        });
    });

    describe('hasCookie', function() {

        it('should return true if both session cookies exists', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            var result = Mozilla.Yandex.hasCookie();
            expect(Mozilla.Cookies.hasItem.calls.count()).toEqual(2);
            expect(Mozilla.Cookies.hasItem).toHaveBeenCalledWith(Mozilla.Yandex.COOKIE_ID);
            expect(Mozilla.Cookies.hasItem).toHaveBeenCalledWith(Mozilla.Yandex.COOKIE_YANDEX_COHORT);
            expect(result).toBeTruthy();
        });

        it('should return false if one or more session cookies do not exist', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.callFake(function(id) {
                return id === Mozilla.Yandex.COOKIE_ID ? true : false;
            });
            var result = Mozilla.Yandex.hasCookie();
            expect(Mozilla.Cookies.hasItem.calls.count()).toEqual(2);
            expect(result).toBeFalsy();
        });
    });

    describe('isWithinSampleRate', function() {

        it('should return true if within sample rate', function() {
            spyOn(window.Math, 'random').and.returnValue(0.8);
            expect(Mozilla.Yandex.isWithinSampleRate()).toBeTruthy();
        });

        it('should return false if exceeds sample rate', function() {
            spyOn(window.Math, 'random').and.returnValue(1);
            expect(Mozilla.Yandex.isWithinSampleRate()).toBeFalsy();
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
