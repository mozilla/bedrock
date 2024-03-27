/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import FxaForm from '../../../../media/js/base/fxa-form.es6.js';

describe('fxa-form.js', function () {
    describe('init', function () {
        beforeEach(function () {
            const form = `<form action="https://accounts.firefox.com/" id="fxa-email-form" class="fxa-email-form">
                    <input type="hidden" name="action" value="email">
                    <input type="hidden" name="entrypoint" value="mozilla.org-privacy-products" id="fxa-email-form-entrypoint">
                    <input type="hidden" name="entrypoint_experiment" value="exp" id="fxa-email-form-entrypoint-experiment">
                    <input type="hidden" name="entrypoint_variation" value="var" id="fxa-email-form-entrypoint-variation">
                    <input type="hidden" name="form_type" value="email">
                    <input type="hidden" name="utm_source" value="mozilla.org-privacy-products" id="fxa-email-form-utm-source">
                    <input type="hidden" name="utm_campaign" value="fxa-embedded-form" id="fxa-email-form-utm-campaign">
                    <input type="hidden" name="flow_id" value="">
                    <input type="hidden" name="flow_begin_time" value="">
                    <input type="hidden" name="device_id" value="">
                    <input type="email" name="email" id="fxa-email-field" class="fxa-email-field" placeholder="user@example.com" required="">
                    <button type="submit" class="mzp-c-button mzp-t-primary mzp-t-product" id="fxa-email-form-submit">Continue</button>
                </form>`;

            const data = {
                deviceId: '848377ff6e3e4fc982307a316f4ca3d6',
                flowBeginTime: '1573052386673',
                flowId: '75f9a48a0f66c2f5919a0989605d5fa5dd04625ea5a2ee59b2d5d54637c566d1'
            };

            const mockResponse = new window.Response(JSON.stringify(data), {
                status: 200,
                headers: {
                    'Content-type': 'application/json'
                }
            });

            spyOn(window, 'fetch').and.returnValue(
                window.Promise.resolve(mockResponse)
            );

            window.Mozilla.UITour = sinon.stub();
            window.Mozilla.UITour.showFirefoxAccounts = sinon
                .stub()
                .returns(true);
            window.Mozilla.UITour.ping = sinon.stub().callsArg(0);

            document.body.insertAdjacentHTML('beforeend', form);
        });

        afterEach(function () {
            document.querySelectorAll('.fxa-email-form').forEach((e) => {
                e.parentNode.removeChild(e);
            });
        });

        it('should configure the form for Firefox desktop < 80', function () {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(
                true
            );
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue(
                '79.0'
            );

            return FxaForm.init().then(() => {
                const form = document.getElementById('fxa-email-form');
                expect(form.getAttribute('action')).toEqual(
                    'https://accounts.firefox.com/'
                );
                expect(form.querySelector('[name="flow_id"]').value).toEqual(
                    '75f9a48a0f66c2f5919a0989605d5fa5dd04625ea5a2ee59b2d5d54637c566d1'
                );
                expect(
                    form.querySelector('[name="flow_begin_time"]').value
                ).toEqual('1573052386673');
                expect(form.querySelector('[name="device_id"]').value).toEqual(
                    '848377ff6e3e4fc982307a316f4ca3d6'
                );
            });
        });

        it('should configure the form for Firefox desktop >= 80', function () {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(
                true
            );
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue(
                '80.0'
            );

            return FxaForm.init().then(() => {
                const form = document.getElementById('fxa-email-form');
                expect(form.getAttribute('action')).toEqual(
                    'https://accounts.firefox.com/'
                );
                expect(form.querySelector('[name="context"]').value).toEqual(
                    'fx_desktop_v3'
                );
                expect(form.querySelector('[name="flow_id"]').value).toEqual(
                    '75f9a48a0f66c2f5919a0989605d5fa5dd04625ea5a2ee59b2d5d54637c566d1'
                );
                expect(
                    form.querySelector('[name="flow_begin_time"]').value
                ).toEqual('1573052386673');
                expect(form.querySelector('[name="device_id"]').value).toEqual(
                    '848377ff6e3e4fc982307a316f4ca3d6'
                );
            });
        });

        it('should configure the form for non-Firefox browsers', function () {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(
                false
            );

            return FxaForm.init().then(() => {
                const form = document.getElementById('fxa-email-form');
                expect(form.getAttribute('action')).toEqual(
                    'https://accounts.firefox.com/'
                );
                expect(form.querySelector('[name="context"]')).toBeNull();
                expect(form.querySelector('[name="flow_id"]').value).toEqual(
                    '75f9a48a0f66c2f5919a0989605d5fa5dd04625ea5a2ee59b2d5d54637c566d1'
                );
                expect(
                    form.querySelector('[name="flow_begin_time"]').value
                ).toEqual('1573052386673');
                expect(form.querySelector('[name="device_id"]').value).toEqual(
                    '848377ff6e3e4fc982307a316f4ca3d6'
                );
            });
        });

        it('should pass through utm parameters from the URL to the form', function () {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(
                false
            );
            /* eslint-disable camelcase */
            spyOn(FxaForm, 'getUTMParams').and.returnValue({
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242,
                utm_campaign: 'F100_4242_otherstuff_in_here'
            });
            /* eslint-enable camelcase */

            return FxaForm.init().then(function () {
                const form = document.getElementById('fxa-email-form');
                expect(form.getAttribute('action')).toEqual(
                    'https://accounts.firefox.com/'
                );
                expect(form.querySelector('[name="flow_id"]').value).toEqual(
                    '75f9a48a0f66c2f5919a0989605d5fa5dd04625ea5a2ee59b2d5d54637c566d1'
                );
                expect(
                    form.querySelector('[name="flow_begin_time"]').value
                ).toEqual('1573052386673');
                expect(form.querySelector('[name="device_id"]').value).toEqual(
                    '848377ff6e3e4fc982307a316f4ca3d6'
                );
                expect(form.querySelector('[name="utm_source"]').value).toEqual(
                    'desktop-snippet'
                );
                expect(
                    form.querySelector('[name="utm_campaign"]').value
                ).toEqual('F100_4242_otherstuff_in_here');
                expect(
                    form.querySelector('[name="utm_content"]').value
                ).toEqual('rel-esr');
                expect(form.querySelector('[name="utm_term"]').value).toEqual(
                    '4242'
                );
                expect(form.querySelector('[name="utm_medium"]').value).toEqual(
                    'referral'
                );
            });
        });

        it('should pass through utm parameters from the URL to the form into the UITour', function () {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(
                true
            );
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue(
                '80.0'
            );
            spyOn(Mozilla.Client, 'getFirefoxDetails').and.callFake(
                function (callback) {
                    callback({
                        accurate: true,
                        distribution: undefined
                    });
                }
            );
            spyOn(window.Mozilla.UITour, 'showFirefoxAccounts');
            /* eslint-disable camelcase */
            spyOn(FxaForm, 'getUTMParams').and.returnValue({
                utm_source: 'desktop-snippet',
                utm_content: 'rel-esr',
                utm_medium: 'referral',
                utm_term: 4242,
                utm_campaign: 'F100_4242_otherstuff_in_here'
            });
            /* eslint-enable camelcase */
            return FxaForm.init().then(function () {
                const form = document.getElementById('fxa-email-form');
                form.querySelector('#fxa-email-field').value = 'a@a.com';
                expect(form.getAttribute('action')).toEqual(
                    'https://accounts.firefox.com/'
                );
                expect(form.querySelector('[name="flow_id"]').value).toEqual(
                    '75f9a48a0f66c2f5919a0989605d5fa5dd04625ea5a2ee59b2d5d54637c566d1'
                );
                expect(
                    form.querySelector('[name="flow_begin_time"]').value
                ).toEqual('1573052386673');
                expect(form.querySelector('[name="device_id"]').value).toEqual(
                    '848377ff6e3e4fc982307a316f4ca3d6'
                );
                expect(form.querySelector('[name="utm_source"]').value).toEqual(
                    'desktop-snippet'
                );
                expect(
                    form.querySelector('[name="utm_campaign"]').value
                ).toEqual('F100_4242_otherstuff_in_here');
                expect(
                    form.querySelector('[name="utm_content"]').value
                ).toEqual('rel-esr');
                expect(form.querySelector('[name="utm_term"]').value).toEqual(
                    '4242'
                );
                expect(form.querySelector('[name="utm_medium"]').value).toEqual(
                    'referral'
                );

                form.querySelector('#fxa-email-form-submit').click();
                /* eslint-disable camelcase */
                expect(
                    window.Mozilla.UITour.showFirefoxAccounts
                ).toHaveBeenCalledWith(
                    {
                        utm_source: 'desktop-snippet',
                        utm_content: 'rel-esr',
                        utm_medium: 'referral',
                        utm_term: 4242,
                        utm_campaign: 'F100_4242_otherstuff_in_here',
                        entrypoint_experiment: 'exp',
                        entrypoint_variation: 'var',
                        device_id: '848377ff6e3e4fc982307a316f4ca3d6',
                        flow_id:
                            '75f9a48a0f66c2f5919a0989605d5fa5dd04625ea5a2ee59b2d5d54637c566d1',
                        flow_begin_time: 1573052386673
                    },
                    'mozilla.org-privacy-products',
                    'a@a.com'
                );
                /* eslint-enable camelcase */
            });
        });
    });
});
