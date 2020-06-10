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
            var content = '<div id="outer-wrapper">' +
                            '<h1>Some title</h1>' +
                            '<aside id="' + bannerId + '"><button type="button" class="c-banner-close">Close</button></aside>' +
                          '</div>';
            document.body.insertAdjacentHTML('beforeend', content);
        });

        afterEach(function() {
            var content = document.getElementById('outer-wrapper');
            content.parentNode.removeChild(content);

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
            var content = '<div id="outer-wrapper">' +
                            '<h1>Some title</h1>' +
                            '<aside id="' + bannerId + '"><button type="button" class="c-banner-close">Close</button></aside>' +
                          '</div>';
            document.body.insertAdjacentHTML('beforeend', content);
        });

        afterEach(function() {
            var content = document.getElementById('outer-wrapper');
            content.parentNode.removeChild(content);

            Mozilla.Banner.id = null;
        });

        it('should close the banner when clicked and set a cookie', function() {
            spyOn(window.Mozilla.Banner, 'hasCookie').and.returnValue(false);
            spyOn(window.Mozilla.Banner, 'setCookie');
            spyOn(window.Mozilla.Banner, 'close').and.callThrough();
            Mozilla.Banner.init(bannerId);
            var banner = document.getElementById(bannerId);
            expect(banner.classList.contains('c-banner-is-visible')).toBeTruthy();
            var close = document.querySelector('.c-banner-close');
            close.click();
            expect(Mozilla.Banner.close).toHaveBeenCalled();
            expect(Mozilla.Banner.setCookie).toHaveBeenCalledWith(bannerId);
            expect(document.getElementById(bannerId)).toBeNull();
        });
    });

});
