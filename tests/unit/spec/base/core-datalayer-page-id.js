/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('core-datalayer-page-id.js', function () {
    describe('getPageId', function () {
        const html = document.documentElement;

        afterEach(function () {
            html.removeAttribute('data-gtm-page-id');
        });

        it('will grab data-gtm-page-id value if present on <html> element', function () {
            html.setAttribute('data-gtm-page-id', 'test');
            expect(Mozilla.Analytics.getPageId('/en-US/firefox/new/')).toBe(
                'test'
            );
        });

        it('will grab the pathname minus the first directory if no data-gtm-page-id value is present on <html> element', function () {
            expect(Mozilla.Analytics.getPageId('/en-US/firefox/new/')).toBe(
                '/firefox/new/'
            );
        });

        it('will return the full page path when no data-gtm-page-id value is present and no locale is in page path', function () {
            expect(Mozilla.Analytics.getPageId('/firefox/new/')).toBe(
                '/firefox/new/'
            );
        });
    });

    describe('getTrafficCopReferrer', function () {
        it('should return null if the referrer does not exist', function () {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(false);
            expect(Mozilla.Analytics.getTrafficCopReferrer()).toBe(undefined);
        });

        it('should return the referrer if one exists', function () {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            spyOn(Mozilla.Cookies, 'getItem').and.returnValue('direct');
            expect(Mozilla.Analytics.getTrafficCopReferrer()).toBe('direct');
        });
    });

    describe('buildDataObject', function () {
        it('should contain customReferrer if found in cookie', function () {
            spyOn(Mozilla.Analytics, 'getTrafficCopReferrer').and.returnValue(
                'http://www.google.com'
            );
            const obj = Mozilla.Analytics.buildDataObject();
            expect(obj.customReferrer).toBeDefined();
        });

        it('should not contain customReferrer if not found in cookie', function () {
            spyOn(Mozilla.Analytics, 'getTrafficCopReferrer').and.returnValue(
                undefined
            );
            const obj = Mozilla.Analytics.buildDataObject();
            expect(obj.customReferrer).not.toBeDefined();
        });
    });
});
