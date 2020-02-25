/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global sinon, */

describe('mozilla-banner.js', function() {
    'use strict';

    beforeEach(function() {
        // stub out Mozilla.Cookie lib
        window.Mozilla.Cookies = sinon.stub();
        window.Mozilla.Cookies.enabled = sinon.stub().returns(true);
        window.Mozilla.Cookies.setItem = sinon.stub();
        window.Mozilla.Cookies.getItem = sinon.stub();
        window.Mozilla.Cookies.hasItem = sinon.stub();

        // stub out google tag manager
        window.dataLayer = sinon.stub();
        window.dataLayer.push = sinon.stub();
    });

    describe('init', function() {

        var bannerId = 'test-banner';

        beforeEach(function() {
            var banner = '<aside id="page-banner"><button type="button" id="page-banner-close">Close</button></aside>';
            document.body.insertAdjacentHTML('beforeend', banner);
        });

        afterEach(function() {
            var banner = document.getElementById('page-banner');
            banner.parentNode.removeChild(banner);

            Mozilla.Banner.id = null;
        });

        it('should show the banner if no cookie is set', function() {
            spyOn(window.Mozilla.Banner, 'hasCookie').and.returnValue(false);
            spyOn(window.Mozilla.Banner, 'show');
            Mozilla.Banner.init(bannerId);
            expect(Mozilla.Banner.id).toEqual(bannerId);
            expect(Mozilla.Banner.show).toHaveBeenCalled();
        });

        it('should not show the banner if there is a cookie', function() {
            spyOn(window.Mozilla.Banner, 'hasCookie').and.returnValue(true);
            spyOn(window.Mozilla.Banner, 'show');
            Mozilla.Banner.init(bannerId);
            expect(Mozilla.Banner.id).toEqual(bannerId);
            expect(Mozilla.Banner.show).not.toHaveBeenCalled();
        });
    });

    describe('close', function() {
        var bannerId = 'test-banner';

        beforeEach(function() {
            var banner = '<aside id="page-banner"><button type="button" id="page-banner-close">Close</button></aside>';
            document.body.insertAdjacentHTML('beforeend', banner);
        });

        afterEach(function() {
            Mozilla.Banner.id = null;
        });

        it('should close the banner when clicked and set a cookie', function() {
            spyOn(window.Mozilla.Banner, 'hasCookie').and.returnValue(false);
            spyOn(window.Mozilla.Banner, 'setCookie');
            spyOn(window.Mozilla.Banner, 'close').and.callThrough();
            Mozilla.Banner.init(bannerId);
            var banner = document.getElementById('page-banner');
            expect(banner.classList.contains('c-banner-is-visible')).toBeTruthy();
            var close = document.getElementById('page-banner-close');
            close.click();
            expect(Mozilla.Banner.close).toHaveBeenCalled();
            expect(Mozilla.Banner.setCookie).toHaveBeenCalledWith(bannerId);
            expect(document.getElementById('page-banner')).toBeNull();
        });
    });

});
