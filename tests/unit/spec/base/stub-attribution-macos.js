/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect */
/* eslint new-cap: [2, {"capIsNewExceptions": ["Deferred"]}] */

describe('stub-attribution-macos.js', function () {

    'use strict';

    describe('init', function () {

        beforeEach(function () {
            spyOn(Mozilla.StubAttributionMacOS, 'updateTransitionalLinks');
        });

        it('should update download links if utm_* params exist', function () {
            var utmData = {
                campaing: 'thedude',
                source: 'abides'
            };

            spyOn(Mozilla.StubAttributionMacOS, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.StubAttributionMacOS, 'getAttributionData').and.returnValue(utmData);
            Mozilla.StubAttributionMacOS.init();
            expect(Mozilla.StubAttributionMacOS.updateTransitionalLinks).toHaveBeenCalledWith(utmData);
        });

        it('should do nothing if stub attribution requirements are not satisfied', function () {
            spyOn(Mozilla.StubAttributionMacOS, 'meetsRequirements').and.returnValue(false);
            Mozilla.StubAttributionMacOS.init();
            expect(Mozilla.StubAttributionMacOS.updateTransitionalLinks).not.toHaveBeenCalled();
        });
    });

    describe('meetsRequirements', function () {

        afterEach(function () {
            window.site.platform = 'other';
        });

        it('should return false if platform is not osx', function () {
            window.site.platform = 'windows';
            expect(Mozilla.StubAttributionMacOS.meetsRequirements()).toBeFalsy();
        });

        it('should return false if browser has DNT enabled', function () {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(true);
            expect(Mozilla.StubAttributionMacOS.meetsRequirements()).toBeFalsy();
        });

        it('should return true for osx/macOS users who satisfy all other requirements', function () {
            window.site.platform = 'osx';
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            expect(Mozilla.StubAttributionMacOS.meetsRequirements()).toBeTruthy();
        });
    });

    describe('getAttributionData', function () {

        var utms = {
            'utm_campaign': 'non-fx-button',
            'utm_medium': 'referral',
            'utm_source': 'addons.mozilla.org',
            'utm_content': 'rta%3Ae2JkZmNjZjM4LTBmMzgtNGM0YS04NzB_TM3NzA2-jFmYTZiOX0'
        };

        afterEach(function () {
            utms = {
                'utm_campaign': 'non-fx-button',
                'utm_medium': 'referral',
                'utm_source': 'addons.mozilla.org',
                'utm_content': 'rta%3Ae2JkZmNjZjM4LTBmMzgtNGM0YS04NzB_TM3NzA2-jFmYTZiOX0'
            };
        });

        it('should return a populated object if all utm_ params meet requirements', function () {
            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(utms);
            var data = Mozilla.StubAttributionMacOS.getAttributionData();
            expect(data).not.toBe(null);
            expect(data['campaign']).toEqual(utms['utm_campaign']);
            expect(data['medium']).toEqual(utms['utm_medium']);
            expect(data['source']).toEqual(utms['utm_source']);
            expect(data['content']).toEqual(decodeURIComponent(utms['utm_content']));
        });

        it('should return null if utm_campaign is missing', function () {
            delete (utms['utm_campaign']);

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(utms);
            var data = Mozilla.StubAttributionMacOS.getAttributionData();
            expect(data).toBe(null);
        });

        it('should return null if utm_campaign is invalid', function () {
            utms['utm_campaign'] = 'overtheline';

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(utms);
            var data = Mozilla.StubAttributionMacOS.getAttributionData();
            expect(data).toBe(null);
        });

        it('should return null if utm_medium is missing', function () {
            delete (utms['utm_medium']);

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(utms);
            var data = Mozilla.StubAttributionMacOS.getAttributionData();
            expect(data).toBe(null);
        });

        it('should return null if utm_medium is invalid', function () {
            utms['utm_medium'] = 'webelieveinnothing';

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(utms);
            var data = Mozilla.StubAttributionMacOS.getAttributionData();
            expect(data).toBe(null);
        });

        it('should return null if utm_source is missing', function () {
            delete (utms['utm_source']);

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(utms);
            var data = Mozilla.StubAttributionMacOS.getAttributionData();
            expect(data).toBe(null);
        });

        it('should return null if utm_source is invalid', function () {
            utms['utm_source'] = 'autobahn';

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(utms);
            var data = Mozilla.StubAttributionMacOS.getAttributionData();
            expect(data).toBe(null);
        });

        it('should return null if utm_content is missing', function () {
            delete (utms['utm_content']);

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(utms);
            var data = Mozilla.StubAttributionMacOS.getAttributionData();
            expect(data).toBe(null);
        });

        it('should return null if utm_content is invalid', function () {
            var data;
            utms['utm_content'] = 'thisstringismissingtheprefix';

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(utms);
            data = Mozilla.StubAttributionMacOS.getAttributionData();
            expect(data).toBe(null);

            utms['utm_content'] = 'rta%3Ai-have_some(invalid*characters>';
            data = Mozilla.StubAttributionMacOS.getAttributionData();
            expect(data).toBe(null);
        });
    });

    describe('updateTransitionalLinks', function () {

        var data = {
            campaign: 'thedude',
            source: 'abides'
        };

        var osxUrl = 'https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US';
        var transitionalUrl = '/firefox/download/thanks/';

        beforeEach(function () {
            var downloadMarkup = '<ul class="download-list">' +
                '<li><a class="download-link" data-download-version="osx" href="' + transitionalUrl + '">Download</a></li>' +
                '<li><a class="download-link" data-download-version="osx" href="' + osxUrl + '">Download</a></li>' +
                '</ul>';
            $(downloadMarkup).appendTo('body');
        });

        afterEach(function () {
            $('.download-list').remove();
        });

        it('should update download links with attribution data as expected', function () {
            spyOn(Mozilla.StubAttributionMacOS, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.StubAttributionMacOS, 'appendToDownloadURL');
            Mozilla.StubAttributionMacOS.updateTransitionalLinks(data);
            expect(Mozilla.StubAttributionMacOS.appendToDownloadURL.calls.count()).toEqual(1);
            var args = Mozilla.StubAttributionMacOS.appendToDownloadURL.calls.argsFor(0);
            // need to check args individually because host gets prepended to relative URLs
            expect(args[0]).toContain(transitionalUrl);
            expect(args[1]).toBe(data);
        });

        it('should do nothing if stub attribution requirements are not satisfied', function () {
            spyOn(Mozilla.StubAttributionMacOS, 'meetsRequirements').and.returnValue(false);
            spyOn(Mozilla.StubAttributionMacOS, 'appendToDownloadURL');
            Mozilla.StubAttributionMacOS.updateTransitionalLinks(data);
            expect(Mozilla.StubAttributionMacOS.appendToDownloadURL).not.toHaveBeenCalled();
        });

        it('should not update download URLs if attribution data is null', function () {
            spyOn(Mozilla.StubAttributionMacOS, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.StubAttributionMacOS, 'appendToDownloadURL');
            Mozilla.StubAttributionMacOS.updateTransitionalLinks(null);
            expect(Mozilla.StubAttributionMacOS.appendToDownloadURL).not.toHaveBeenCalled();
        });
    });

    describe('appendToDownloadURL', function () {

        var data = {
            campaign: 'thedude',
            source: 'abides'
        };

        it('should append params to a URL without a querystring', function () {
            var url = '/firefox/download/thanks/';
            var result = Mozilla.StubAttributionMacOS.appendToDownloadURL(url, data);
            expect(result).toContain(url + '?');
            expect(result).toContain('campaign=thedude');
            expect(result).toContain('source=abides');
        });

        it('should append params to a URL with a querystring and retain that querystring', function () {
            var url = '/firefox/download/thanks/?stranger=alps&near=theinnoutburger';
            var result = Mozilla.StubAttributionMacOS.appendToDownloadURL(url, data);
            expect(result).toContain('/firefox/download/thanks/?');
            expect(result).toContain('campaign=thedude');
            expect(result).toContain('source=abides');
            expect(result).toContain('stranger=alps');
            expect(result).toContain('near=theinnoutburger');
        });

        it('should favor values in the url over those attempting to be appended', function () {
            var url = '/firefox/download/thanks/?campaign=overtheline';
            var result = Mozilla.StubAttributionMacOS.appendToDownloadURL(url, data);
            expect(result).toContain('campaign=overtheline');
            expect(result).not.toContain('campaign=thedude');
        });
    });
});
