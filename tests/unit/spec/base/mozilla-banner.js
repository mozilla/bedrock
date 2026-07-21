/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import MozBanner from '../../../../media/js/base/banners/mozilla-banner.es6';

describe('mozilla-banner.es6.js', function () {
    beforeEach(function () {
        // stub out google tag manager
        window.dataLayer = sinon.stub();
        window.dataLayer.push = sinon.stub();
    });

    describe('init()', function () {
        const bannerId = 'test-banner';

        beforeEach(function () {
            const content = `<div id="outer-wrapper">
                    <h1>Some title</h1>
                    <aside id="${bannerId}"><button type="button" class="c-banner-close">Close</button></aside>
                </div>`;
            document.body.insertAdjacentHTML('beforeend', content);
        });

        afterEach(function () {
            const content = document.getElementById('outer-wrapper');
            content.parentNode.removeChild(content);

            MozBanner.id = null;
        });

        it('should show the banner if no cookie is set', function () {
            spyOn(MozBanner, 'hasCookie').and.returnValue(false);
            spyOn(MozBanner, 'show');
            MozBanner.init(bannerId);
            expect(MozBanner.id).toEqual(bannerId);
            expect(MozBanner.show).toHaveBeenCalled();
        });

        it('should not show the banner if there is a cookie', function () {
            spyOn(MozBanner, 'hasCookie').and.returnValue(true);
            spyOn(MozBanner, 'show');
            MozBanner.init(bannerId);
            expect(MozBanner.id).toEqual(bannerId);
            expect(MozBanner.show).not.toHaveBeenCalled();
        });
    });

    describe('close()', function () {
        const bannerId = 'test-banner';

        beforeEach(function () {
            const content = `<div id="outer-wrapper">
                    <h1>Some title</h1>
                    <aside id="${bannerId}"><button type="button" class="c-banner-close">Close</button></aside>
                </div>`;
            document.body.insertAdjacentHTML('beforeend', content);
        });

        afterEach(function () {
            const content = document.getElementById('outer-wrapper');
            content.parentNode.removeChild(content);

            MozBanner.id = null;
        });

        it('should close the banner when clicked and set a cookie', function () {
            spyOn(MozBanner, 'hasCookie').and.returnValue(false);
            spyOn(MozBanner, 'setCookie');
            spyOn(MozBanner, 'close').and.callThrough();
            MozBanner.init(bannerId);
            const banner = document.getElementById(bannerId);
            expect(
                banner.classList.contains('c-banner-is-visible')
            ).toBeTruthy();
            const close = document.querySelector('.c-banner-close');
            close.click();
            expect(MozBanner.close).toHaveBeenCalled();
            expect(MozBanner.setCookie).toHaveBeenCalledWith(bannerId);
            expect(document.getElementById(bannerId)).toBeNull();
        });
    });

    describe('setCookie()', function () {
        it('should set a cookie as expected', function () {
            spyOn(MozBanner, 'consentsToCookies').and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'setItem');
            MozBanner.setCookie('some-id');
            expect(window.Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                'moz-banner-some-id',
                true,
                jasmine.any(String),
                '/',
                undefined,
                false,
                'lax'
            );
        });

        it('should not set a cookie if user does not consent to preference cookies', function () {
            spyOn(MozBanner, 'consentsToCookies').and.returnValue(false);
            spyOn(window.Mozilla.Cookies, 'setItem');
            MozBanner.setCookie('some-id');
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

            expect(MozBanner.consentsToCookies()).toBeTrue();
        });

        it('should return false if preference cookies are rejected', function () {
            const obj = {
                analytics: false,
                preference: false
            };
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify(obj)
            );

            expect(MozBanner.consentsToCookies()).toBeFalse();
        });

        it('should return true if consent cookie does not exist', function () {
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(false);
            expect(MozBanner.consentsToCookies()).toBeTrue();
        });
    });
});
