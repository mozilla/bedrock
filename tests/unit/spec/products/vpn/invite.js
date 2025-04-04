/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import WaitListForm from '../../../../../media/js/products/vpn/invite.es6';

/**
 * Note: There is a `novalidate` attribute added to the <form>
 * element below for testing purposes only.
 */
describe('WaitListForm', function () {
    beforeEach(async function () {
        const form = `<div class="vpn-waitlist-invite-form">
            <form id="newsletter-form" class="mzp-c-newsletter-form" action="https://basket.mozilla.org/news/subscribe/" method="post" novalidate>
                <h1 class="mzp-c-form-header">Join the VPN Waitlist</h1>
                <p class="mzp-c-form-subtitle">Get notified when Mozilla VPN is available for your device and region.</p>
                <div hidden="">
                    <ul id="id_newsletters">
                        <li>
                            <label for="id_newsletters_0">
                                <input type="checkbox" name="newsletters" value="guardian-vpn-waitlist" id="id_newsletters_0" checked="">
                                guardian-vpn-waitlist
                            </label>

                        </li>
                    </ul>
                </div>
                <input type="hidden" name="source_url" value="https://www.mozilla.org/en-US/products/vpn/invite/">

                <fieldset class="mzp-c-newsletter-content">
                    <div class="mzp-c-form-errors hide-from-legacy-ie hidden" id="newsletter-errors">
                        <ul class="mzp-u-list-styled">
                            <li class="error-email-invalid hidden">Please enter a valid email address</li>
                            <li class="error-select-country hidden">Please select a country or region</li>
                            <li class="error-select-language hidden">Please select a language</li>
                            <li class="error-try-again-later hidden">We are sorry, but there was a problem with our system. Please try again later!</li>
                        </ul>
                    </div>

                    <div>
                        <label for="id_email">
                            What is your email address?
                            <em class="mzp-c-fieldnote">Required</em>
                        </label>
                        <input type="email" class="mzp-js-email-field" id="id_email" name="email" required="" aria-required="true" placeholder="yourname@example.com">
                    </div>

                    <div id="newsletter-details" class="mzp-c-newsletter-details">
                        <label for="id_country">
                            What country do you live in?
                            <em class="mzp-c-fieldnote">Required</em>
                        </label>
                        <select name="country" required="required" aria-required="true" id="id_country">
                            <option value="" selected="">Select a country or region</option>
                            <option value="de">Germany</option>
                            <option value="fr">France</option>
                            <option value="us">United States</option>
                        </select>

                        <label for="id_lang">
                            Select your preferred language.
                            <em class="mzp-c-fieldnote">Required</em>
                        </label>
                        <select name="lang" required="required" aria-required="true" id="id_lang">
                            <option value="" selected="">Select a language</option>
                            <option value="de">Deutsch</option>
                            <option value="en">English</option>
                            <option value="fr">Français</option>
                        </select>
                    </div>
                    <p class="mzp-c-form-submit">
                        <button class="mzp-c-button mzp-t-xl" id="newsletter-submit" type="submit" data-cta-text="Join the Waitlist">Join the Waitlist</button>
                    </p>
                </fieldset>
            </form>
            <div id="newsletter-thanks" class="vpn-invite-success hidden">
                <h3>Thanks! You’re on the list</h3>
                <p>Once Mozilla VPN becomes available for your region, we’ll email you.</p>
            </div>
        </div>`;

        document.body.insertAdjacentHTML('beforeend', form);

        // stub out google tag manager
        window.dataLayer = sinon.stub();
        window.dataLayer.push = sinon.stub();
    });

    afterEach(function () {
        const form = document.querySelector('.vpn-waitlist-invite-form');
        form.parentNode.removeChild(form);
    });

    describe('form submission', function () {
        let xhrRequests = [];

        beforeEach(function () {
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
            spyOn(WaitListForm, 'handleFormSuccess').and.callThrough();
            WaitListForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('newsletter-submit').click();

            const req = xhrRequests[0];
            req.status = 200;
            req.readyState = 4;
            req.responseText = '{"status": "ok"}';
            req.onload({ target: req });

            expect(WaitListForm.handleFormSuccess).toHaveBeenCalled();
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
            spyOn(WaitListForm, 'handleFormError').and.callThrough();
            WaitListForm.init();
            document.getElementById('id_email').value = 'invalid@email';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('newsletter-submit').click();

            const req = xhrRequests[0];
            req.status = 400;
            req.readyState = 4;
            req.responseText =
                '{"status": "error", "desc": "Invalid email address"}';
            req.onload({ target: req });

            expect(WaitListForm.handleFormError).toHaveBeenCalledWith(
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
            spyOn(WaitListForm, 'handleFormError').and.callThrough();
            WaitListForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('newsletter-submit').click();

            expect(WaitListForm.handleFormError).toHaveBeenCalledWith(
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
            spyOn(WaitListForm, 'handleFormError').and.callThrough();
            WaitListForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('newsletter-submit').click();

            expect(WaitListForm.handleFormError).toHaveBeenCalledWith(
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

        it('should handle unknown error', function () {
            spyOn(WaitListForm, 'handleFormError').and.callThrough();
            WaitListForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('newsletter-submit').click();

            const req = xhrRequests[0];
            req.status = 400;
            req.readyState = 4;
            req.responseText =
                '{"status": "error", "desc": "Unknown non-helpful error"}';
            req.onload({ target: req });

            expect(WaitListForm.handleFormError).toHaveBeenCalled();
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
            spyOn(WaitListForm, 'handleFormError').and.callThrough();
            WaitListForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';
            document.getElementById('newsletter-submit').click();

            const req = xhrRequests[0];
            req.status = 500;
            req.readyState = 4;
            req.responseText = null;
            req.onload({ target: req });

            expect(WaitListForm.handleFormError).toHaveBeenCalled();
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
            WaitListForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('id_country').value = 'us';
            document.getElementById('id_lang').value = 'en';

            const data1 = WaitListForm.serialize();
            expect(data1).toEqual(
                'email=fox%40example.com&newsletters=guardian-vpn-waitlist&fpn_country=us&lang=en&format=H&source_url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2Fproducts%2Fvpn%2Finvite%2F'
            );
        });
    });
});
