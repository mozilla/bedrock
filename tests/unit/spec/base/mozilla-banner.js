/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global sinon, */

describe('mozilla-banner.js', function () {
    beforeEach(function () {
        // stub out google tag manager
        window.dataLayer = sinon.stub();
        window.dataLayer.push = sinon.stub();
    });

    describe('init', function () {
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

            Mozilla.Banner.id = null;
        });

        it('should show the banner if no cookie is set', function () {
            spyOn(window.Mozilla.Banner, 'hasCookie').and.returnValue(false);
            spyOn(window.Mozilla.Banner, 'show');
            Mozilla.Banner.init(bannerId);
            expect(Mozilla.Banner.id).toEqual(bannerId);
            expect(Mozilla.Banner.show).toHaveBeenCalled();
        });

        it('should not show the banner if there is a cookie', function () {
            spyOn(window.Mozilla.Banner, 'hasCookie').and.returnValue(true);
            spyOn(window.Mozilla.Banner, 'show');
            Mozilla.Banner.init(bannerId);
            expect(Mozilla.Banner.id).toEqual(bannerId);
            expect(Mozilla.Banner.show).not.toHaveBeenCalled();
        });
    });

    describe('close', function () {
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

            Mozilla.Banner.id = null;
        });

        it('should close the banner when clicked and set a cookie', function () {
            spyOn(window.Mozilla.Banner, 'hasCookie').and.returnValue(false);
            spyOn(window.Mozilla.Banner, 'setCookie');
            spyOn(window.Mozilla.Banner, 'close').and.callThrough();
            Mozilla.Banner.init(bannerId);
            const banner = document.getElementById(bannerId);
            expect(
                banner.classList.contains('c-banner-is-visible')
            ).toBeTruthy();
            const close = document.querySelector('.c-banner-close');
            close.click();
            expect(Mozilla.Banner.close).toHaveBeenCalled();
            expect(Mozilla.Banner.setCookie).toHaveBeenCalledWith(bannerId);
            expect(document.getElementById(bannerId)).toBeNull();
        });
    });
});
