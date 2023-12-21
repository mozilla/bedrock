/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import GTMSnippet from '../../../../../media/js/base/gtm/gtm-snippet.es6';

describe('gtm-snippet.es6.js', function () {
    beforeEach(function () {
        window.Mozilla.gpcEnabled = sinon.stub().returns(false);
        window.Mozilla.dntEnabled = sinon.stub().returns(false);

        spyOn(GTMSnippet, 'loadSnippet');
    });

    afterEach(function () {
        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');

        window.removeEventListener(
            'mozConsentStatus',
            GTMSnippet.handleConsent,
            false
        );

        delete window.Mozilla.gpcEnabled;
        delete window.Mozilla.dntEnabled;
    });

    describe('Global visitors', function () {
        it('should not load GTM if DNT is enabled', function () {
            window.Mozilla.dntEnabled = sinon.stub().returns(true);

            GTMSnippet.init();
            expect(GTMSnippet.loadSnippet).not.toHaveBeenCalled();
        });

        it('should not load GTM if GPC is enabled', function () {
            window.Mozilla.gpcEnabled = sinon.stub().returns(true);

            GTMSnippet.init();
            expect(GTMSnippet.loadSnippet).not.toHaveBeenCalled();
        });
    });

    describe('EU visitors (explicit consent required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');
        });

        it('should wait for a mozConsentStatus event before loading', function () {
            GTMSnippet.init();
            expect(GTMSnippet.loadSnippet).not.toHaveBeenCalled();
        });

        it('should load GTM if consent event accepts analytics', function () {
            GTMSnippet.init();
            expect(GTMSnippet.loadSnippet).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: true,
                        preference: true
                    }
                })
            );

            expect(GTMSnippet.loadSnippet).toHaveBeenCalled();
        });

        it('should not load GTM if consent event rejects analytics', function () {
            GTMSnippet.init();
            expect(GTMSnippet.loadSnippet).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: false,
                        preference: false
                    }
                })
            );

            expect(GTMSnippet.loadSnippet).not.toHaveBeenCalled();
        });

        it('should load GTM on /thanks/ if a consent cookie exists that accepts analytics', function () {
            const obj = {
                analytics: true,
                preference: false
            };
            spyOn(GTMSnippet, 'isFirefoxDownloadThanks').and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            GTMSnippet.init();
            expect(GTMSnippet.loadSnippet).toHaveBeenCalled();
        });

        it('should not load GTM on /thanks/ if a consent cookie exists that rejects analytics', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(GTMSnippet, 'isFirefoxDownloadThanks').and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            GTMSnippet.init();
            expect(GTMSnippet.loadSnippet).not.toHaveBeenCalled();
        });

        it('should not load GTM if a consent cookie exists but URL is not /thanks/', function () {
            const obj = {
                analytics: true,
                preference: false
            };
            spyOn(GTMSnippet, 'isFirefoxDownloadThanks').and.returnValue(false);
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            GTMSnippet.init();
            expect(GTMSnippet.loadSnippet).not.toHaveBeenCalled();
        });
    });

    describe('Non-EU visitors (explicit consent not required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');
        });

        it('should load GTM by default', function () {
            GTMSnippet.init();
            expect(GTMSnippet.loadSnippet).toHaveBeenCalled();
        });

        it('should not load GTM if consent cookie rejects analytics', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            GTMSnippet.init();
            expect(GTMSnippet.loadSnippet).not.toHaveBeenCalled();
        });
    });
});
