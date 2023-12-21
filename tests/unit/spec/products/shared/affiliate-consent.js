/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import AffiliateConsent from '../../../../../media/js/products/shared/affiliate-consent.es6';

describe('affiliate-consent.es6.js', function () {
    afterEach(function () {
        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');

        window.removeEventListener(
            'mozConsentStatus',
            AffiliateConsent.handleConsent,
            false
        );
    });

    describe('EU visitors (explicit consent required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');

            spyOn(AffiliateConsent, 'initAffiliateFlow');
        });

        it('should wait for a mozConsentStatus event before initializing attribution', function () {
            AffiliateConsent.init();
            expect(AffiliateConsent.initAffiliateFlow).not.toHaveBeenCalled();
        });

        it('should initialize attribution if consent event accepts analytics', function () {
            AffiliateConsent.init();
            expect(AffiliateConsent.initAffiliateFlow).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: true,
                        preference: true
                    }
                })
            );

            expect(AffiliateConsent.initAffiliateFlow).toHaveBeenCalled();
        });

        it('should not initialize attribution if consent event rejects analytics', function () {
            AffiliateConsent.init();
            expect(AffiliateConsent.initAffiliateFlow).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: false,
                        preference: false
                    }
                })
            );

            expect(AffiliateConsent.initAffiliateFlow).not.toHaveBeenCalled();
        });
    });

    describe('Non-EU visitors (explicit consent not required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');

            spyOn(AffiliateConsent, 'initAffiliateFlow');

            window.Mozilla.gpcEnabled = sinon.stub().returns(false);
            window.Mozilla.dntEnabled = sinon.stub().returns(false);
        });

        afterEach(function () {
            delete window.Mozilla.gpcEnabled;
            delete window.Mozilla.dntEnabled;
        });

        it('should initialize attribution if consent cookie accepts analytics', function () {
            AffiliateConsent.init();
            expect(AffiliateConsent.initAffiliateFlow).toHaveBeenCalled();
        });

        it('should not initialize attribution if consent cookie rejects analytics', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            AffiliateConsent.init();
            expect(AffiliateConsent.initAffiliateFlow).not.toHaveBeenCalled();
        });

        it('should initialize attribution if consent cookie accepts analytics', function () {
            const obj = {
                analytics: true,
                preference: true
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            AffiliateConsent.init();
            expect(AffiliateConsent.initAffiliateFlow).toHaveBeenCalled();
        });

        it('should only initialize FxA flow params if DNT is enabled', function () {
            window.Mozilla.dntEnabled = sinon.stub().returns(true);
            spyOn(AffiliateConsent, 'initFlowParams');
            AffiliateConsent.init();
            expect(AffiliateConsent.initFlowParams).toHaveBeenCalled();
            expect(AffiliateConsent.initAffiliateFlow).not.toHaveBeenCalled();
        });

        it('should only initialize FxA flow params if GPC is enabled', function () {
            window.Mozilla.gpcEnabled = sinon.stub().returns(true);
            spyOn(AffiliateConsent, 'initFlowParams');
            AffiliateConsent.init();
            expect(AffiliateConsent.initFlowParams).toHaveBeenCalled();
            expect(AffiliateConsent.initAffiliateFlow).not.toHaveBeenCalled();
        });
    });
});
