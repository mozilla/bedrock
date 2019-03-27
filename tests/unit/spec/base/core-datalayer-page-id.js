/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon */

describe('core-datalayer-page-id.js', function() {
    'use strict';

    beforeEach(function() {
        // stub out Mozilla.Cookie lib
        window.Mozilla.Cookies = sinon.stub();
        window.Mozilla.Cookies.hasItem = sinon.stub();
        window.Mozilla.Cookies.getItem = sinon.stub();
        window.Mozilla.Cookies.removeItem = sinon.stub();
    });

    describe('getPageId', function(){
        var html = document.documentElement;

        afterEach(function() {
            html.removeAttribute('data-gtm-page-id');
        });

        it('will grab data-gtm-page-id value if present on <html> element', function(){
            html.setAttribute('data-gtm-page-id', 'test');

            expect(Mozilla.Analytics.getPageId('/en-US/firefox/new/')).toBe('test');
        });

        it('will grab the pathname minus the first directory if no data-gtm-page-id value is present on <html> element', function(){
            expect(Mozilla.Analytics.getPageId('/en-US/firefox/new/')).toBe('/firefox/new/');
        });

        it('will return the full page path when no data-gtm-page-id value is present and no locale is in page path', function(){
            expect(Mozilla.Analytics.getPageId('/firefox/new/')).toBe('/firefox/new/');
        });
    });

    describe('getTrafficCopReferrer', function(){
        it('should return null if the referrer does not exist', function(){
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(false);
            expect(Mozilla.Analytics.getTrafficCopReferrer()).toBe(undefined);
        });

        it('should return the referrer if one exists', function(){
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('direct');
            expect(Mozilla.Analytics.getTrafficCopReferrer()).toBe('direct');
        });
    });

    describe('buildDataObject', function(){
        it('should contain customReferrer if found in cookie', function(){
            spyOn(Mozilla.Analytics, 'getTrafficCopReferrer').and.returnValue('http://www.google.com');
            var obj = Mozilla.Analytics.buildDataObject();
            expect(obj.customReferrer).toBeDefined();
        });

        it('should not contain customReferrer if not found in cookie', function(){
            spyOn(Mozilla.Analytics, 'getTrafficCopReferrer').and.returnValue(undefined);
            var obj = Mozilla.Analytics.buildDataObject();
            expect(obj.customReferrer).not.toBeDefined();
        });
    });
});
