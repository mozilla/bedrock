/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import CountryForm from '../../../../media/js/newsletter/country.es6';

describe('CountryForm', function () {
    beforeEach(async function () {
        const form = `<div id="country-newsletter-test-form">
            <div class="country-newsletter-content">
                <form id="country-newsletter-form" class="country-newsletter-form" method="post" action="https://basket.mozilla.org/news/user-meta/c3e6c6b9-daf1-43ed-a560-51160e15b360/">
                    <div class="mzp-c-form-errors hidden" id="country-newsletter-errors">
                        <ul class="mzp-u-list-styled">
                            <li class="error-try-again-later hidden">
                                We are sorry, but there was a problem with our system. Please try again later!
                            </li>
                        </ul>
                    </div>

                    <p>
                        <label for="id_country">Country:</label>
                        <select name="country" id="id_country">
                            <option value="de">Germany</option>
                            <option value="fr">France</option>
                            <option value="gb">United Kingdom</option>
                            <option value="us">United States</option>
                        </select>
                    </p>
                    <button type="submit" id="country-newsletter-submit" class="mzp-c-button">Submit</button>
                </form>
            </div>
            <div class="country-newsletter-thanks hidden">
                <h2 class="country-newsletter-title">Thanks for updating your country or region!</h2>
            </div>
        </div>`;
        document.body.insertAdjacentHTML('beforeend', form);
    });

    afterEach(function () {
        const form = document.getElementById('country-newsletter-test-form');
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
            spyOn(CountryForm, 'handleFormSuccess').and.callThrough();
            CountryForm.init();
            document.getElementById('country-newsletter-submit').click();
            xhrRequests[0].respond(
                200,
                { 'Content-Type': 'application/json' },
                '{"status": "ok"}'
            );

            expect(CountryForm.handleFormSuccess).toHaveBeenCalled();
            expect(
                document
                    .querySelector('.country-newsletter-content')
                    .classList.contains('hidden')
            ).toBeTrue();
            expect(
                document
                    .querySelector('.country-newsletter-thanks')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle unknown error', function () {
            spyOn(CountryForm, 'handleFormError').and.callThrough();
            CountryForm.init();
            document.getElementById('country-newsletter-submit').click();
            xhrRequests[0].respond(
                400,
                { 'Content-Type': 'application/json' },
                '{"status": "error", "desc": "Unknown non-helpful error"}'
            );

            expect(CountryForm.handleFormError).toHaveBeenCalled();
            expect(
                document
                    .getElementById('country-newsletter-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .querySelector('.error-try-again-later')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle failure', function () {
            spyOn(CountryForm, 'handleFormError').and.callThrough();
            CountryForm.init();
            document.getElementById('country-newsletter-submit').click();
            xhrRequests[0].respond(
                500,
                { 'Content-Type': 'application/json' },
                null
            );

            expect(CountryForm.handleFormError).toHaveBeenCalled();
            expect(
                document
                    .getElementById('country-newsletter-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .querySelector('.error-try-again-later')
                    .classList.contains('hidden')
            ).toBeFalse();
        });
    });
});
