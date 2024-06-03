/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import StubAttributionConsent from '../../../../../media/js/base/stub-attribution/stub-attribution-consent.es6';

describe('consent.es6.js', function () {
    beforeEach(function () {
        window.Mozilla.gpcEnabled = sinon.stub().returns(false);
        window.Mozilla.dntEnabled = sinon.stub().returns(false);

        spyOn(window.Mozilla.StubAttribution, 'init');
    });

    afterEach(function () {
        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');

        window.removeEventListener(
            'mozConsentStatus',
            StubAttributionConsent.handleConsent,
            false
        );

        delete window.Mozilla.gpcEnabled;
        delete window.Mozilla.dntEnabled;
    });

    describe('Global visitors', function () {
        it('should not load GTM if DNT is enabled', function () {
            window.Mozilla.dntEnabled = sinon.stub().returns(true);

            StubAttributionConsent.init();
            expect(window.Mozilla.StubAttribution.init).not.toHaveBeenCalled();
        });

        it('should not load GTM if GPC is enabled', function () {
            window.Mozilla.gpcEnabled = sinon.stub().returns(true);

            StubAttributionConsent.init();
            expect(window.Mozilla.StubAttribution.init).not.toHaveBeenCalled();
        });
    });

    describe('EU visitors (explicit consent required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');
        });

        it('should initialize attribution on /thanks/ if a consent cookie exists that accepts analytics', function () {
            const obj = {
                analytics: true,
                preference: false
            };
            spyOn(
                window.Mozilla.StubAttribution,
                'isFirefoxDownloadThanks'
            ).and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            StubAttributionConsent.init();
            expect(window.Mozilla.StubAttribution.init).toHaveBeenCalled();
        });

        it('should not initialize attribution on /thanks/ if a consent cookie exists that rejects analytics', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(
                window.Mozilla.StubAttribution,
                'isFirefoxDownloadThanks'
            ).and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            StubAttributionConsent.init();
            expect(window.Mozilla.StubAttribution.init).not.toHaveBeenCalled();
        });

        it('should not initialize attribution if a consent cookie exists but URL is not /thanks/', function () {
            const obj = {
                analytics: true,
                preference: false
            };
            spyOn(
                window.Mozilla.StubAttribution,
                'isFirefoxDownloadThanks'
            ).and.returnValue(false);
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            StubAttributionConsent.init();
            expect(window.Mozilla.StubAttribution.init).not.toHaveBeenCalled();
        });

        it('should initialize attribution if consent event accepts analytics', function () {
            StubAttributionConsent.init();
            expect(window.Mozilla.StubAttribution.init).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: true,
                        preference: true
                    }
                })
            );

            expect(window.Mozilla.StubAttribution.init).toHaveBeenCalled();
        });

        it('should not initialize attribution if consent event rejects analytics', function () {
            StubAttributionConsent.init();
            expect(window.Mozilla.StubAttribution.init).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: false,
                        preference: false
                    }
                })
            );

            expect(window.Mozilla.StubAttribution.init).not.toHaveBeenCalled();
        });
    });

    describe('Non-EU visitors (explicit consent not required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');
        });

        it('should initialize attribution by default', function () {
            StubAttributionConsent.init();
            expect(window.Mozilla.StubAttribution.init).toHaveBeenCalled();
        });

        it('should not initialize attribution if consent cookie rejects analytics', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            StubAttributionConsent.init();
            expect(window.Mozilla.StubAttribution.init).not.toHaveBeenCalled();
        });
    });
});
