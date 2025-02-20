/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import MarketingOptOut from '../../../../../media/js/firefox/landing/get/marketing-opt-out.es6';

const labelSelector = '.marketing-opt-out-checkbox-label.hidden';
const checkboxSelector = '.marketing-opt-out-checkbox-input:checked';

describe('marketing-opt-out.es6.js', function () {
    beforeEach(function () {
        const optOut = `<div id="opt-out">
            <label for="marketing-opt-out-primary" class="marketing-opt-out-checkbox-label hidden">
                <input type="checkbox" id="marketing-opt-out-primary" class="marketing-opt-out-checkbox-input">.
            </label>
            <label for="marketing-opt-out-secondary" class="marketing-opt-out-checkbox-label hidden">
                <input type="checkbox" id="marketing-opt-out-secondary" class="marketing-opt-out-checkbox-input">.
            </label>
        </div>`;

        document.body.insertAdjacentHTML('beforeend', optOut);
    });

    afterEach(function () {
        const optOut = document.getElementById('opt-out');
        optOut.parentNode.removeChild(optOut);

        document
            .getElementsByTagName('html')[0]
            .removeAttribute('data-needs-consent');
    });

    describe('init()', function () {
        it('should return false if attribution requirements are not satisfied', function () {
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(false);

            const result = MarketingOptOut.init();
            expect(result).toBeFalse();

            const labels = document.querySelectorAll(labelSelector);
            expect(labels.length).toEqual(2);

            const checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(0);
        });

        it('should return false if GPC is enabled', function () {
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(true);
            window.Mozilla.gpcEnabled = sinon.stub().returns(true);

            const result = MarketingOptOut.init();
            expect(result).toBeFalse();
            delete window.Mozilla.gpcEnabled;

            const labels = document.querySelectorAll(labelSelector);
            expect(labels.length).toEqual(2);

            const checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(0);
        });

        it('should return false if DNT is enabled', function () {
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(true);
            window.Mozilla.dntEnabled = sinon.stub().returns(true);

            const result = MarketingOptOut.init();
            expect(result).toBeFalse();
            delete window.Mozilla.dntEnabled;

            const labels = document.querySelectorAll(labelSelector);
            expect(labels.length).toEqual(2);

            const checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(0);
        });

        it('should return true if attribution cookie exists', function () {
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'hasCookie').and.returnValue(
                true
            );

            const result = MarketingOptOut.init();
            expect(result).toBeTrue();

            const labels = document.querySelectorAll(labelSelector);
            expect(labels.length).toEqual(0);

            const checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(2);
        });

        it('should return true if consent cookie accepts analytics', function () {
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'hasCookie').and.returnValue(
                false
            );
            spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(true);

            const obj = {
                analytics: true,
                preference: true
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            const result = MarketingOptOut.init();
            expect(result).toBeTrue();

            const labels = document.querySelectorAll(labelSelector);
            expect(labels.length).toEqual(0);

            const checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(2);
        });

        it('should return false if consent cookie rejects analytics', function () {
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'hasCookie').and.returnValue(
                false
            );
            spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(true);

            const obj = {
                analytics: false,
                preference: true
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            const result = MarketingOptOut.init();
            expect(result).toBeFalse();

            const labels = document.querySelectorAll(labelSelector);
            expect(labels.length).toEqual(2);

            const checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(0);
        });

        it('should return false if visitor is in EU/EAA country', function () {
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'hasCookie').and.returnValue(
                false
            );
            spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(false);

            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');

            const result = MarketingOptOut.init();
            expect(result).toBeFalse();

            const labels = document.querySelectorAll(labelSelector);
            expect(labels.length).toEqual(2);

            const checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(0);
        });

        it('should return true if visitor is outside EU/EAA', function () {
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'hasCookie').and.returnValue(
                false
            );
            spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(false);

            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');

            const result = MarketingOptOut.init();
            expect(result).toBeTrue();

            const labels = document.querySelectorAll(labelSelector);
            expect(labels.length).toEqual(0);

            const checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(2);
        });

        it('should remove attribution data and reject analytics when visitor unchecks input', function () {
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(true);
            spyOn(MarketingOptOut, 'shouldShowCheckbox').and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'removeAttributionData');
            spyOn(window.Mozilla.Cookies, 'setItem');

            const result = MarketingOptOut.init();
            expect(result).toBeTrue();

            const labels = document.querySelectorAll(labelSelector);
            expect(labels.length).toEqual(0);

            let checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(2);

            document.getElementById('marketing-opt-out-primary').click();
            expect(
                window.Mozilla.StubAttribution.removeAttributionData
            ).toHaveBeenCalled();
            expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                'moz-consent-pref',
                '{"analytics":false,"preference":true}',
                jasmine.any(String),
                '/',
                null,
                false,
                'lax'
            );

            checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(0);
        });

        it('should opt back into analytics and init attribution if visitor re-checks input', function () {
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(true);
            spyOn(MarketingOptOut, 'shouldShowCheckbox').and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'init');
            spyOn(window.Mozilla.Cookies, 'setItem');

            const result = MarketingOptOut.init();
            expect(result).toBeTrue();

            const labels = document.querySelectorAll(labelSelector);
            expect(labels.length).toEqual(0);

            let checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(2);

            // Opt out
            document.getElementById('marketing-opt-out-primary').click();

            checkboxes = document.querySelectorAll(
                '.marketing-opt-out-checkbox-input:checked'
            );
            expect(checkboxes.length).toEqual(0);

            // Opt in
            document.getElementById('marketing-opt-out-secondary').click();
            expect(window.Mozilla.StubAttribution.init).toHaveBeenCalled();
            expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                'moz-consent-pref',
                '{"analytics":true,"preference":true}',
                jasmine.any(String),
                '/',
                null,
                false,
                'lax'
            );

            checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(2);
        });

        it('should remember a previous preference cookie choice if it exists', function () {
            spyOn(
                window.Mozilla.StubAttribution,
                'meetsRequirements'
            ).and.returnValue(true);
            spyOn(MarketingOptOut, 'shouldShowCheckbox').and.returnValue(true);
            spyOn(window.Mozilla.StubAttribution, 'hasCookie').and.returnValue(
                false
            );
            spyOn(window.Mozilla.StubAttribution, 'removeAttributionData');
            spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'setItem');

            const obj = {
                analytics: true,
                preference: false
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            const result = MarketingOptOut.init();
            expect(result).toBeTrue();

            const labels = document.querySelectorAll(labelSelector);
            expect(labels.length).toEqual(0);

            let checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(2);

            document.getElementById('marketing-opt-out-primary').click();
            expect(
                window.Mozilla.StubAttribution.removeAttributionData
            ).toHaveBeenCalled();
            expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                'moz-consent-pref',
                '{"analytics":false,"preference":false}',
                jasmine.any(String),
                '/',
                null,
                false,
                'lax'
            );

            checkboxes = document.querySelectorAll(checkboxSelector);
            expect(checkboxes.length).toEqual(0);
        });
    });
});
