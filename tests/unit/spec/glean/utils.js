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
        it('should return regular referrer', function () {
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

    describe('bootstrapGlean', function () {
        afterEach(function () {
            document
                .getElementsByTagName('html')[0]
                .removeAttribute('data-needs-consent');

            window.removeEventListener(
                'mozConsentStatus',
                Utils.handleConsent,
                false
            );
        });

        describe('EU visitors (explicit consent required)', function () {
            beforeEach(function () {
                document
                    .getElementsByTagName('html')[0]
                    .setAttribute('data-needs-consent', 'True');

                spyOn(Utils, 'initGlean');
                spyOn(Utils, 'initPageLoadEvent');
            });

            it('should return wait for a mozConsentStatus event before initializing Glean', function () {
                Utils.bootstrapGlean();
                expect(Utils.initGlean).not.toHaveBeenCalled();
            });

            it('should init Glean and fire page load if mozConsentStatus event accepts analytics', function () {
                Utils.bootstrapGlean();
                expect(Utils.initGlean).not.toHaveBeenCalled();

                window.dispatchEvent(
                    new CustomEvent('mozConsentStatus', {
                        detail: {
                            analytics: true,
                            preference: true
                        }
                    })
                );

                expect(Utils.initGlean).toHaveBeenCalledWith(true);
                expect(Utils.initPageLoadEvent).toHaveBeenCalled();
            });

            it('should init Glean to send a deletion request if mozConsentStatus event rejects analytics', function () {
                Utils.bootstrapGlean();
                expect(Utils.initGlean).not.toHaveBeenCalled();

                window.dispatchEvent(
                    new CustomEvent('mozConsentStatus', {
                        detail: {
                            analytics: false,
                            preference: false
                        }
                    })
                );

                expect(Utils.initGlean).toHaveBeenCalledWith(false);
                expect(Utils.initPageLoadEvent).not.toHaveBeenCalled();
            });

            it('should load Glean on /thanks/ if a consent cookie exists that accepts analytics', function () {
                const obj = {
                    analytics: true,
                    preference: false
                };

                spyOn(Utils, 'isFirefoxDownloadThanks').and.returnValue(true);
                spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                    JSON.stringify(obj)
                );

                Utils.bootstrapGlean();

                expect(Utils.initGlean).toHaveBeenCalledWith(true);
                expect(Utils.initPageLoadEvent).toHaveBeenCalled();
            });

            it('should not load GTM on /thanks/ if a consent cookie exists that rejects analytics', function () {
                const obj = {
                    analytics: false,
                    preference: false
                };
                spyOn(Utils, 'isFirefoxDownloadThanks').and.returnValue(true);
                spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                    JSON.stringify(obj)
                );

                Utils.bootstrapGlean();

                expect(Utils.initGlean).not.toHaveBeenCalled();
                expect(Utils.initPageLoadEvent).not.toHaveBeenCalled();
            });

            it('should not load GTM if a consent cookie exists but URL is not /thanks/', function () {
                const obj = {
                    analytics: true,
                    preference: false
                };
                spyOn(Utils, 'isFirefoxDownloadThanks').and.returnValue(false);
                spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                    JSON.stringify(obj)
                );

                Utils.bootstrapGlean();

                expect(Utils.initGlean).not.toHaveBeenCalled();
                expect(Utils.initPageLoadEvent).not.toHaveBeenCalled();
            });
        });

        describe('Non-EU visitors (explicit consent not required)', function () {
            beforeEach(function () {
                document
                    .getElementsByTagName('html')[0]
                    .setAttribute('data-needs-consent', 'False');

                spyOn(Utils, 'initGlean');
                spyOn(Utils, 'initPageLoadEvent');
            });

            it('should init Glean and fire page load by default', function () {
                Utils.bootstrapGlean();
                expect(Utils.initGlean).toHaveBeenCalled();
                expect(Utils.initPageLoadEvent).toHaveBeenCalled();
            });

            it('should init Glean to send a deletion request if consent cookie rejects analytics', function () {
                const obj = {
                    analytics: false,
                    preference: false
                };
                spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                    JSON.stringify(obj)
                );

                Utils.bootstrapGlean();
                expect(Utils.initGlean).toHaveBeenCalledWith(false);
                expect(Utils.initPageLoadEvent).not.toHaveBeenCalled();
            });
        });
    });
});
