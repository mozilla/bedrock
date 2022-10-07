/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import RecoveryEmailForm from '../../../../media/js/newsletter/recovery.es6';

describe('RecoveryEmailForm', function () {
    beforeEach(async function () {
        const form = `<form method="post" action="https://basket.mozilla.org/news/recover/" id="newsletter-recovery-form" class="newsletter-recovery-form mzp-c-form">
        <header class="mzp-c-newsletter-header">
          <p>Enter your email address and we’ll send you a link to your email preference center.</p>
        </header>

        <div class="mzp-c-form-errors hidden" id="newsletter-errors">
            <ul class="mzp-u-list-styled">
                <li class="error-email-invalid hidden">This is not a valid email address. Please check the spelling.</li>
                <li class="error-email-not-found hidden">This email address is not in our system. Please double check your address or subscribe to our newsletters.</li>
                <li class="error-try-again-later hidden">We are sorry, but there was a problem with our system. Please try again later!</li>
            </ul>
        </div>

        <div class="newsletter-recovery-form-success-msg hidden">
            <p>Success! An email has been sent to you with your preference center link. Thanks!</p>
        </div>

        <div class="newsletter-recovery-form-fields">
          <div class="mzp-c-field mzp-l-stretch">
            <label for="id_email" class="mzp-c-field-label">Your email address:</label>
            <input type="email" name="email" required="" class="mzp-c-field-control" id="id_email">
          </div>
          <div class="mzp-c-button-container mzp-l-stretch">
            <button class="mzp-c-button" id="newsletter-submit" type="submit">Send me a link</button>
          </div>
        </div>
      </form>`;
        document.body.insertAdjacentHTML('beforeend', form);
    });

    afterEach(function () {
        const form = document.getElementById('newsletter-recovery-form');
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
            spyOn(RecoveryEmailForm, 'handleFormSuccess').and.callThrough();
            RecoveryEmailForm.init();
            document.getElementById('id_email').value = 'fox@example.com';
            document.getElementById('newsletter-submit').click();
            xhrRequests[0].respond(
                200,
                { 'Content-Type': 'application/json' },
                '{"status": "ok"}'
            );

            expect(RecoveryEmailForm.handleFormSuccess).toHaveBeenCalled();
            expect(
                document
                    .querySelector('.newsletter-recovery-form-fields')
                    .classList.contains('hidden')
            ).toBeTrue();
            expect(
                document
                    .querySelector('.newsletter-recovery-form-success-msg')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle invalid email', function () {
            spyOn(RecoveryEmailForm, 'handleFormError').and.callThrough();
            RecoveryEmailForm.init();
            document.getElementById('id_email').value = 'invalid@email';
            document.getElementById('newsletter-submit').click();
            xhrRequests[0].respond(
                400,
                { 'Content-Type': 'application/json' },
                '{"status": "error", "desc": "Invalid email address"}'
            );

            expect(RecoveryEmailForm.handleFormError).toHaveBeenCalledWith(
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

        it('should handle unknown email', function () {
            spyOn(RecoveryEmailForm, 'handleFormError').and.callThrough();
            RecoveryEmailForm.init();
            document.getElementById('id_email').value = 'ohnoes@example.com';
            document.getElementById('newsletter-submit').click();
            xhrRequests[0].respond(
                400,
                { 'Content-Type': 'application/json' },
                '{"status": "error", "desc": "Email address not known"}'
            );

            expect(RecoveryEmailForm.handleFormError).toHaveBeenCalledWith(
                'Email address not known'
            );
            expect(
                document
                    .getElementById('newsletter-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .querySelector('.error-email-not-found')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle unknown error', function () {
            spyOn(RecoveryEmailForm, 'handleFormError').and.callThrough();
            RecoveryEmailForm.init();
            document.getElementById('id_email').value = 'ohnoes@example.com';
            document.getElementById('newsletter-submit').click();
            xhrRequests[0].respond(
                400,
                { 'Content-Type': 'application/json' },
                '{"status": "error", "desc": "Unknown non-helpful error"}'
            );

            expect(RecoveryEmailForm.handleFormError).toHaveBeenCalled();
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
            spyOn(RecoveryEmailForm, 'handleFormError').and.callThrough();
            RecoveryEmailForm.init();
            document.getElementById('id_email').value = 'ohnoes@example.com';
            document.getElementById('newsletter-submit').click();
            xhrRequests[0].respond(
                500,
                { 'Content-Type': 'application/json' },
                null
            );

            expect(RecoveryEmailForm.handleFormError).toHaveBeenCalled();
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
});
