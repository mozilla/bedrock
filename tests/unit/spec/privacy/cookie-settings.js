/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import CookieSettingsForm from '../../../../media/js/privacy/cookie-settings-form.es6';

describe('CookieSettingsForm', function () {
    beforeEach(function () {
        const form = `<form class="cookie-consent-form">
            <ul>
                <li class="cookie-category">
                    <h3 class="cookie-category-title">Preference</h3>
                    <div class="cookie-control" id="cookie-control-preference">
                        <label for="cookie-radio-preference-yes" class="cookie-control-label mzp-u-inline">
                            <input type="radio" name="cookie-radio-preference" id="cookie-radio-preference-yes" value="yes">
                            I Agree
                        </label>

                        <label for="cookie-radio-preference-no" class="cookie-control-label mzp-u-inline">
                            <input type="radio" name="cookie-radio-preference" id="cookie-radio-preference-no" value="no">
                            I Do Not Agree
                        </label>
                    </div>
                </li>
                <li class="cookie-category">
                    <h3 class="cookie-category-title">Analytics</h3>
                    <div class="cookie-control" id="cookie-control-analytics">
                        <label for="cookie-radio-analytics-yes" class="cookie-control-label mzp-u-inline">
                            <input type="radio" name="cookie-radio-analytics" id="cookie-radio-analytics-yes" value="yes">
                            I Agree
                        </label>

                        <label for="cookie-radio-analytics-no" class="cookie-control-label mzp-u-inline">
                            <input type="radio" name="cookie-radio-analytics" id="cookie-radio-analytics-no" value="no">
                            I Do Not Agree
                        </label>
                    </div>
                </li>
            </ul>
            <div class="cookie-consent-form-submit">
                <button class="mzp-c-button" type="submit">
                    Save Changes
                </button>

                <p class="hidden cookie-consent-form-submit-success" tabindex="-1">Your cookie settings have been updated.</p>
            </div>
        </form>`;

        document.body.insertAdjacentHTML('beforeend', form);
    });

    afterEach(function () {
        const form = document.querySelector('.cookie-consent-form');

        if (form) {
            form.parentNode.removeChild(form);
        }
    });

    describe('init()', function () {
        afterEach(function () {
            document
                .getElementsByTagName('html')[0]
                .removeAttribute('data-needs-consent');
        });

        it('should initialize default form data if no consent cookie exists and consent is required', function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'True');
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(false);
            CookieSettingsForm.init();
            expect(
                document.getElementById('cookie-radio-preference-no').checked
            ).toBeTruthy();
            expect(
                document.getElementById('cookie-radio-preference-yes').checked
            ).toBeFalsy();
            expect(
                document.getElementById('cookie-radio-analytics-no').checked
            ).toBeTruthy();
            expect(
                document.getElementById('cookie-radio-analytics-yes').checked
            ).toBeFalsy();
        });

        it('should initialize default form data if no consent cookie exists and consent is not required', function () {
            document
                .getElementsByTagName('html')[0]
                .setAttribute('data-needs-consent', 'False');
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(false);
            CookieSettingsForm.init();
            expect(
                document.getElementById('cookie-radio-preference-no').checked
            ).toBeFalsy();
            expect(
                document.getElementById('cookie-radio-preference-yes').checked
            ).toBeTruthy();
            expect(
                document.getElementById('cookie-radio-analytics-no').checked
            ).toBeFalsy();
            expect(
                document.getElementById('cookie-radio-analytics-yes').checked
            ).toBeTruthy();
        });

        it('should update default form data using consent cookie values if they exist', function () {
            const consent = '{"preference":true,"analytics":true}';

            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(consent);
            CookieSettingsForm.init();
            expect(window.Mozilla.Cookies.getItem).toHaveBeenCalledWith(
                'moz-consent-pref'
            );
            expect(
                document.getElementById('cookie-radio-preference-no').checked
            ).toBeFalsy();
            expect(
                document.getElementById('cookie-radio-preference-yes').checked
            ).toBeTruthy();
            expect(
                document.getElementById('cookie-radio-analytics-no').checked
            ).toBeFalsy();
            expect(
                document.getElementById('cookie-radio-analytics-yes').checked
            ).toBeTruthy();
        });

        it('should only update specific cookie options that have consent', function () {
            const consent = '{"preference":true,"analytics":false}';

            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(consent);
            CookieSettingsForm.init();
            expect(window.Mozilla.Cookies.getItem).toHaveBeenCalledWith(
                'moz-consent-pref'
            );
            expect(
                document.getElementById('cookie-radio-preference-no').checked
            ).toBeFalsy();
            expect(
                document.getElementById('cookie-radio-preference-yes').checked
            ).toBeTruthy();
            expect(
                document.getElementById('cookie-radio-analytics-no').checked
            ).toBeTruthy();
            expect(
                document.getElementById('cookie-radio-analytics-yes').checked
            ).toBeFalsy();
        });

        it('should set a consent cookie when the form is submitted', function () {
            spyOn(window.Mozilla.Cookies, 'setItem');

            CookieSettingsForm.init();
            document.getElementById('cookie-radio-preference-yes').click();
            document.getElementById('cookie-radio-analytics-yes').click();
            document
                .querySelector('.cookie-consent-form-submit .mzp-c-button')
                .click();
            expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                'moz-consent-pref',
                '{"preference":true,"analytics":true}',
                jasmine.any(String),
                '/',
                null,
                false,
                'lax'
            );
        });

        it('should set a consent cookie with the same values that are reflected in the form', function () {
            spyOn(window.Mozilla.Cookies, 'setItem');

            CookieSettingsForm.init();
            document.getElementById('cookie-radio-preference-no').click();
            document.getElementById('cookie-radio-analytics-yes').click();
            document
                .querySelector('.cookie-consent-form-submit .mzp-c-button')
                .click();
            expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                'moz-consent-pref',
                '{"preference":false,"analytics":true}',
                jasmine.any(String),
                '/',
                null,
                false,
                'lax'
            );
        });
    });
});
