/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Forked from https://raw.githubusercontent.com/mozilla/protocol/refs/heads/main/tests/unit/newsletter.js

import MzpNewsletter from '../../../../media/js/newsletter/newsletter.es6.js';

/**
 * Note: There is a `novalidate` attribute added to the <form>
 * element below for testing purposes only.
 */
describe('MzpNewsletter', function () {
    beforeEach(async function () {
        const form = `<aside class="mzp-c-newsletter">
            <div class="newsletter-content">
                <form id="newsletter-form" class="mzp-c-newsletter-form" action="https://basket.mozilla.org/news/subscribe/" method="post" novalidate>
                    <input type="hidden" name="source_url" value="https://www.mozilla.org/en-US/">
                    <fieldset class="mzp-c-newsletter-content">
                        <div class="mzp-c-form-errors hidden" id="newsletter-errors">
                            <ul class="mzp-u-list-styled">
                                <li class="error-email-invalid hidden">
                                    Please enter a valid email address
                                </li>
                                <li class="error-select-country hidden">
                                    Please select a country or region
                                </li>
                                <li class="error-select-language hidden">
                                    Please select a language
                                </li>
                                <li class="error-newsletter-checkbox hidden">
                                    Please check at least one of the newsletter options.
                                </li>
                                <li class="error-privacy-policy hidden">
                                    You must agree to the privacy notice
                                </li>
                                <li class="error-try-again-later hidden">
                                    We are sorry, but there was a problem with our system. Please try again later!
                                </li>
                            </ul>
                        </div>
                        <label for="id_email">Your email address:</label>
                        <input type="email" name="email" placeholder="yourname@example.com" class="mzp-js-email-field" id="id_email">
                        <div id="newsletter-details" class="mzp-c-newsletter-details">
                            <label for="id_country">Select country or region:</label>
                            <p>
                                <select name="country" id="id_country">
                                    <option value="" selected="">Select a country or region</option>
                                    <option value="de">Germany</option>
                                    <option value="fr">France</option>
                                    <option value="us">United States</option>
                                </select>
                            </p>
                            <label for="id_lang">Select language:</label>
                            <p>
                                <select name="lang" id="id_lang">
                                    <option value="" selected="">Select a language</option>
                                    <option value="de">Deutsch</option>
                                    <option value="en">English</option>
                                    <option value="fr">Français</option>
                                </select>
                            </p>
                            <fieldset class="mzp-u-inline">
                                <legend>I want information about:</legend>
                                <p>
                                    <label for="id_newsletters_0" class="mzp-u-inline">
                                        <input type="checkbox" name="newsletters" value="mozilla-foundation" id="id_newsletters_0" checked=""> Mozilla Foundation
                                    </label>
                                    <label for="id_newsletters_1" class="mzp-u-inline">
                                        <input type="checkbox" name="newsletters" value="mozilla-and-you" id="id_newsletters_1" checked=""> Firefox
                                    </label>
                                </p>
                            </fieldset>
                            <p>
                                <label for="privacy" class="mzp-u-inline">
                                    <input type="checkbox" id="privacy" name="privacy"">
                                    I’m okay with Mozilla handling my info as explained in this Privacy Notice
                                </label>
                            </p>
                        </div>
                        <p class="mzp-c-form-submit">
                            <button type="submit" id="newsletter-submit" class="mzp-c-button button-dark">
                                <span class="submit-text">
                                    Sign Up Now
                                </span>
                            <svg class="submit-loading" hidden fill="currentColor" width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><style>.s1{animation:s .8s linear infinite;animation-delay:-.8s}.s2{animation-delay:-.65s}.s3{animation-delay:-.5s}@keyframes s{93.75%,100%{opacity:.2}}</style><circle class="s1" cx="4" cy="12" r="3"/><circle class="s1 s2" cx="12" cy="12" r="3"/><circle class="s1 s3" cx="20" cy="12" r="3"/></svg>
                            </button>
                        </p>
                    </fieldset>
                </form>
                <div id="newsletter-thanks" class="mzp-c-newsletter-thanks hidden">
                    <h3>Thanks!</h3>
                </div>
            </div>
        </aside>`;

        document.body.insertAdjacentHTML('beforeend', form);
    });

    afterEach(function () {
        const form = document.querySelector('.mzp-c-newsletter');
        form.parentNode.removeChild(form);
    });

    describe('form submission', function () {
        let xhrRequests = [];

        beforeEach(function () {
            xhrRequests = [];

            function FakeXHR() {
                this.headers = {};
                this.readyState = 0;
                this.status = 0;
                this.responseText = '';
                this.onload = null;

                xhrRequests.push(this);
            }

            FakeXHR.prototype.open = jasmine.createSpy('open');
            FakeXHR.prototype.setRequestHeader = function (header, value) {
                this.headers[header] = value;
            };
            FakeXHR.prototype.send = jasmine.createSpy('send');

            spyOn(window, 'XMLHttpRequest').and.callFake(function () {
                return new FakeXHR();
            });
        });

        afterEach(function () {
            xhrRequests = [];
        });

        describe('Basket response', function () {
            it('should handle success', function () {
                spyOn(MzpNewsletter, 'handleFormSuccess').and.callThrough();
                MzpNewsletter.init();
                document.getElementById('id_email').value = 'fox@example.com';
                document.getElementById('id_country').value = 'us';
                document.getElementById('id_lang').value = 'en';
                document.getElementById('privacy').click();
                document.getElementById('newsletter-submit').click();

                const req = xhrRequests[0];
                req.status = 200;
                req.readyState = 4;
                req.responseText = '{"status": "ok"}';
                req.onload({ target: req });

                expect(MzpNewsletter.handleFormSuccess).toHaveBeenCalled();
                expect(
                    document
                        .getElementById('newsletter-thanks')
                        .classList.contains('hidden')
                ).toBeFalse();
                expect(
                    document
                        .getElementById('newsletter-form')
                        .classList.contains('hidden')
                ).toBeTrue();
            });

            it('should handle invalid email', function () {
                spyOn(MzpNewsletter, 'handleFormError').and.callThrough();
                MzpNewsletter.init();
                document.getElementById('id_email').value = 'invalid@email';
                document.getElementById('id_country').value = 'us';
                document.getElementById('id_lang').value = 'en';
                document.getElementById('privacy').click();
                document.getElementById('newsletter-submit').click();

                const req = xhrRequests[0];
                req.status = 400;
                req.readyState = 4;
                req.responseText =
                    '{"status": "error", "desc": "Invalid email address"}';
                req.onload({ target: req });

                expect(MzpNewsletter.handleFormError).toHaveBeenCalledWith(
                    'Invalid email address'
                );
                expect(
                    document
                        .getElementById('newsletter-errors')
                        .classList.contains('hidden')
                ).toBeFalse();
                expect(
                    document
                        .querySelector('.error-email-invalid')
                        .classList.contains('hidden')
                ).toBeFalse();
            });

            it('should handle unknown error', function () {
                spyOn(MzpNewsletter, 'handleFormError').and.callThrough();
                MzpNewsletter.init();
                document.getElementById('id_email').value = 'fox@example.com';
                document.getElementById('id_country').value = 'us';
                document.getElementById('id_lang').value = 'en';
                document.getElementById('privacy').click();
                document.getElementById('newsletter-submit').click();

                const req = xhrRequests[0];
                req.status = 400;
                req.readyState = 4;
                req.responseText =
                    '{"status": "error", "desc": "Unknown non-helpful error"}';
                req.onload({ target: req });

                expect(MzpNewsletter.handleFormError).toHaveBeenCalled();
                expect(
                    document
                        .getElementById('newsletter-errors')
                        .classList.contains('hidden')
                ).toBeFalse();
                expect(
                    document
                        .querySelector('.error-try-again-later')
                        .classList.contains('hidden')
                ).toBeFalse();
            });

            it('should handle failure', function () {
                spyOn(MzpNewsletter, 'handleFormError').and.callThrough();
                MzpNewsletter.init();
                document.getElementById('id_email').value = 'fox@example.com';
                document.getElementById('id_country').value = 'us';
                document.getElementById('id_lang').value = 'en';
                document.getElementById('privacy').click();
                document.getElementById('newsletter-submit').click();

                const req = xhrRequests[0];
                req.status = 500;
                req.readyState = 4;
                req.responseText = null;
                req.onload({ target: req });

                expect(MzpNewsletter.handleFormError).toHaveBeenCalled();
                expect(
                    document
                        .getElementById('newsletter-errors')
                        .classList.contains('hidden')
                ).toBeFalse();
                expect(
                    document
                        .querySelector('.error-try-again-later')
                        .classList.contains('hidden')
                ).toBeFalse();
            });

            it('should handle custom success callback', function () {
                const testObj = {
                    successCallback: () => {
                        // no-op
                    },
                    errorCallback: () => {
                        // no-op
                    }
                };
                spyOn(MzpNewsletter, 'handleFormSuccess').and.callThrough();
                spyOn(testObj, 'successCallback');
                MzpNewsletter.init(
                    testObj.successCallback,
                    testObj.errorCallback
                );
                document.getElementById('id_email').value = 'fox@example.com';
                document.getElementById('id_country').value = 'us';
                document.getElementById('id_lang').value = 'en';
                document.getElementById('privacy').click();
                document.getElementById('newsletter-submit').click();

                const req = xhrRequests[0];
                req.status = 200;
                req.readyState = 4;
                req.responseText = '{"status": "ok"}';
                req.onload({ target: req });

                expect(MzpNewsletter.handleFormSuccess).toHaveBeenCalled();
                expect(testObj.successCallback).toHaveBeenCalled();
            });

            it('should handle custom error callback', function () {
                const testObj = {
                    successCallback: () => {
                        // no-op
                    },
                    errorCallback: () => {
                        // no-op
                    }
                };
                spyOn(MzpNewsletter, 'handleFormError').and.callThrough();
                spyOn(testObj, 'errorCallback');
                MzpNewsletter.init(
                    testObj.successCallback,
                    testObj.errorCallback
                );
                document.getElementById('id_email').value = 'fox@example.com';
                document.getElementById('id_country').value = 'us';
                document.getElementById('id_lang').value = 'en';
                document.getElementById('privacy').click();
                document.getElementById('newsletter-submit').click();

                const req = xhrRequests[0];
                req.status = 500;
                req.readyState = 4;
                req.responseText = null;
                req.onload({ target: req });

                expect(MzpNewsletter.handleFormError).toHaveBeenCalled();
                expect(testObj.errorCallback).toHaveBeenCalled();
            });
        });

        describe('AWS response', function () {
            it('should handle success', function () {
                spyOn(MzpNewsletter, 'handleFormSuccess').and.callThrough();
                MzpNewsletter.init();
                document.getElementById('id_email').value = 'fox@example.com';
                document.getElementById('id_country').value = 'us';
                document.getElementById('id_lang').value = 'en';
                document.getElementById('privacy').click();
                document.getElementById('newsletter-submit').click();

                const req = xhrRequests[0];
                req.status = 200;
                req.readyState = 4;
                req.responseText =
                    '{"message": "Newsletter subscription completed successfully", "data": {"email": "fox@example.com", "newsletters": ["mozilla-foundation"]}}';
                req.onload({ target: req });

                expect(MzpNewsletter.handleFormSuccess).toHaveBeenCalled();
                expect(
                    document
                        .getElementById('newsletter-thanks')
                        .classList.contains('hidden')
                ).toBeFalse();
                expect(
                    document
                        .getElementById('newsletter-form')
                        .classList.contains('hidden')
                ).toBeTrue();
            });

            it('should handle unknown error', function () {
                spyOn(MzpNewsletter, 'handleFormError').and.callThrough();
                MzpNewsletter.init();
                document.getElementById('id_email').value = 'fox@example.com';
                document.getElementById('id_country').value = 'us';
                document.getElementById('id_lang').value = 'en';
                document.getElementById('privacy').click();
                document.getElementById('newsletter-submit').click();

                const req = xhrRequests[0];
                req.status = 400;
                req.readyState = 4;
                req.responseText =
                    '{"error": "Subscription Error", "message": "Failed to subscribe: Subscription service failed: Failed to subscribe to newsletters", "data": null}';
                req.onload({ target: req });

                expect(MzpNewsletter.handleFormError).toHaveBeenCalled();
                expect(
                    document
                        .getElementById('newsletter-errors')
                        .classList.contains('hidden')
                ).toBeFalse();
                expect(
                    document
                        .querySelector('.error-try-again-later')
                        .classList.contains('hidden')
                ).toBeFalse();
            });

            it('should handle failure', function () {
                spyOn(MzpNewsletter, 'handleFormError').and.callThrough();
                MzpNewsletter.init();
                document.getElementById('id_email').value = 'fox@example.com';
                document.getElementById('id_country').value = 'us';
                document.getElementById('id_lang').value = 'en';
                document.getElementById('privacy').click();
                document.getElementById('newsletter-submit').click();

                const req = xhrRequests[0];
                req.status = 500;
                req.readyState = 4;
                req.responseText = null;
                req.onload({ target: req });

                expect(MzpNewsletter.handleFormError).toHaveBeenCalled();
                expect(
                    document
                        .getElementById('newsletter-errors')
                        .classList.contains('hidden')
                ).toBeFalse();
                expect(
                    document
                        .querySelector('.error-try-again-later')
                        .classList.contains('hidden')
                ).toBeFalse();
            });

            it('should handle custom success callback', function () {
                const testObj = {
                    successCallback: () => {
                        // no-op
                    },
                    errorCallback: () => {
                        // no-op
                    }
                };
                spyOn(MzpNewsletter, 'handleFormSuccess').and.callThrough();
                spyOn(testObj, 'successCallback');
                MzpNewsletter.init(
                    testObj.successCallback,
                    testObj.errorCallback
                );
                document.getElementById('id_email').value = 'fox@example.com';
                document.getElementById('id_country').value = 'us';
                document.getElementById('id_lang').value = 'en';
                document.getElementById('privacy').click();
                document.getElementById('newsletter-submit').click();

                const req = xhrRequests[0];
                req.status = 200;
                req.readyState = 4;
                req.responseText =
                    '{"message": "Newsletter subscription completed successfully", "data": {"email": "fox@example.com", "newsletters": ["mozilla-foundation"]}}';
                req.onload({ target: req });

                expect(MzpNewsletter.handleFormSuccess).toHaveBeenCalled();
                expect(testObj.successCallback).toHaveBeenCalled();
            });

            it('should handle custom error callback', function () {
                const testObj = {
                    successCallback: () => {
                        // no-op
                    },
                    errorCallback: () => {
                        // no-op
                    }
                };
                spyOn(MzpNewsletter, 'handleFormError').and.callThrough();
                spyOn(testObj, 'errorCallback');
                MzpNewsletter.init(
                    testObj.successCallback,
                    testObj.errorCallback
                );
                document.getElementById('id_email').value = 'fox@example.com';
                document.getElementById('id_country').value = 'us';
                document.getElementById('id_lang').value = 'en';
                document.getElementById('privacy').click();
                document.getElementById('newsletter-submit').click();

                const req = xhrRequests[0];
                req.status = 500;
                req.readyState = 4;
                req.responseText =
                    '{"error": "Subscription Error", "message": "Failed to subscribe: Subscription service failed: Failed to subscribe to newsletters", "data": null}';
                req.onload({ target: req });

                expect(MzpNewsletter.handleFormError).toHaveBeenCalled();
                expect(testObj.errorCallback).toHaveBeenCalled();
            });
        });

        it('should handle incomplete country selection', function () {
            spyOn(MzpNewsletter, 'handleFormError').and.callThrough();
            MzpNewsletter.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('privacy').click();
            document.getElementById('newsletter-submit').click();

            expect(MzpNewsletter.handleFormError).toHaveBeenCalledWith(
                'Country not selected'
            );
            expect(
                document
                    .getElementById('newsletter-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .querySelector('.error-select-country')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle incomplete language selection', function () {
            spyOn(MzpNewsletter, 'handleFormError').and.callThrough();
            MzpNewsletter.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('privacy').click();
            document.getElementById('newsletter-submit').click();

            expect(MzpNewsletter.handleFormError).toHaveBeenCalledWith(
                'Language not selected'
            );
            expect(
                document
                    .getElementById('newsletter-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .querySelector('.error-select-language')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle incomplete newsletter selection', function () {
            spyOn(MzpNewsletter, 'handleFormError').and.callThrough();
            MzpNewsletter.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('id_newsletters_0').click();
            document.getElementById('id_newsletters_1').click();
            document.getElementById('newsletter-submit').click();

            expect(MzpNewsletter.handleFormError).toHaveBeenCalledWith(
                'Newsletter not selected'
            );
            expect(
                document
                    .getElementById('newsletter-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .querySelector('.error-newsletter-checkbox')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle incomplete privacy agreement', function () {
            spyOn(MzpNewsletter, 'handleFormError').and.callThrough();
            MzpNewsletter.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('newsletter-submit').click();

            expect(MzpNewsletter.handleFormError).toHaveBeenCalledWith(
                'Privacy policy not checked'
            );
            expect(
                document
                    .getElementById('newsletter-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .querySelector('.error-privacy-policy')
                    .classList.contains('hidden')
            ).toBeFalse();
        });
    });

    describe('serialize', function () {
        it('should serialize form data as expected', function () {
            MzpNewsletter.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';

            const data1 = MzpNewsletter.serialize();
            expect(data1).toEqual(
                'email=fox%40example.com&country=us&lang=en&source_url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2F&newsletters=mozilla-foundation%2Cmozilla-and-you'
            );
            document.getElementById('id_newsletters_0').click();
            const data2 = MzpNewsletter.serialize();
            expect(data2).toEqual(
                'email=fox%40example.com&country=us&lang=en&source_url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2F&newsletters=mozilla-and-you'
            );
        });
    });
});

describe('checkEmailValidity', function () {
    it('should return true for primitive email format', function () {
        expect(MzpNewsletter.checkEmailValidity('a@a')).toBeTruthy();
        expect(
            MzpNewsletter.checkEmailValidity('example@example.com')
        ).toBeTruthy();
    });

    it('should return false for anything else', function () {
        expect(MzpNewsletter.checkEmailValidity(1234567890)).toBeFalsy();
        expect(MzpNewsletter.checkEmailValidity('aaa')).toBeFalsy();
        expect(MzpNewsletter.checkEmailValidity(null)).toBeFalsy();
        expect(MzpNewsletter.checkEmailValidity(undefined)).toBeFalsy();
        expect(MzpNewsletter.checkEmailValidity(true)).toBeFalsy();
        expect(MzpNewsletter.checkEmailValidity(false)).toBeFalsy();
    });
});
