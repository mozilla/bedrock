/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import FxaFormConsent from '../../../../media/js/base/fxa-form-consent.es6.js';

describe('fxa-form-consent.es6.js', function () {
    beforeEach(function () {
        spyOn(FxaFormConsent, 'initEssential');
    });

    afterEach(function () {
        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');

        window.removeEventListener(
            'mozConsentStatus',
            FxaFormConsent.handleConsent,
            false
        );
    });

    describe('Global visitors', function () {
        it('should initialize Sync for Firefox desktop browsers', function () {
            FxaFormConsent.init();
            expect(FxaFormConsent.initEssential).toHaveBeenCalled();
        });
    });

    describe('EU visitors (explicit consent required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');

            spyOn(FxaFormConsent, 'initForm');
        });

        it('should wait for a mozConsentStatus event before initializing attribution', function () {
            FxaFormConsent.init();
            expect(FxaFormConsent.initForm).not.toHaveBeenCalled();
        });

        it('should initialize attribution if consent event accepts analytics', function () {
            FxaFormConsent.init();
            expect(FxaFormConsent.initForm).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: true,
                        preference: true
                    }
                })
            );

            expect(FxaFormConsent.initForm).toHaveBeenCalledWith(true);
        });

        it('should not initialize attribution if consent event rejects analytics', function () {
            FxaFormConsent.init();
            expect(FxaFormConsent.initForm).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: false,
                        preference: false
                    }
                })
            );

            expect(FxaFormConsent.initForm).toHaveBeenCalledWith(false);
        });
    });

    describe('Non-EU visitors (explicit consent not required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');

            spyOn(FxaFormConsent, 'initForm');
        });

        it('should initialize attribution by default', function () {
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(false);
            FxaFormConsent.init();
            expect(FxaFormConsent.initForm).toHaveBeenCalledWith(true);
        });

        it('should not initialize attribution if consent cookie rejects analytics', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            FxaFormConsent.init();
            expect(FxaFormConsent.initForm).toHaveBeenCalledWith(false);
        });

        it('should initialize attribution if consent cookie accepts analytics', function () {
            const obj = {
                analytics: true,
                preference: true
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            FxaFormConsent.init();
            expect(FxaFormConsent.initForm).toHaveBeenCalledWith(true);
        });
    });
});
