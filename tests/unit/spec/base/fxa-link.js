/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import FxaLink from '../../../../media/js/base/fxa-link.es6.js';

describe('fxa-link.js', function () {
    describe('init', function () {
        beforeEach(function () {
            const link =
                '<a href="https://accounts.firefox.com/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in" class="js-fxa-cta-link">Sign In</a>';

            window.Mozilla.UITour = sinon.stub();
            window.Mozilla.UITour.showFirefoxAccounts = sinon
                .stub()
                .returns(true);
            window.Mozilla.UITour.ping = sinon.stub().callsArg(0);

            document.body.insertAdjacentHTML('beforeend', link);
        });

        afterEach(function () {
            document.querySelectorAll('.js-fxa-cta-link').forEach(function (e) {
                e.parentNode.removeChild(e);
            });
        });

        it('should add context param for Firefox desktop >= 80', function () {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(
                true
            );
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue(
                '80.0'
            );
            FxaLink.init();
            const link = document.querySelector('.js-fxa-cta-link');
            expect(link.href).toEqual(
                'https://accounts.firefox.com/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in&context=fx_desktop_v3'
            );
        });

        it('should not add context param for Firefox desktop < 80', function () {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(
                true
            );
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue(
                '79.0'
            );
            FxaLink.init();
            const link = document.querySelector('.js-fxa-cta-link');
            expect(link.href).toEqual(
                'https://accounts.firefox.com/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in'
            );
        });

        it('should not add context or service params for other user agents', function () {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(
                false
            );
            FxaLink.init();
            const link = document.querySelector('.js-fxa-cta-link');
            expect(link.href).toEqual(
                'https://accounts.firefox.com/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in'
            );
        });

        it('should use the UITour for Firefox Desktop >= 80', function () {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(
                true
            );
            spyOn(window.Mozilla.UITour, 'showFirefoxAccounts');
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue(
                '80.0'
            );
            return FxaLink.init(() => {
                const link = document.querySelector('.js-fxa-cta-link');
                expect(link.getAttribute('role')).toEqual('button');
                link.click();
                expect(
                    window.Mozilla.UITour.showFirefoxAccounts
                ).toHaveBeenCalledWith(
                    {
                        /* eslint-disable camelcase */
                        utm_source: 'mozilla.org-firefoxnav',
                        utm_campaign: 'nav',
                        utm_content: 'join-sign-in',
                        utm_medium: 'referral'
                        /* eslint-enable camelcase */
                    },
                    'mozilla.org-firefoxnav'
                );
            });
        });

        it('does NOT use the UITour for non-FxA domains in Fx >= 80', function () {
            const link = document.querySelectorAll('.js-fxa-cta-link')[0];
            link.href = 'https://monitor.firefox.com';
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(
                true
            );
            spyOn(window.Mozilla.UITour, 'showFirefoxAccounts');
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue(
                '80.0'
            );
            return FxaLink.init(() => {
                expect(link.getAttribute('role')).toEqual(null);
            });
        });

        it('handles flow and entrypoint parameters on the link in Fx >= 80', function () {
            const link = document.querySelectorAll('.js-fxa-cta-link')[0];
            link.href =
                'https://accounts.firefox.com/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&' +
                'utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in&' +
                'flow_id=flow&flow_begin_time=100&device_id=dev&entrypoint_experiment=exp&entrypoint_variation=var';
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(
                true
            );
            window.Mozilla.UITour = sinon.stub();
            window.Mozilla.UITour.showFirefoxAccounts = sinon
                .stub()
                .returns(true);
            window.Mozilla.UITour.ping = sinon.stub().callsArg(0);
            spyOn(window.Mozilla.UITour, 'showFirefoxAccounts');
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue(
                '80.0'
            );
            return FxaLink.init(() => {
                const link = document.querySelector('.js-fxa-cta-link');
                expect(link.getAttribute('role')).toEqual('button');
                link.click();
                expect(
                    window.Mozilla.UITour.showFirefoxAccounts
                ).toHaveBeenCalledWith(
                    {
                        /* eslint-disable camelcase */
                        flow_id: 'flow',
                        flow_begin_time: '100',
                        device_id: 'dev',
                        entrypoint_experiment: 'exp',
                        entrypoint_variation: 'var',
                        utm_source: 'mozilla.org-firefoxnav',
                        utm_campaign: 'nav',
                        utm_content: 'join-sign-in',
                        utm_medium: 'referral'
                        /* eslint-enable camelcase */
                    },
                    'mozilla.org-firefoxnav'
                );
            });
        });
    });
});
