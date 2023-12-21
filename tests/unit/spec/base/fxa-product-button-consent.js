/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import FxaProductButtonConsent from '../../../../media/js/base/fxa-product-button-consent.es6.js';

describe('fxa-product-button-consent.es6.js', function () {
    beforeEach(function () {
        spyOn(FxaProductButtonConsent, 'initMetricsFlow');
    });

    afterEach(function () {
        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');

        window.removeEventListener(
            'mozConsentStatus',
            FxaProductButtonConsent.handleConsent,
            false
        );
    });

    describe('EU visitors (explicit consent required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');
        });

        it('should wait for a mozConsentStatus event before initializing attribution', function () {
            FxaProductButtonConsent.init();
            expect(
                FxaProductButtonConsent.initMetricsFlow
            ).not.toHaveBeenCalled();
        });

        it('should initialize attribution if consent event accepts analytics', function () {
            FxaProductButtonConsent.init();
            expect(
                FxaProductButtonConsent.initMetricsFlow
            ).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: true,
                        preference: true
                    }
                })
            );

            expect(FxaProductButtonConsent.initMetricsFlow).toHaveBeenCalled();
        });

        it('should not initialize attribution if consent event rejects analytics', function () {
            FxaProductButtonConsent.init();
            expect(
                FxaProductButtonConsent.initMetricsFlow
            ).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: false,
                        preference: false
                    }
                })
            );

            expect(
                FxaProductButtonConsent.initMetricsFlow
            ).not.toHaveBeenCalled();
        });
    });

    describe('Non-EU visitors (explicit consent not required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');
        });

        it('should initialize attribution by default', function () {
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(false);
            FxaProductButtonConsent.init();
            expect(FxaProductButtonConsent.initMetricsFlow).toHaveBeenCalled();
        });

        it('should not initialize attribution if consent cookie rejects analytics', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            FxaProductButtonConsent.init();
            expect(
                FxaProductButtonConsent.initMetricsFlow
            ).not.toHaveBeenCalled();
        });

        it('should initialize attribution if consent cookie accepts analytics', function () {
            const obj = {
                analytics: true,
                preference: true
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            FxaProductButtonConsent.init();
            expect(FxaProductButtonConsent.initMetricsFlow).toHaveBeenCalled();
        });
    });
});
