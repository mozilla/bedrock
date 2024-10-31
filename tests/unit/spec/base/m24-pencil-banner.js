/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import M24PencilBanner from '../../../../media/js/base/banners/m24-pencil-banner.es6';

describe('mozilla-banner.es6.js', function () {
    beforeEach(function () {
        const content = `<aside class="m24-pencil-banner hidden">
            <div class="m24-pencil-banner-copy">
                <p>Promo copy</p>
            </div>
            <button class="m24-pencil-banner-close" type="button">Close</button>
        </aside>`;
        document.body.insertAdjacentHTML('beforeend', content);

        // stub out google tag manager
        window.dataLayer = sinon.stub();
        window.dataLayer.push = sinon.stub();
    });

    describe('init()', function () {
        it('should show the banner if no cookie is set', function () {
            spyOn(M24PencilBanner, 'hasCookie').and.returnValue(false);
            spyOn(M24PencilBanner, 'show');
            M24PencilBanner.init();
            expect(M24PencilBanner.show).toHaveBeenCalled();
        });

        it('should not show the banner if there is a cookie', function () {
            spyOn(M24PencilBanner, 'hasCookie').and.returnValue(true);
            spyOn(M24PencilBanner, 'show');
            M24PencilBanner.init();
            expect(M24PencilBanner.show).not.toHaveBeenCalled();
        });
    });

    describe('close()', function () {
        it('should close the banner when clicked and set a cookie', function () {
            spyOn(M24PencilBanner, 'hasCookie').and.returnValue(false);
            spyOn(M24PencilBanner, 'setCookie');
            spyOn(M24PencilBanner, 'close').and.callThrough();
            M24PencilBanner.init();
            const banner = document.querySelector('.m24-pencil-banner');
            expect(banner.classList.contains('hidden')).toBeFalsy();
            const close = document.querySelector('.m24-pencil-banner-close');
            close.click();
            expect(M24PencilBanner.close).toHaveBeenCalled();
            expect(M24PencilBanner.setCookie).toHaveBeenCalled();
        });
    });

    describe('setCookie()', function () {
        it('should set a cookie as expected', function () {
            spyOn(M24PencilBanner, 'consentsToCookies').and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'setItem');
            M24PencilBanner.setCookie();
            expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                'pencil-banner',
                true,
                jasmine.any(String),
                '/',
                undefined,
                false,
                'lax'
            );
        });

        it('should not set a cookie if user does not consent to preference cookies', function () {
            spyOn(M24PencilBanner, 'consentsToCookies').and.returnValue(false);
            spyOn(window.Mozilla.Cookies, 'setItem');
            M24PencilBanner.setCookie();
            expect(window.Mozilla.Cookies.setItem).not.toHaveBeenCalled();
        });
    });

    describe('consentsToCookies()', function () {
        it('should return true if preference cookies are permitted', function () {
            const obj = {
                analytics: false,
                preference: true
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            expect(M24PencilBanner.consentsToCookies()).toBeTrue();
        });

        it('should return false if preference cookies are rejected', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            expect(M24PencilBanner.consentsToCookies()).toBeFalse();
        });

        it('should return true if consent cookie does not exist', function () {
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(false);
            expect(M24PencilBanner.consentsToCookies()).toBeTrue();
        });
    });
});
