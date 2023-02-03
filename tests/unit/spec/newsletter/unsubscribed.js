/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FormUtils from '../../../../media/js/newsletter/form-utils.es6';
import UnsubscribedEmailForm from '../../../../media/js/newsletter/unsubscribed.es6';

const TOKEN_MOCK = 'a1a2a3a4-abc1-12ab-a123-12345a12345b';

describe('UnsubscribedEmailForm', function () {
    beforeEach(async function () {
        const form = `<section class="c-updated-block">
            <form id="newsletter-updated-form" action="https://basket.mozilla.org/news/custom_unsub_reason/" method="post" class="c-updated-block-content c-updated-form">

            <div class="mzp-c-form-errors hidden" id="newsletter-updated-form-errors">
                <ul class="mzp-u-list-styled">
                <li class="error-reason hidden">Please select a reason for unsubscribing.</li>
                <li class="error-try-again-later hidden">We are sorry, but there was a problem with our system. Please try again later!</li>
                </ul>
            </div>

            <h3>Would you mind telling us why you’re leaving?</h3>

            <label>
                <input type="checkbox" id="unsub0" name="reason0" value="You send too many emails.">
                You send too many emails.
            </label>

            <label>
                <input type="checkbox" id="unsub1" name="reason1" value="Your content wasn’t relevant to me.">
                Your content wasn’t relevant to me.
            </label>

            <label>
                <input type="checkbox" id="unsub2" name="reason2" value="Your email design was too hard to read.">
                Your email design was too hard to read.
            </label>

            <label>
                <input type="checkbox" id="unsub3" name="reason3" value="I didn’t sign up for this.">
                I didn’t sign up for this.
            </label>

            <label>
                <input type="checkbox" id="unsub4" name="reason4" value="I’m keeping in touch with Mozilla on Twitter instead.">
                I’m keeping in touch with Mozilla on Twitter instead.
            </label>

            <label>
                <input type="checkbox" id="unsub99" name="reason-text-p" value="Other…">
                Other… (maximum 500 characters)<br>
                <textarea id="unsub99-reason-text" cols="35" rows="3" name="reason-text"></textarea>
            </label>
            <div class="mzp-c-button-container mzp-l-align-center">
                <button type="submit" id="newsletter-updated-form-submit" class="mzp-c-button">Submit</button>
            </div>
            </form>

            <div class="c-updated-form-thanks hidden">
                <p>Thanks for telling us why you’re leaving.</p>
            </div>
        </section>`;
        document.body.insertAdjacentHTML('beforeend', form);
    });

    afterEach(function () {
        const form = document.querySelector('.c-updated-block');
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
            spyOn(UnsubscribedEmailForm, 'handleFormSuccess').and.callThrough();
            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            UnsubscribedEmailForm.init();
            document.getElementById('unsub0').click();
            document.getElementById('unsub99').click();
            document.getElementById('unsub99-reason-text').value = 'Test';
            document.getElementById('newsletter-updated-form-submit').click();
            xhrRequests[0].respond(
                200,
                { 'Content-Type': 'application/json' },
                '{"status": "ok"}'
            );

            expect(xhrRequests[0].requestBody).toEqual(
                'token=a1a2a3a4-abc1-12ab-a123-12345a12345b&reason=You%20send%20too%20many%20emails.%0A%0AOther%E2%80%A6%0A%0ATest'
            );
            expect(UnsubscribedEmailForm.handleFormSuccess).toHaveBeenCalled();
            expect(
                document
                    .querySelector('.c-updated-form')
                    .classList.contains('hidden')
            ).toBeTrue();
            expect(
                document
                    .querySelector('.c-updated-form-thanks')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle an incomplete form', function () {
            spyOn(UnsubscribedEmailForm, 'handleFormError').and.callThrough();
            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            UnsubscribedEmailForm.init();
            document.getElementById('newsletter-updated-form-submit').click();
            expect(UnsubscribedEmailForm.handleFormError).toHaveBeenCalled();
            expect(
                document
                    .getElementById('newsletter-updated-form-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .querySelector('.error-reason')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle an invalid token', function () {
            spyOn(UnsubscribedEmailForm, 'handleFormError').and.callThrough();
            spyOn(FormUtils, 'getUserToken').and.returnValue('');
            UnsubscribedEmailForm.init();
            document.getElementById('unsub0').click();
            document.getElementById('newsletter-updated-form-submit').click();
            expect(UnsubscribedEmailForm.handleFormError).toHaveBeenCalled();
            expect(
                document
                    .getElementById('newsletter-updated-form-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .querySelector('.error-try-again-later')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle failure', function () {
            spyOn(UnsubscribedEmailForm, 'handleFormError').and.callThrough();
            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            UnsubscribedEmailForm.init();
            document.getElementById('unsub0').click();
            document.getElementById('newsletter-updated-form-submit').click();
            xhrRequests[0].respond(
                400,
                { 'Content-Type': 'application/json' },
                '{"status": "error", "desc": "Unknown non-helpful error"}'
            );

            expect(UnsubscribedEmailForm.handleFormError).toHaveBeenCalled();
            expect(
                document
                    .getElementById('newsletter-updated-form-errors')
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
            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            UnsubscribedEmailForm.init();
            document.getElementById('unsub0').click();

            const data1 = UnsubscribedEmailForm.serialize();
            expect(data1).toEqual(
                'token=a1a2a3a4-abc1-12ab-a123-12345a12345b&reason=You%20send%20too%20many%20emails.'
            );

            document.getElementById('unsub99').click();
            const data2 = UnsubscribedEmailForm.serialize();
            expect(data2).toEqual(
                'token=a1a2a3a4-abc1-12ab-a123-12345a12345b&reason=You%20send%20too%20many%20emails.%0A%0AOther%E2%80%A6'
            );

            document.querySelector('textarea[name="reason-text"]').value =
                'Testing';
            const data3 = UnsubscribedEmailForm.serialize();
            expect(data3).toEqual(
                'token=a1a2a3a4-abc1-12ab-a123-12345a12345b&reason=You%20send%20too%20many%20emails.%0A%0AOther%E2%80%A6%0A%0ATesting'
            );

            document.querySelector('textarea[name="reason-text"]').value =
                'Testing <script>123</script>';
            const data4 = UnsubscribedEmailForm.serialize();
            expect(data4).toEqual(
                'token=a1a2a3a4-abc1-12ab-a123-12345a12345b&reason=You%20send%20too%20many%20emails.%0A%0AOther%E2%80%A6%0A%0ATesting%20123'
            );
        });
    });
});
