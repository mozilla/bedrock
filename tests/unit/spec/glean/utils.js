/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import Utils from '../../../../media/js/glean/utils.es6';

describe('utils.js', function () {
    afterEach(function () {
        Mozilla.Analytics.customReferrer = '';
    });

    describe('getUrl', function () {
        it('should return the a complete URL including query parameters', function () {
            const url1 = 'https://www.mozilla.org/en-US/';
            expect(Utils.getUrl(url1)).toEqual(url1);

            const url2 =
                'https://www.mozilla.org/en-US/firefox/new/?utm_source=test&utm_campaign=test';
            expect(Utils.getUrl(url2)).toEqual(url2);
        });

        it('should remove newsletter tokens from know URLs', function () {
            const url1 =
                'https://www.mozilla.org/en-US/newsletter/existing/a1a2a3a4-abc1-12ab-a123-12345a12345b/?utm_source=test&utm_campaign=test';
            expect(Utils.getUrl(url1)).toEqual(
                'https://www.mozilla.org/en-US/newsletter/existing/?utm_source=test&utm_campaign=test'
            );

            const url2 =
                'https://www.mozilla.org/en-US/newsletter/country/a1a2a3a4-abc1-12ab-a123-12345a12345b/?utm_source=test&utm_campaign=test';
            expect(Utils.getUrl(url2)).toEqual(
                'https://www.mozilla.org/en-US/newsletter/country/?utm_source=test&utm_campaign=test'
            );

            const url3 =
                'https://www.mozilla.org/en-US/newsletter/existing/?utm_source=test&utm_campaign=test';
            expect(Utils.getUrl(url3)).toEqual(url3);
        });
    });

    describe('getPathFromUrl', function () {
        it('should return the path from a page URL excluding locale', function () {
            expect(Utils.getPathFromUrl('/en-US/firefox/new/')).toEqual(
                '/firefox/new/'
            );
            expect(Utils.getPathFromUrl('/de/firefox/new/')).toEqual(
                '/firefox/new/'
            );
            expect(Utils.getPathFromUrl('/kab/firefox/new/')).toEqual(
                '/firefox/new/'
            );
            expect(Utils.getPathFromUrl('/fr/')).toEqual('/');
        });

        it('should return original path when there is no locale', function () {
            expect(Utils.getPathFromUrl('/locales/')).toEqual('/locales/');
        });

        it('should exclude tokens from newsletter URLS', function () {
            expect(
                Utils.getPathFromUrl(
                    '/en-US/newsletter/existing/a1a2a3a4-abc1-12ab-a123-12345a12345b/'
                )
            ).toEqual('/newsletter/existing/');

            expect(
                Utils.getPathFromUrl(
                    '/en-US/newsletter/country/a1a2a3a4-abc1-12ab-a123-12345a12345b/'
                )
            ).toEqual('/newsletter/country/');
        });
    });

    describe('getLocaleFromUrl', function () {
        it('should return the locale from a page URL excluding path', function () {
            expect(Utils.getLocaleFromUrl('/en-US/firefox/new/')).toEqual(
                'en-US'
            );
            expect(Utils.getLocaleFromUrl('/de/firefox/new/')).toEqual('de');
            expect(Utils.getLocaleFromUrl('/kab/firefox/new/')).toEqual('kab');
            expect(Utils.getLocaleFromUrl('/fr/')).toEqual('fr');
        });

        it('should return `en-US` for language when there is no locale', function () {
            expect(Utils.getLocaleFromUrl('/locales/')).toEqual('en-US');
        });
    });

    describe('getQueryParamsFromUrl', function () {
        it('should return an object made up of params from a query string', function () {
            const query =
                'utm_source=test-source&utm_campaign=test-campaign&utm_medium=test-medium&utm_content=test-content&entrypoint_experiment=test_entrypoint_experiment&entrypoint_variation=1&experiment=test-experiment&variation=1&v=1&xv=test-xv';

            expect(Utils.getQueryParamsFromUrl(query).params).toEqual({
                utm_source: 'test-source',
                utm_campaign: 'test-campaign',
                utm_medium: 'test-medium',
                utm_content: 'test-content',
                entrypoint_experiment: 'test_entrypoint_experiment',
                entrypoint_variation: 1,
                experiment: 'test-experiment',
                variation: 1,
                v: 1,
                xv: 'test-xv'
            });
        });
    });

    describe('getReferrer', function () {
        afterEach(function () {
            Mozilla.Analytics.customReferrer = '';
        });

        it('should return a custom referrer when set', function () {
            const expected = 'http://www.google.com/';
            Mozilla.Analytics.customReferrer = expected;
            expect(Utils.getReferrer()).toEqual(expected);
        });

        it('should return regular referrer otherwise', function () {
            const expected = 'http://www.bing.com/';
            expect(Utils.getReferrer(expected)).toEqual(expected);
        });

        it('should strip newsletter tokens from referrer URLs', function () {
            const expected =
                'https://www.mozilla.org/en-US/newsletter/country/a1a2a3a4-abc1-12ab-a123-12345a12345b/?utm_source=test&utm_campaign=test';
            expect(Utils.getReferrer(expected)).toEqual(
                'https://www.mozilla.org/en-US/newsletter/country/?utm_source=test&utm_campaign=test'
            );
        });
    });

    describe('getHttpStatus', function () {
        afterEach(function () {
            document
                .getElementsByTagName('html')[0]
                .removeAttribute('data-http-status');
        });

        it('should return 200 by default', function () {
            expect(Utils.getHttpStatus()).toEqual('200');
        });

        it('should return 404 if matching data-http-status attribute is present in the page', function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-http-status', '404');
            expect(Utils.getHttpStatus()).toEqual('404');
        });
    });

    describe('isTelemetryEnabled', function () {
        it('should return true if opt out cookie does not exist', function () {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(false);
            const result = Utils.isTelemetryEnabled();
            expect(Mozilla.Cookies.hasItem).toHaveBeenCalledWith(
                'moz-1st-party-data-opt-out'
            );
            expect(result).toBeTrue();
        });

        it('should return false if opt out cookie exists', function () {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            const result = Utils.isTelemetryEnabled();
            expect(Mozilla.Cookies.hasItem).toHaveBeenCalledWith(
                'moz-1st-party-data-opt-out'
            );
            expect(result).toBeFalse();
        });
    });
});
