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

    describe('GTMSnippet.setGtagConsentDefaults()', function () {
        beforeEach(function () {
            window.gtag = jasmine.createSpy('gtag');
        });

        afterEach(function () {
            delete window.gtag;
            document
                .getElementsByTagName('html')[0]
                .removeAttribute('data-needs-consent');
        });

        it('should set granted defaults when consent cookie accepts analytics', function () {
            const obj = { analytics: true, preference: true };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            GTMSnippet.setGtagConsentDefaults();
            expect(window.gtag).toHaveBeenCalledWith('consent', 'default', {
                ad_user_data: 'granted',
                ad_personalization: 'granted',
                ad_storage: 'granted'
            });
            expect(window.gtag).toHaveBeenCalledWith('consent', 'default', {
                analytics_storage: 'granted'
            });
        });

        it('should set denied defaults when consent cookie rejects analytics', function () {
            const obj = { analytics: false, preference: false };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            GTMSnippet.setGtagConsentDefaults();
            expect(window.gtag).toHaveBeenCalledWith('consent', 'default', {
                ad_user_data: 'denied',
                ad_personalization: 'denied',
                ad_storage: 'denied'
            });
            expect(window.gtag).toHaveBeenCalledWith('consent', 'default', {
                analytics_storage: 'denied'
            });
        });

        it('should deny ads and grant analytics defaults when no cookie and visitor is outside EU/EAA', function () {
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(false);
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');
            GTMSnippet.setGtagConsentDefaults();
            expect(window.gtag).toHaveBeenCalledWith('consent', 'default', {
                ad_user_data: 'denied',
                ad_personalization: 'denied',
                ad_storage: 'denied'
            });
            expect(window.gtag).toHaveBeenCalledWith('consent', 'default', {
                analytics_storage: 'granted'
            });
        });

        it('should deny all defaults when no cookie and visitor is in EU/EAA', function () {
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(false);
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');
            GTMSnippet.setGtagConsentDefaults();
            expect(window.gtag).toHaveBeenCalledWith('consent', 'default', {
                ad_user_data: 'denied',
                ad_personalization: 'denied',
                ad_storage: 'denied'
            });
            expect(window.gtag).toHaveBeenCalledWith('consent', 'default', {
                analytics_storage: 'denied'
            });
        });
    });

    describe('GTMSnippet.handleConsent()', function () {
        beforeEach(function () {
            window.gtag = jasmine.createSpy('gtag');
        });

        afterEach(function () {
            delete window.gtag;
        });

        it('should call gtag consent update when analytics are accepted', function () {
            GTMSnippet.handleConsent({
                detail: { analytics: true, preference: true }
            });
            expect(window.gtag).toHaveBeenCalledWith('consent', 'update', {
                ad_user_data: 'granted',
                ad_personalization: 'granted',
                ad_storage: 'granted'
            });
            expect(window.gtag).toHaveBeenCalledWith('consent', 'update', {
                analytics_storage: 'granted'
            });
        });

        it('should call gtag consent update when analytics are rejected', function () {
            GTMSnippet.handleConsent({
                detail: { analytics: false, preference: false }
            });
            expect(window.gtag).toHaveBeenCalledWith('consent', 'update', {
                ad_user_data: 'denied',
                ad_personalization: 'denied',
                ad_storage: 'denied'
            });
            expect(window.gtag).toHaveBeenCalledWith('consent', 'update', {
                analytics_storage: 'denied'
            });
        });
    });
});
