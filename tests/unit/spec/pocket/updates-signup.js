/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import UpdatesForm from '../../../../media/js/pocket/updates-signup.es6';
import sinon from 'sinon';

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

/**
 * Note: There is a `novalidate` attribute added to the <form>
 * element below for testing purposes only.
 */

describe('updates-signup.es6.js', function () {
    beforeEach(async function () {
        const pocketUpdatesNode = `<div class="pocket-updates">
        <section class="mzp-c-split mzp-l-split-center-on-sm-md">

            <div class="mzp-c-split-container">

                <div class="mzp-c-split-body">

                    <div id="pocket-updates-thanks" class="pocket-updates-success hidden">
                        <h1>Done! Keep an eye out for messages from us.</h1>
                        <p>Until then, why not read something interesting?</p>
                        <a class="mzp-c-button" href="/{LANG}/explore">
                        Discover must-read articles
                        </a>
                    </div>

                    <div id="pocket-updates-form-wrapper">
                        <h1>Keep up with Pocket</h1>
                        <p>Join our mailing list to stay on top of improvements, tips and product updates.</p>
                        <form action="/en/_newsletter_subscribe/" class="mzp-c-newsletter-form pocket-updates-form" id="updates-form" novalidate>

                            <div class="mzp-c-form-errors hide-from-legacy-ie hidden" id="subscribe-errors">
                                <ul class="mzp-u-list-styled">
                                <li class="error-email-invalid hidden">
                                    Please enter a valid email address.
                                </li>
                                <li class="error-try-again-later hidden">
                                    We are sorry, but there was a problem with our system. Please try again later.
                                </li>
                                </ul>
                            </div>

                            <fieldset>
                                <label for="email" class="visually-hidden">
                                pocket-udpates-your-email-address
                                </label>
                                <input type="email" name="email" id="email" placeholder="Your email address" required aria-required="true">

                                <input type="hidden" name="newsletter" id="newsletter" value="news" required aria-required="true">
                                <input type="hidden" name="campaign" id="campaign">
                                <input type="hidden" name="medium" id="medium">
                                <input type="hidden" name="source" id="source">
                                <input type="hidden" name="language" id="language" value="en">
                                <input type="hidden" name="country" id="country" value="US">
                                <input type="hidden" name="form_source" id="form_source" value="/en/pocket-updates-signup/pilot/">

                                <button type="submit" id="updates-form-submit" class="mzp-c-button">Subscribe</button>
                            </fieldset>
                        </form>
                        <div class="legal-links">
                            <p>
                            <a href="/en/privacy/">Privacy</a>
                            </p>
                            <p aria-hidden="true" class="separator">⸱</p>
                            <p>
                            <a href="/en/tos/">Terms</a>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="mzp-c-split-media mzp-l-split-h-center mzp-l-split-media-overflow">
                    <img src="/media/img/pocket/pocket-update-signup.png" alt="" class="mzp-c-split-media-asset">
                </div>
            </div>

        </section>
    </div>`;

        document.body.insertAdjacentHTML('beforeend', pocketUpdatesNode);
    });
    afterEach(function () {
        const node = document.querySelector('.pocket-updates');
        node.parentNode.removeChild(node);
    });

    describe('Form boostrapping with querystrings present', function () {
        it('Should pull data from querystrings when available', function () {
            spyOn(UpdatesForm, 'getSearchParams').and.returnValue(
                new URLSearchParams(
                    'utm_source=test-source' +
                        '&utm_medium=test-medium' +
                        '&utm_noise=test-noise-to-be-ignored' +
                        '&utm_campaign=test-campaign'
                )
            );

            expect(document.getElementById('campaign').value).toBe('');
            expect(document.getElementById('medium').value).toBe('');
            expect(document.getElementById('source').value).toBe('');

            UpdatesForm.init();

            expect(document.getElementById('campaign').value).toBe(
                'test-campaign'
            );
            expect(document.getElementById('medium').value).toBe('test-medium');
            expect(document.getElementById('source').value).toBe('test-source');
        });
    });

    describe('Form boostrapping with querystrings present - XSS check', function () {
        it('Should pull data from querystrings when available', function () {
            spyOn(UpdatesForm, 'getSearchParams').and.returnValue(
                new URLSearchParams(
                    'utm_source=test-source' +
                        '&utm_medium=test-medium<script>alert("xss");</script>' +
                        '&utm_noise=test-noise-to-be-ignored' +
                        '&utm_campaign=%3Cscript%3Ealert(%22xss%22)%3B%3C%2Fscript%3E'
                )
            );

            expect(document.getElementById('campaign').value).toBe('');
            expect(document.getElementById('medium').value).toBe('');
            expect(document.getElementById('source').value).toBe('');

            UpdatesForm.init();

            expect(document.getElementById('campaign').value).toBe('');
            expect(document.getElementById('medium').value).toBe('');
            expect(document.getElementById('source').value).toBe('test-source');
        });
    });

    describe('Form boostrapping without querystrings present', function () {
        it('should find no data to pull data from querystrings', function () {
            spyOn(UpdatesForm, 'getSearchParams').and.returnValue(
                new URLSearchParams('')
            );

            expect(document.getElementById('campaign').value).toBe('');
            expect(document.getElementById('medium').value).toBe('');
            expect(document.getElementById('source').value).toBe('');

            UpdatesForm.init();

            expect(document.getElementById('campaign').value).toBe('');
            expect(document.getElementById('medium').value).toBe('');
            expect(document.getElementById('source').value).toBe('');
        });
    });

    describe('Form submission flows', function () {
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
            spyOn(UpdatesForm, 'handleFormSuccess').and.callThrough();
            UpdatesForm.init();
            expect(document.getElementById('newsletter').value).toBe('news');
            document.getElementById('email').value = 'fox@example.com';
            document.getElementById('updates-form-submit').click();
            xhrRequests[0].respond(
                200,
                { 'Content-Type': 'application/json' },
                '{"status": "success"}'
            );
            expect(UpdatesForm.handleFormSuccess).toHaveBeenCalled();
            expect(
                document
                    .getElementById('pocket-updates-thanks')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .getElementById('pocket-updates-form-wrapper')
                    .classList.contains('hidden')
            ).toBeTrue();
        });

        it('should handle invalid email', function () {
            spyOn(UpdatesForm, 'handleFormError').and.callThrough();
            UpdatesForm.init();
            expect(document.getElementById('newsletter').value).toBe('news');
            document.getElementById('email').value = 'BADEMAILexample.com';
            document.getElementById('updates-form-submit').click();
            xhrRequests[0].respond(
                400,
                { 'Content-Type': 'application/json' },
                '{"status": "error", "detail": {"email": ["This field is required.]"}}'
            );
            expect(UpdatesForm.handleFormError).toHaveBeenCalled();
            expect(
                document
                    .getElementById('pocket-updates-thanks')
                    .classList.contains('hidden')
            ).toBeTrue();
            expect(
                document
                    .getElementById('pocket-updates-form-wrapper')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .getElementById('subscribe-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle other payload error', function () {
            spyOn(UpdatesForm, 'handleFormError').and.callThrough();
            UpdatesForm.init();
            expect(document.getElementById('newsletter').value).toBe('news');
            document.getElementById('email').value = 'test@example.com';
            document.getElementById('updates-form-submit').click();
            xhrRequests[0].respond(
                400,
                { 'Content-Type': 'application/json' },
                '{"status": "error", "detail": "Error parsing JSON data"}'
            );
            expect(UpdatesForm.handleFormError).toHaveBeenCalled();
            expect(
                document
                    .getElementById('pocket-updates-thanks')
                    .classList.contains('hidden')
            ).toBeTrue();
            expect(
                document
                    .getElementById('pocket-updates-form-wrapper')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .getElementById('subscribe-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
        });

        it('should handle Braze subscribe connection error', function () {
            spyOn(UpdatesForm, 'handleFormError').and.callThrough();
            UpdatesForm.init();
            expect(document.getElementById('newsletter').value).toBe('news');
            document.getElementById('email').value = 'test@example.com';
            document.getElementById('updates-form-submit').click();
            xhrRequests[0].respond(
                500,
                { 'Content-Type': 'application/json' },
                '{"status": "error", "detail": "Error contacting subscription provider"}'
            );
            expect(UpdatesForm.handleFormError).toHaveBeenCalled();
            expect(
                document
                    .getElementById('pocket-updates-thanks')
                    .classList.contains('hidden')
            ).toBeTrue();
            expect(
                document
                    .getElementById('pocket-updates-form-wrapper')
                    .classList.contains('hidden')
            ).toBeFalse();
            expect(
                document
                    .getElementById('subscribe-errors')
                    .classList.contains('hidden')
            ).toBeFalse();
        });
    });
});
