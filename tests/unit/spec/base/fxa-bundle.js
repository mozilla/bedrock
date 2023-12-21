/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import FxaBundleConsent from '../../../../media/js/base/fxa-bundle-consent.es6.js';

describe('fxa-bundle.es6.js', function () {
    afterEach(function () {
        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');

        window.removeEventListener(
            'mozConsentStatus',
            FxaBundleConsent.handleConsent,
            false
        );
    });

    describe('EU visitors (explicit consent required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');

            spyOn(FxaBundleConsent, 'initAttribution');
        });

        it('should wait for a mozConsentStatus event before initializing attribution', function () {
            FxaBundleConsent.init();
            expect(FxaBundleConsent.initAttribution).not.toHaveBeenCalled();
        });

        it('should initialize attribution if consent event accepts analytics', function () {
            FxaBundleConsent.init();
            expect(FxaBundleConsent.initAttribution).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: true,
                        preference: true
                    }
                })
            );

            expect(FxaBundleConsent.initAttribution).toHaveBeenCalled();
        });

        it('should not initialize attribution if consent event rejects analytics', function () {
            FxaBundleConsent.init();
            expect(FxaBundleConsent.initAttribution).not.toHaveBeenCalled();

            window.dispatchEvent(
                new CustomEvent('mozConsentStatus', {
                    detail: {
                        analytics: false,
                        preference: false
                    }
                })
            );

            expect(FxaBundleConsent.initAttribution).not.toHaveBeenCalled();
        });
    });

    describe('Non-EU visitors (explicit consent not required)', function () {
        beforeEach(function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');

            spyOn(FxaBundleConsent, 'initAttribution');
        });

        it('should initialize attribution by default', function () {
            FxaBundleConsent.init();
            expect(FxaBundleConsent.initAttribution).toHaveBeenCalled();
        });

        it('should not initialize attribution if consent cookie rejects analytics', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            FxaBundleConsent.init();
            expect(FxaBundleConsent.initAttribution).not.toHaveBeenCalled();
        });

        it('should initialize attribution if consent cookie accepts analytics', function () {
            const obj = {
                analytics: true,
                preference: true
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );
            FxaBundleConsent.init();
            expect(FxaBundleConsent.initAttribution).toHaveBeenCalled();
        });
    });
});
