/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* eslint camelcase: [2, {properties: "never"}] */
/* eslint new-cap: [2, {"capIsNewExceptions": ["Deferred"]}] */

describe('send-to-device.js', function () {
    let form;

    beforeEach(function () {
        const formMarkup = `<section id="send-to-device" class="send-to-device">
                <div class="form-container">
                    <form class="send-to-device-form">
                        <ul class="mzp-c-form-errors hidden"></ul>
                        <div class="send-to-device-form-fields">
                            <input type="hidden" value="all">
                            <label id="mzp-c-field-label" for="send-to-device-input">Enter your email.</label>
                            <div class="mzp-c-field mzp-l-stretch">
                                <input id="send-to-device-input" class="mzp-c-field-control send-to-device-input" name="s2d-email" type="text" required>
                                <button type="submit" class="button mzp-c-button mzp-t-product">Send</button>
                            </div>
                        </div>
                        <div class="thank-you hidden"><a href="#" role="button" class="send-another">Send to another device</a></div>
                        <div class="loading-spinner"></div>
                    </form>
                </div>
            </section>`;

        document.body.insertAdjacentHTML('beforeend', formMarkup);

        // stub out spinner.js
        window.Spinner = sinon.stub();
        window.Spinner.prototype.spin = sinon.stub();

        // stub out google tag manager
        window.dataLayer = sinon.stub();
        window.dataLayer.push = sinon.stub();

        form = new Mozilla.SendToDevice();
    });

    afterEach(function () {
        form.unbindEvents();
        const content = document.getElementById('send-to-device');
        content.parentNode.removeChild(content);
    });

    describe('instantiation', function () {
        it('should create a new instance of SendToDevice', function () {
            spyOn(form, 'bindEvents');
            form.init();
            expect(form instanceof Mozilla.SendToDevice).toBeTruthy();
            expect(form.bindEvents).toHaveBeenCalled();
        });
    });

    describe('checkEmailValidity', function () {
        it('should return true for primitive email format', function () {
            expect(form.checkEmailValidity('a@a')).toBeTruthy();
            expect(form.checkEmailValidity('example@example.com')).toBeTruthy();
        });

        it('should return false for anything else', function () {
            expect(form.checkEmailValidity(1234567890)).toBeFalsy();
            expect(form.checkEmailValidity('aaa')).toBeFalsy();
            expect(form.checkEmailValidity(null)).toBeFalsy();
            expect(form.checkEmailValidity(undefined)).toBeFalsy();
            expect(form.checkEmailValidity(true)).toBeFalsy();
            expect(form.checkEmailValidity(false)).toBeFalsy();
        });
    });

    describe('onFormSubmit', function () {
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
            spyOn(form, 'onFormSuccess').and.callThrough();
            form.init();
            document.getElementById('send-to-device-input').value =
                'success@example.com';
            document
                .querySelector('.send-to-device-form button[type="submit"]')
                .click();
            xhrRequests[0].respond(
                200,
                { 'Content-Type': 'application/json' },
                '{"success": "success"}'
            );

            expect(form.onFormSuccess).toHaveBeenCalledWith('success');
        });

        it('should handle invalid email', function () {
            spyOn(form, 'onFormError').and.callThrough();
            form.init();
            document.getElementById('send-to-device-input').value =
                'invalid@email';
            document
                .querySelector('.send-to-device-form button[type="submit"]')
                .click();
            xhrRequests[0].respond(
                200,
                { 'Content-Type': 'application/json' },
                '{"success": false, "errors": ["email"]}'
            );

            expect(form.onFormError).toHaveBeenCalledWith(['email']);
        });

        it('should handle failure', function () {
            spyOn(form, 'onFormFailure').and.callThrough();
            form.init();
            document.getElementById('send-to-device-input').value =
                'failure@example.com';
            document
                .querySelector('.send-to-device-form button[type="submit"]')
                .click();
            xhrRequests[0].respond(
                400,
                { 'Content-Type': 'application/json' },
                '{"success": false, "errors": ["system"]}'
            );

            expect(form.onFormFailure).toHaveBeenCalled();
        });
    });
});
