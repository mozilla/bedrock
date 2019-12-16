/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-fxa-link.js', function() {
    'use strict';

    describe('init', function() {

        beforeEach(function() {
            var link = '<a href="https://accounts.firefox.com/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in" data-mozillaonline-link="https://accounts.firefox.com.cn/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in" class="js-fxa-cta-link">Sign In</a>';
            document.body.insertAdjacentHTML('beforeend', link);
        });

        afterEach(function() {
            document.querySelectorAll('.js-fxa-cta-link').forEach(function(e)  {
                e.parentNode.removeChild(e);
            });
        });

        it('should add service and context params for Firefox desktop < 71', function() {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(true);
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue('70.0');
            Mozilla.FxaLink.init();
            var link = document.querySelector('.js-fxa-cta-link');
            var mozillaOnlineLink = link.getAttribute('data-mozillaonline-link');
            expect(link.href).toEqual('https://accounts.firefox.com/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in&context=fx_desktop_v3&service=sync');
            expect(mozillaOnlineLink).toEqual('https://accounts.firefox.com.cn/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in&context=fx_desktop_v3&service=sync');
        });

        it('should add context param only for Firefox desktop >= 71', function() {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(true);
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue('71.0');
            Mozilla.FxaLink.init();
            var link = document.querySelector('.js-fxa-cta-link');
            var mozillaOnlineLink = link.getAttribute('data-mozillaonline-link');
            expect(link.href).toEqual('https://accounts.firefox.com/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in&context=fx_desktop_v3');
            expect(mozillaOnlineLink).toEqual('https://accounts.firefox.com.cn/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in&context=fx_desktop_v3');
        });

        it('should not add context or service params for other user agents', function() {
            spyOn(window.Mozilla.Client, '_isFirefoxDesktop').and.returnValue(false);
            Mozilla.FxaLink.init();
            var link = document.querySelector('.js-fxa-cta-link');
            var mozillaOnlineLink = link.getAttribute('data-mozillaonline-link');
            expect(link.href).toEqual('https://accounts.firefox.com/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in');
            expect(mozillaOnlineLink).toEqual('https://accounts.firefox.com.cn/signin?form_type=button&entrypoint=mozilla.org-firefoxnav&utm_source=mozilla.org-firefoxnav&utm_medium=referral&utm_campaign=nav&utm_content=join-sign-in');
        });
    });

});
