/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import StripeConsent from '../../../../../media/js/products/shared/stripe-consent.es6';

describe('stripe-consent.es6.js', function () {
    afterEach(function () {
        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');

        window.removeEventListener(
            'mozConsentStatus',
            StripeConsent.handleConsent,
            false
        );
    });

    describe('EU visitors (explicit consent required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');

            spyOn(StripeConsent, 'loadStripeJS');
        });

        it('should wait for a mozConsentStatus event before loading Stripe JS', function () {
            StripeConsent.init();
            expect(StripeConsent.loadStripeJS).not.toHaveBeenCalled();
        });

        it('should load Stripe JS if consent event accepts analytics', function () {
            StripeConsent.init();
            expect(StripeConsent.loadStripeJS).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: true,
                        preference: true
                    }
                })
            );

            expect(StripeConsent.loadStripeJS).toHaveBeenCalled();
        });

        it('should not load Stripe JS if consent event rejects analytics', function () {
            StripeConsent.init();
            expect(StripeConsent.loadStripeJS).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: false,
                        preference: false
                    }
                })
            );

            expect(StripeConsent.loadStripeJS).not.toHaveBeenCalled();
        });
    });

    describe('Non-EU visitors (explicit consent not required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');

            spyOn(StripeConsent, 'loadStripeJS');
        });

        it('should load Stripe JS if consent cookie accepts analytics', function () {
            StripeConsent.init();
            expect(StripeConsent.loadStripeJS).toHaveBeenCalled();
        });

        it('should not load Stripe JS if consent cookie rejects analytics', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            StripeConsent.init();
            expect(StripeConsent.loadStripeJS).not.toHaveBeenCalled();
        });

        it('should load Stripe JS if consent cookie accepts analytics', function () {
            const obj = {
                analytics: true,
                preference: true
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            StripeConsent.init();
            expect(StripeConsent.loadStripeJS).toHaveBeenCalled();
        });
    });
});
