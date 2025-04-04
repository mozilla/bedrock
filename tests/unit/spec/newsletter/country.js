/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FormUtils from '../../../../media/js/newsletter/form-utils.es6';
import CountryForm from '../../../../media/js/newsletter/country.es6';

const TOKEN_MOCK = 'a1a2a3a4-abc1-12ab-a123-12345a12345b';

describe('CountryForm', function () {
    beforeEach(async function () {
        const form = `<div id="country-newsletter-test-form">
            <div class="country-newsletter-content">
                <form id="country-newsletter-form" class="country-newsletter-form" method="post" action="https://basket.mozilla.org/news/user-meta/">
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
        let xhrRequests = [];

        beforeEach(function () {
            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);

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

        it('should handle success', function () {
            spyOn(CountryForm, 'handleFormSuccess').and.callThrough();
            CountryForm.init();
            document.getElementById('country-newsletter-submit').click();

            const req = xhrRequests[0];
            req.status = 200;
            req.readyState = 4;
            req.responseText = '{"status": "ok"}';
            req.onload({ target: req });

            expect(req.open).toHaveBeenCalledWith(
                'POST',
                `https://basket.mozilla.org/news/user-meta/${TOKEN_MOCK}/`,
                true
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

            const req = xhrRequests[0];
            req.status = 400;
            req.readyState = 4;
            req.responseText =
                '{"status": "error", "desc": "Unknown non-helpful error"}';
            req.onload({ target: req });

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

            const req = xhrRequests[0];
            req.status = 500;
            req.readyState = 4;
            req.responseText = null;
            req.onload({ target: req });

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
