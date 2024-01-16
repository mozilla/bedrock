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
});
