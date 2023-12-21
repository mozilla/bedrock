/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import SentryConsent from '../../../../media/js/base/sentry-consent.es6';

describe('sentry-consent.es6.js', function () {
    beforeEach(function () {
        window.Mozilla.gpcEnabled = sinon.stub().returns(false);
        window.Mozilla.dntEnabled = sinon.stub().returns(false);

        spyOn(SentryConsent, 'initClient');
    });

    afterEach(function () {
        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');

        window.removeEventListener(
            'mozConsentStatus',
            SentryConsent.handleConsent,
            false
        );

        delete window.Mozilla.gpcEnabled;
        delete window.Mozilla.dntEnabled;
    });

    describe('Global visitors', function () {
        it('should not load Sentry if DNT is enabled', function () {
            window.Mozilla.dntEnabled = sinon.stub().returns(true);

            SentryConsent.init();
            expect(SentryConsent.initClient).not.toHaveBeenCalled();
        });

        it('should not load Sentry if GPC is enabled', function () {
            window.Mozilla.gpcEnabled = sinon.stub().returns(true);

            SentryConsent.init();
            expect(SentryConsent.initClient).not.toHaveBeenCalled();
        });
    });

    describe('EU visitors (explicit consent required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');
        });

        it('should wait for a mozConsentStatus event before loading', function () {
            SentryConsent.init();
            expect(SentryConsent.initClient).not.toHaveBeenCalled();
        });

        it('should load Sentry if consent event accepts analytics', function () {
            SentryConsent.init();
            expect(SentryConsent.initClient).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: true,
                        preference: true
                    }
                })
            );

            expect(SentryConsent.initClient).toHaveBeenCalled();
        });

        it('should not load Sentry if consent event rejects analytics', function () {
            SentryConsent.init();
            expect(SentryConsent.initClient).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: false,
                        preference: false
                    }
                })
            );

            expect(SentryConsent.initClient).not.toHaveBeenCalled();
        });
    });

    describe('Non-EU visitors (explicit consent not required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');
        });

        it('should load Sentry by default', function () {
            SentryConsent.init();
            expect(SentryConsent.initClient).toHaveBeenCalled();
        });

        it('should not load Sentry if consent cookie rejects analytics', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            SentryConsent.init();
            expect(SentryConsent.initClient).not.toHaveBeenCalled();
        });
    });
});
