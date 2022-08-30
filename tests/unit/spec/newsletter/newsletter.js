/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import NewsletterForm from '../../../../media/js/newsletter/newsletter.es6';

describe('NewsletterForm', function () {
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
                            <fieldset class="mzp-u-inline">
                                <legend>Format</legend>
                                <p>
                                    <label for="format-html" class="mzp-u-inline">
                                        <input type="radio" id="format-html" name="fmt" value="H" checked=""> HTML
                                    </label>
                                    <label for="format-text" class="mzp-u-inline">
                                        <input type="radio" id="format-text" name="fmt" value="T"> Text
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
                            <button type="submit" id="newsletter-submit" class="mzp-c-button button-dark">Sign Up Now</button>
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
        let xhr;
        let xhrRequests = [];

        beforeEach(function () {
            xhr = sinon.useFakeXMLHttpRequest();
            xhr.onCreate = (req) => {
                xhrRequests.push(req);
            };
        });

        afterEach(function () {
            xhr.restore();
            xhrRequests = [];
        });

        it('should handle success', function () {
            spyOn(NewsletterForm, 'handleFormSuccess').and.callThrough();
            NewsletterForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('privacy').click();
            document.getElementById('newsletter-submit').click();
            xhrRequests[0].respond(
                200,
                { 'Content-Type': 'application/json' },
                '{"status": "ok"}'
            );

            expect(NewsletterForm.handleFormSuccess).toHaveBeenCalled();
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
            spyOn(NewsletterForm, 'handleFormError').and.callThrough();
            NewsletterForm.init();
            document.getElementById('id_email').value = 'invalid@email';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('privacy').click();
            document.getElementById('newsletter-submit').click();
            xhrRequests[0].respond(
                400,
                { 'Content-Type': 'application/json' },
                '{"status": "error", "desc": "Invalid email address"}'
            );

            expect(NewsletterForm.handleFormError).toHaveBeenCalledWith(
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

        it('should handle incomplete country selection', function () {
            spyOn(NewsletterForm, 'handleFormError').and.callThrough();
            NewsletterForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('privacy').click();
            document.getElementById('newsletter-submit').click();

            expect(NewsletterForm.handleFormError).toHaveBeenCalledWith(
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
            spyOn(NewsletterForm, 'handleFormError').and.callThrough();
            NewsletterForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('privacy').click();
            document.getElementById('newsletter-submit').click();

            expect(NewsletterForm.handleFormError).toHaveBeenCalledWith(
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
            spyOn(NewsletterForm, 'handleFormError').and.callThrough();
            NewsletterForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('id_newsletters_0').click();
            document.getElementById('id_newsletters_1').click();
            document.getElementById('newsletter-submit').click();

            expect(NewsletterForm.handleFormError).toHaveBeenCalledWith(
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
            spyOn(NewsletterForm, 'handleFormError').and.callThrough();
            NewsletterForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('newsletter-submit').click();

            expect(NewsletterForm.handleFormError).toHaveBeenCalledWith(
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

        it('should handle unknown error', function () {
            spyOn(NewsletterForm, 'handleFormError').and.callThrough();
            NewsletterForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('privacy').click();
            document.getElementById('newsletter-submit').click();
            xhrRequests[0].respond(
                400,
                { 'Content-Type': 'application/json' },
                '{"status": "error", "desc": "Unknown non-helpful error"}'
            );

            expect(NewsletterForm.handleFormError).toHaveBeenCalled();
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
            spyOn(NewsletterForm, 'handleFormError').and.callThrough();
            NewsletterForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('privacy').click();
            document.getElementById('newsletter-submit').click();
            xhrRequests[0].respond(
                500,
                { 'Content-Type': 'application/json' },
                null
            );

            expect(NewsletterForm.handleFormError).toHaveBeenCalled();
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
    });

    describe('serialize', function () {
        it('should serialize form data as expected', function () {
            NewsletterForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';

            const data1 = NewsletterForm.serialize();
            expect(data1).toEqual(
                'email=fox%40example.com&format=H&country=us&lang=en&source_url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2F&newsletters=mozilla-foundation%2Cmozilla-and-you'
            );
            document.getElementById('id_newsletters_0').click();
            const data2 = NewsletterForm.serialize();
            expect(data2).toEqual(
                'email=fox%40example.com&format=H&country=us&lang=en&source_url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2F&newsletters=mozilla-and-you'
            );
            document.getElementById('format-text').click();
            const data3 = NewsletterForm.serialize();
            expect(data3).toEqual(
                'email=fox%40example.com&format=T&country=us&lang=en&source_url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2F&newsletters=mozilla-and-you'
            );
        });
    });
});
