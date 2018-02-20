/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon */
/* eslint new-cap: [2, {"capIsNewExceptions": ["Deferred"]}] */

describe('stub-attribution.js', function() {

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

        var data = {};

        beforeEach(function() {
            /* eslint-disable camelcase */
            data = {
                utm_source: 'foo',
                utm_medium: 'bar',
                utm_campaign: 'fizz',
                utm_content: 'buzz',
                referrer: 'https://www.google.com'
            };
            /* eslint-enable camelcase */

            spyOn(Mozilla.StubAttribution, 'requestAuthentication');
            spyOn(Mozilla.StubAttribution, 'updateBouncerLinks');
        });

        it('should update download links if session cookie exists', function() {
            /* eslint-disable camelcase */
            var cookieData = {
                attribution_code: 'foo',
                attribution_sig: 'bar'
            };
            /* eslint-enable camelcase */
            spyOn(Mozilla.StubAttribution, 'withinAttributionRate').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'getCookie').and.returnValue(cookieData);
            Mozilla.StubAttribution.init();
            expect(Mozilla.StubAttribution.requestAuthentication).not.toHaveBeenCalled();
            expect(Mozilla.StubAttribution.updateBouncerLinks).toHaveBeenCalledWith(cookieData);
        });

        it('should authenticate attribution data if none exists', function() {
            spyOn(Mozilla.StubAttribution, 'withinAttributionRate').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'isFirefoxNewScene2').and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'getAttributionData').and.returnValue(data);
            Mozilla.StubAttribution.init();
            expect(Mozilla.StubAttribution.requestAuthentication).toHaveBeenCalledWith(data);
            expect(Mozilla.StubAttribution.updateBouncerLinks).not.toHaveBeenCalled();
        });

        it('should do nothing if stub attribution requirements are not satisfied', function() {
            spyOn(Mozilla.StubAttribution, 'withinAttributionRate').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'isFirefoxNewScene2').and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'getAttributionData').and.returnValue(data);
            Mozilla.StubAttribution.init();
            expect(Mozilla.StubAttribution.requestAuthentication).not.toHaveBeenCalled();
            expect(Mozilla.StubAttribution.updateBouncerLinks).not.toHaveBeenCalled();
        });

        it('should do nothing if session is not within sample rate', function() {
            spyOn(Mozilla.StubAttribution, 'withinAttributionRate').and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'isFirefoxNewScene2').and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'getAttributionData').and.returnValue(data);
            Mozilla.StubAttribution.init();
            expect(Mozilla.StubAttribution.requestAuthentication).not.toHaveBeenCalled();
            expect(Mozilla.StubAttribution.updateBouncerLinks).not.toHaveBeenCalled();
        });

        it('should do nothing if page is scene2 of /firefox/new/', function() {
            spyOn(Mozilla.StubAttribution, 'withinAttributionRate').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'isFirefoxNewScene2').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'getAttributionData').and.returnValue(data);
            Mozilla.StubAttribution.init();
            expect(Mozilla.StubAttribution.requestAuthentication).not.toHaveBeenCalled();
            expect(Mozilla.StubAttribution.updateBouncerLinks).not.toHaveBeenCalled();
        });
    });

    describe('meetsRequirements', function() {

        afterEach(function() {
            window.site.platform = 'other';
        });

        it('should return false if cookies are not enabled', function() {
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(false);
            expect(Mozilla.StubAttribution.meetsRequirements()).toBeFalsy();
        });

        it('should return false if platform is not windows', function() {
            window.site.platform = 'osx';
            expect(Mozilla.StubAttribution.meetsRequirements()).toBeFalsy();
        });

        it('should return false if browser requires sha-1 bouncer', function() {
            spyOn(window.site, 'needsSha1').and.returnValue(true);
            expect(Mozilla.StubAttribution.meetsRequirements()).toBeFalsy();
        });

        it('should return false if browser has DNT enabled', function() {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(true);
            expect(Mozilla.StubAttribution.meetsRequirements()).toBeFalsy();
        });

        it('should return true for windows users who satisfy all other requirements', function() {
            window.site.platform = 'windows';
            spyOn(window.site, 'needsSha1').and.returnValue(false);
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            expect(Mozilla.StubAttribution.meetsRequirements()).toBeTruthy();
        });
    });

    describe('isFirefoxNewScene2', function() {

        it('should return true if the page is scene 2 of /firefox/new/', function() {
            var url = 'https://www.mozilla.org/en-US/firefox/download/thanks/';
            expect(Mozilla.StubAttribution.isFirefoxNewScene2(url)).toBeTruthy();

            var url2 = 'https://www.mozilla.org/en-US/firefox/download/thanks/?foo=bar';
            expect(Mozilla.StubAttribution.isFirefoxNewScene2(url2)).toBeTruthy();
        });
    });

    describe('getAttributionData', function() {

        it('should return attribution data if utm params are present', function() {
            /* eslint-disable camelcase */
            var data = {
                utm_source: 'foo',
                utm_medium: 'bar',
                utm_campaign: 'fizz',
                utm_content: 'buzz',
                referrer: ''
            };
            /* eslint-enable camelcase */

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(data);
            spyOn(window.site, 'needsSha1').and.returnValue(false);
            var result = Mozilla.StubAttribution.getAttributionData('');
            expect(result).toEqual(data);
        });

        it('should return attribution data if referrer is present', function() {
            /* eslint-disable camelcase */
            var data = {
                utm_source: undefined,
                utm_medium: undefined,
                utm_campaign: undefined,
                utm_content: undefined,
                referrer: 'https://www.mozilla.org/en-US/'
            };
            /* eslint-enable camelcase */
            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue({});
            spyOn(window.site, 'needsSha1').and.returnValue(false);
            var result = Mozilla.StubAttribution.getAttributionData('https://www.mozilla.org/en-US/');
            expect(result).toEqual(data);
        });

        it('should return false if neither utm params and referrer are present', function() {
            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue({});
            spyOn(window.site, 'needsSha1').and.returnValue(false);
            var result = Mozilla.StubAttribution.getAttributionData('');
            expect(result).toBeFalsy();
        });
    });

    describe('requestAuthentication', function() {

        it('should handle a request successfully', function() {
            /* eslint-disable camelcase */
            var data = {
                attribution_code: 'foo',
                attribution_sig: 'bar'
            };
            /* eslint-enable camelcase */

            spyOn($, 'get').and.callFake(function () {
                var d = $.Deferred();
                d.resolve(data);
                return d.promise();
            });

            spyOn(Mozilla.StubAttribution, 'onRequestSuccess');
            Mozilla.StubAttribution.requestAuthentication();
            expect(Mozilla.StubAttribution.onRequestSuccess).toHaveBeenCalledWith(data);
        });
    });

    describe('onRequestSuccess', function() {

        it('should handle the data as expected', function() {
            /* eslint-disable camelcase */
            var data = {
                attribution_code: 'foo',
                attribution_sig: 'bar'
            };
            /* eslint-enable camelcase */

            spyOn(Mozilla.StubAttribution, 'updateBouncerLinks');
            spyOn(Mozilla.StubAttribution, 'setCookie');
            Mozilla.StubAttribution.onRequestSuccess(data);
            expect(Mozilla.StubAttribution.updateBouncerLinks).toHaveBeenCalledWith(data);
            expect(Mozilla.StubAttribution.setCookie).toHaveBeenCalledWith(data);
        });
    });

    describe('updateBouncerLinks', function() {

        /* eslint-disable camelcase */
        var data = {
            attribution_code: 'foo',
            attribution_sig: 'bar'
        };
        /* eslint-enable camelcase */

        var sha1Url = 'https://download-sha1.allizom.org/?product=firefox-stub&os=win&lang=en-US';
        var winUrl = 'https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US';
        var win64Url = 'https://download.mozilla.org/?product=firefox-50.0b11-SSL&os=win64&lang=en-US';
        var transitionalUrl = '/firefox/download/thanks/';

        beforeEach(function() {
            var downloadMarkup = '<ul class="download-list">' +
                                    '<li><a class="download-link" data-download-version="win" href="' + transitionalUrl +'">Download</a></li>' +
                                    '<li><a class="download-link" data-download-version="winsha1" href="' + sha1Url +'">Download</a></li>' +
                                    '<li><a class="download-link" data-download-version="win" href="' + winUrl+ '">Download</a></li>' +
                                    '<li><a class="download-link" data-download-version="win64" href="' + win64Url + '">Download</a></li>' +
                                 '</ul>';
            $(downloadMarkup).appendTo('body');
        });

        afterEach(function() {
            $('.download-list').remove();
        });

        it('should update download links with attribution data as expected', function() {
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'appendToDownloadURL');
            Mozilla.StubAttribution.updateBouncerLinks(data);
            expect(Mozilla.StubAttribution.appendToDownloadURL.calls.count()).toEqual(2);
            expect(Mozilla.StubAttribution.appendToDownloadURL).toHaveBeenCalledWith(winUrl, data);
            expect(Mozilla.StubAttribution.appendToDownloadURL).toHaveBeenCalledWith(win64Url, data);
        });

        it('should do nothing if stub attribution requirements are not satisfied', function() {
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'appendToDownloadURL');
            Mozilla.StubAttribution.updateBouncerLinks(data);
            expect(Mozilla.StubAttribution.appendToDownloadURL).not.toHaveBeenCalled();
        });

        it('should do nothing if attribution data is not as expected', function() {
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'appendToDownloadURL');
            Mozilla.StubAttribution.updateBouncerLinks({});
            expect(Mozilla.StubAttribution.appendToDownloadURL).not.toHaveBeenCalled();
        });
    });

    describe('appendToDownloadURL', function() {

        var params = {};
        var originalUrl = '';
        var expectedUrl = '';

        beforeEach(function() {
            /* eslint-disable camelcase */
            params = {
                attribution_code: 'source%3Dbrandt%26medium%3Daether%26campaign%3D%28not+set%29%26content%3D%28not+set%29%26timestamp%3D1478181983',
                attribution_sig: '241c4ef87bd2554154c5658d99230660d4c242abbe1ac87b89ac0e9dd56b2f4e'
            };
            /* eslint-enable camelcase */

            originalUrl = 'https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US';
            expectedUrl = 'https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US&attribution_code=source%3Dbrandt%26medium%3Daether%26campaign%3D%28not+set%29%26content%3D%28not+set%29%26timestamp%3D1478181983&attribution_sig=241c4ef87bd2554154c5658d99230660d4c242abbe1ac87b89ac0e9dd56b2f4e';
        });

        it('should append stub attribution data to url', function() {
            expect(Mozilla.StubAttribution.appendToDownloadURL(originalUrl, params)).toEqual(expectedUrl);
        });

        it('should return original url if stub attribution data is missing', function() {
            params = {};
            expect(Mozilla.StubAttribution.appendToDownloadURL(originalUrl, params)).toEqual(originalUrl);
        });

        it('should ignore any other parameters', function() {
            params['foo'] = 'bar';
            expect(Mozilla.StubAttribution.appendToDownloadURL(originalUrl, params)).toEqual(expectedUrl);
        });
    });

    describe('getCookie', function() {

        it('should return an object as expected', function() {
            spyOn(Mozilla.Cookies, 'getItem').and.callFake(function(id) {
                return id === Mozilla.StubAttribution.COOKIE_CODE_ID ? 'foo' : 'bar';
            });
            /* eslint-disable camelcase */
            expect(Mozilla.StubAttribution.getCookie()).toEqual({
                attribution_code: 'foo',
                attribution_sig: 'bar'
            });
            /* eslint-enable camelcase */
            expect(Mozilla.Cookies.getItem.calls.count()).toEqual(2);
        });
    });

    describe('setCookie', function() {

        beforeEach(function() {
            spyOn(Mozilla.Cookies, 'setItem');
        });

        it('should set session cookies as expected', function() {
            /* eslint-disable camelcase */
            var data = {
                attribution_code: 'foo',
                attribution_sig: 'bar'
            };
            /* eslint-enable camelcase */

            Mozilla.StubAttribution.setCookie(data);
            expect(Mozilla.Cookies.setItem.calls.count()).toEqual(2);
            expect(Mozilla.Cookies.setItem).toHaveBeenCalledWith(Mozilla.StubAttribution.COOKIE_CODE_ID, data.attribution_code, jasmine.any(String), '/');
            expect(Mozilla.Cookies.setItem).toHaveBeenCalledWith(Mozilla.StubAttribution.COOKIE_SIGNATURE_ID, data.attribution_sig, jasmine.any(String), '/');
        });

        it('should not set session cookies if data is not passed', function() {
            Mozilla.StubAttribution.setCookie({});
            expect(Mozilla.Cookies.setItem).not.toHaveBeenCalled();
        });
    });

    describe('hasCookie', function() {

        it('should return true if both session cookies exists', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            var result = Mozilla.StubAttribution.hasCookie();
            expect(Mozilla.Cookies.hasItem.calls.count()).toEqual(2);
            expect(Mozilla.Cookies.hasItem).toHaveBeenCalledWith(Mozilla.StubAttribution.COOKIE_CODE_ID);
            expect(Mozilla.Cookies.hasItem).toHaveBeenCalledWith(Mozilla.StubAttribution.COOKIE_SIGNATURE_ID);
            expect(result).toBeTruthy();
        });

        it('should return false if one or more session cookies do not exist', function() {
            spyOn(Mozilla.Cookies, 'hasItem').and.callFake(function(id) {
                return id === Mozilla.StubAttribution.COOKIE_CODE_ID ? true : false;
            });
            var result = Mozilla.StubAttribution.hasCookie();
            expect(Mozilla.Cookies.hasItem.calls.count()).toEqual(2);
            expect(result).toBeFalsy();
        });
    });

    describe('getAttributionRate', function() {

        var html = document.documentElement;
        var attr = 'data-stub-attribution-rate';

        afterEach(function() {
            html.removeAttribute(attr);
        });

        it('should return the stub attribution rate as expected', function() {
            html.setAttribute(attr, '0.5');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(0.5);
        });

        it('should return 0 if data attribute is not present', function() {
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(0);
        });

        it('should not return negative values', function() {
            html.setAttribute(attr, '-0.5');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(0);
            html.setAttribute(attr, '-1');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(0);
        });

        it('should not return values greater than 1', function() {
            html.setAttribute(attr, '1.5');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(1);
            html.setAttribute(attr, '2');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(1);
        });

        it('should not return other values', function() {
            html.setAttribute(attr, 'foo');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(0);
        });
    });

    describe('withinAttributionRate', function() {

        beforeEach(function() {
            spyOn(Mozilla.StubAttribution, 'getAttributionRate').and.returnValue(0.5);
        });

        it('should return true if within sample rate', function() {
            spyOn(window.Math, 'random').and.returnValue(0.3);
            expect(Mozilla.StubAttribution.withinAttributionRate()).toBeTruthy();
        });

        it('should return false if exceeds sample rate', function() {
            spyOn(window.Math, 'random').and.returnValue(0.6);
            expect(Mozilla.StubAttribution.withinAttributionRate()).toBeFalsy();
        });
    });
});
