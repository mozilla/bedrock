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
    describe('filterURL', function () {
        it('should return the a complete URL including query parameters', function () {
            const url1 = 'https://www.mozilla.org/en-US/';
            expect(Utils.filterURL(url1)).toEqual(url1);

            const url2 =
                'https://www.mozilla.org/en-US/firefox/new/?utm_source=test&utm_campaign=test';
            expect(Utils.filterURL(url2)).toEqual(url2);
        });

        it('should remove newsletter tokens from know URLs', function () {
            const url1 =
                'https://www.mozilla.org/en-US/newsletter/existing/a1a2a3a4-abc1-12ab-a123-12345a12345b/?utm_source=test&utm_campaign=test';
            expect(Utils.filterURL(url1)).toEqual(
                'https://www.mozilla.org/en-US/newsletter/existing/?utm_source=test&utm_campaign=test'
            );

            const url2 =
                'https://www.mozilla.org/en-US/newsletter/country/a1a2a3a4-abc1-12ab-a123-12345a12345b/?utm_source=test&utm_campaign=test';
            expect(Utils.filterURL(url2)).toEqual(
                'https://www.mozilla.org/en-US/newsletter/country/?utm_source=test&utm_campaign=test'
            );

            const url3 =
                'https://www.mozilla.org/en-US/newsletter/existing/?utm_source=test&utm_campaign=test';
            expect(Utils.filterURL(url3)).toEqual(url3);
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
                spyOn(Utils, 'initHelpers');
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
                expect(Utils.initHelpers).toHaveBeenCalled();
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
                expect(Utils.initHelpers).not.toHaveBeenCalled();
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
                expect(Utils.initHelpers).toHaveBeenCalled();
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
                expect(Utils.initHelpers).not.toHaveBeenCalled();
            });
        });

        describe('Non-EU visitors (explicit consent not required)', function () {
            beforeEach(function () {
                document
                    .getElementsByTagName('html')[0]
                    .setAttribute('data-needs-consent', 'False');

                spyOn(Utils, 'initGlean');
                spyOn(Utils, 'initPageLoadEvent');
                spyOn(Utils, 'initHelpers');
            });

            it('should init Glean and fire page load by default', function () {
                Utils.bootstrapGlean();
                expect(Utils.initGlean).toHaveBeenCalled();
                expect(Utils.initPageLoadEvent).toHaveBeenCalled();
                expect(Utils.initHelpers).toHaveBeenCalled();
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
                expect(Utils.initHelpers).not.toHaveBeenCalled();
            });
        });
    });
});
