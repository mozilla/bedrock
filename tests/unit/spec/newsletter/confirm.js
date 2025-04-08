/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FormUtils from '../../../../media/js/newsletter/form-utils.es6';
import ConfirmationForm from '../../../../media/js/newsletter/confirm.es6';

const TOKEN_MOCK = 'a1a2a3a4-abc1-12ab-a123-12345a12345b';

describe('ConfirmationForm', function () {
    beforeEach(async function () {
        const form = `<div id="confirm-form-container">
            <form id="confirmation-form" class="c-confirm-form" action="https://basket.mozilla.org/news/subscribe/" data-recovery-url="https://www.mozilla.org/newsletter/recovery/">
                <input type="hidden" name="newsletters" value="mozilla-and-you">
                <input type="hidden" name="source_url" value="https://www.mozilla.org/en-US/newsletter/firefox/confirm/">
                <input type="hidden" name="lang" value="en">
                <div class="c-confirm-form-errors mzp-c-form-errors hidden" id="confirm-form-errors">
                    <p class="c-confirm-error-msg error-invalid-token hidden">
                        This email address is not in our system.
                    </p>
                    <p class="c-confirm-error-msg error-try-again-later hidden">
                        We are sorry, but there was a problem with our system. Please try again later!
                    </p>
                    <p class="c-confirm-error-msg error-update-browser hidden">
                        Your web browser needs to be updated in order to use this page.
                    </p>
                </div>
                <button type="submit" class="c-confirm-form-submit mzp-c-button">Subscribe</button>
            </form>
            <div class="c-confirm-form-thanks hidden">
                <p>Thank you for subscribing!</p>
            </div>
        </div>`;
        document.body.insertAdjacentHTML('beforeend', form);
    });

    afterEach(function () {
        const form = document.getElementById('confirm-form-container');
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

        it('should handle success', function () {
            spyOn(FormUtils, 'getURLToken').and.returnValue(TOKEN_MOCK);
            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            spyOn(ConfirmationForm, 'handleFormSuccess').and.callThrough();

            return ConfirmationForm.init().then(() => {
                document.querySelector('.c-confirm-form-submit').click();

                const req = xhrRequests[0];
                req.status = 200;
                req.readyState = 4;
                req.responseText = '{"status": "ok"}';
                req.onload({ target: req });

                expect(req.open).toHaveBeenCalledWith(
                    'POST',
                    'https://basket.mozilla.org/news/subscribe/',
                    true
                );
                expect(req.send).toHaveBeenCalledWith(
                    'newsletters=mozilla-and-you&source_url=https%3A%2F%2Fwww.mozilla.org%2Fen-US%2Fnewsletter%2Ffirefox%2Fconfirm%2F&lang=en&token=a1a2a3a4-abc1-12ab-a123-12345a12345b'
                );
                expect(ConfirmationForm.handleFormSuccess).toHaveBeenCalled();
                expect(
                    document
                        .querySelector('.c-confirm-form')
                        .classList.contains('hidden')
                ).toBeTrue();
                expect(
                    document
                        .querySelector('.c-confirm-form-thanks')
                        .classList.contains('hidden')
                ).toBeFalse();
            });
        });

        it('should handle invalid token', function () {
            spyOn(FormUtils, 'getURLToken').and.returnValue(TOKEN_MOCK);
            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            spyOn(ConfirmationForm, 'handleFormError').and.callThrough();

            return ConfirmationForm.init()
                .then()
                .then(() => {
                    document.querySelector('.c-confirm-form-submit').click();

                    const req = xhrRequests[0];
                    req.status = 400;
                    req.readyState = 4;
                    req.responseText =
                        '{"status": "error", "desc": "Invalid basket token"}';
                    req.onload({ target: req });

                    expect(ConfirmationForm.handleFormError).toHaveBeenCalled();
                    expect(
                        document
                            .querySelector('.c-confirm-form-errors')
                            .classList.contains('hidden')
                    ).toBeFalse();
                    expect(
                        document
                            .querySelector('.error-invalid-token')
                            .classList.contains('hidden')
                    ).toBeFalse();
                });
        });

        it('should handle unknown error', function () {
            spyOn(FormUtils, 'getURLToken').and.returnValue(TOKEN_MOCK);
            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            spyOn(ConfirmationForm, 'handleFormError').and.callThrough();

            return ConfirmationForm.init().then(() => {
                document.querySelector('.c-confirm-form-submit').click();

                const req = xhrRequests[0];
                req.status = 400;
                req.readyState = 4;
                req.responseText =
                    '{"status": "error", "desc": "Unknown non-helpful error"}';
                req.onload({ target: req });

                expect(ConfirmationForm.handleFormError).toHaveBeenCalled();
                expect(
                    document
                        .querySelector('.c-confirm-form-errors')
                        .classList.contains('hidden')
                ).toBeFalse();
                expect(
                    document
                        .querySelector('.error-try-again-later')
                        .classList.contains('hidden')
                ).toBeFalse();
            });
        });

        it('should handle failure', function () {
            spyOn(FormUtils, 'getURLToken').and.returnValue(TOKEN_MOCK);
            spyOn(FormUtils, 'getUserToken').and.returnValue(TOKEN_MOCK);
            spyOn(ConfirmationForm, 'handleFormError').and.callThrough();

            return ConfirmationForm.init().then(() => {
                document.querySelector('.c-confirm-form-submit').click();

                const req = xhrRequests[0];
                req.status = 500;
                req.readyState = 4;
                req.responseText = null;
                req.onload({ target: req });

                expect(ConfirmationForm.handleFormError).toHaveBeenCalled();
                expect(
                    document
                        .querySelector('.c-confirm-form-errors')
                        .classList.contains('hidden')
                ).toBeFalse();
                expect(
                    document
                        .querySelector('.error-try-again-later')
                        .classList.contains('hidden')
                ).toBeFalse();
            });
        });

        it('should handle an outdated browser', function () {
            spyOn(ConfirmationForm, 'handleFormError').and.callThrough();
            spyOn(ConfirmationForm, 'meetsRequirements').and.returnValue(false);

            ConfirmationForm.init();

            expect(ConfirmationForm.handleFormError).toHaveBeenCalled();
            expect(
                document
                    .querySelector('.c-confirm-form-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .querySelector('.error-update-browser')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should redirect to /newsletter/recovery/ page if token is missing', function () {
            spyOn(FormUtils, 'getURLToken').and.returnValue('');
            spyOn(FormUtils, 'getUserToken').and.returnValue('');
            spyOn(ConfirmationForm, 'redirectToRecoveryPage');

            return ConfirmationForm.init().then(() => {
                expect(
                    ConfirmationForm.redirectToRecoveryPage
                ).toHaveBeenCalled();
            });
        });
    });
});
