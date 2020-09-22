/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.4/introduction
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-utils.js', function() {
    'use strict';

    describe('trans', function () {
        var stringDiv;

        beforeEach(function () {
            stringDiv = '<div id="strings" data-global-close="Close" ' +
            'data-global-next="Next" ' +
            'data-global-previous="Previous"> ' +
            '</div>';

            document.body.insertAdjacentHTML('beforeend', stringDiv);
        });

        afterEach(function() {
            var strings = document.getElementById('strings');
            strings.parentNode.removeChild(strings);
        });

        it('should correctly return translation value', function () {
            var translation = Mozilla.Utils.trans('global-next');
            expect(translation === 'Next');
        });
    });

    describe('initMobileDownloadLinks', function () {

        beforeEach(function() {
            var link = '<a class="download-link" href="https://play.google.com/store/apps/details?id=org.mozilla.firefox">Download Firefox</a>';
            document.body.insertAdjacentHTML('beforeend', link);
        });

        afterEach(function(){
            window.site.platform = 'other';

            document.querySelectorAll('.download-link').forEach(function(e)  {
                e.parentNode.removeChild(e);
            });
        });

        it('should set a URL with the market scheme on Android', function () {
            window.site.platform = 'android';
            Mozilla.Utils.initMobileDownloadLinks();
            var link = document.querySelector('.download-link');
            expect(link.href).toEqual('market://details?id=org.mozilla.firefox');
        });
    });

    describe('maybeSwitchToChinaRepackImages', function() {

        var defaultSrc = '/img/placeholder.png';
        var partnerASrc = '/img/foo.png';

        beforeEach(function () {
            var img = '<img class="test-image" src="' + defaultSrc + '" data-partnera-link="' + partnerASrc + '">';
            document.body.insertAdjacentHTML('beforeend', img);
        });

        afterEach(function() {
            document.querySelectorAll('.test-image').forEach(function(e)  {
                e.parentNode.removeChild(e);
            });
        });

        it('should use specified image for certain distributions', function () {
            Mozilla.Utils.maybeSwitchToChinaRepackImages({
                distribution: 'PartnerA'
            });
            var img = document.querySelector('.test-image');
            expect(img.src).toContain(partnerASrc);
        });

        it('should use default image for other distributions', function () {
            Mozilla.Utils.maybeSwitchToChinaRepackImages({
                distribution: 'PartnerB'
            });
            var img = document.querySelector('.test-image');
            expect(img.src).toContain(defaultSrc);
        });
    });

    describe('getDownloadAttributionValues', function() {

        it('should return expected values for Windows', function () {
            var site = {
                platform: 'windows',
                isARM: false
            };
            var result = Mozilla.Utils.getDownloadAttributionValues(site);
            expect(result).toEqual({
                os: 'Desktop',
                name: 'Windows 32-bit',
                version: 'win'
            });
        });

        it('should return expected values for Windows ARM64 builds', function () {
            var site = {
                platform: 'windows',
                isARM: true
            };
            var result = Mozilla.Utils.getDownloadAttributionValues(site);
            expect(result).toEqual({
                os: 'Desktop',
                name: 'Windows ARM64/AArch64',
                version: 'win64-aarch64'
            });
        });

        it('should return expected values for macOS', function () {
            var site = {
                platform: 'osx'
            };
            var result = Mozilla.Utils.getDownloadAttributionValues(site);
            expect(result).toEqual({
                os: 'Desktop',
                name: 'macOS',
                version: 'osx'
            });
        });

        it('should return expected values for Linux', function () {
            var site = {
                platform: 'linux',
                archSize: 32
            };
            var result = Mozilla.Utils.getDownloadAttributionValues(site);
            expect(result).toEqual({
                os: 'Desktop',
                name: 'Linux 32-bit',
                version: 'linux'
            });
        });

        it('should return expected values for Linux 64-Bit builds', function () {
            var site = {
                platform: 'linux',
                archSize: 64
            };
            var result = Mozilla.Utils.getDownloadAttributionValues(site);
            expect(result).toEqual({
                os: 'Desktop',
                name: 'Linux 64-bit',
                version: 'linux64'
            });
        });

        it('should return expected values for iOS', function () {
            var site = {
                platform: 'ios'
            };
            var result = Mozilla.Utils.getDownloadAttributionValues(site);
            expect(result).toEqual({
                os: 'iOS',
                name: 'iOS',
                version: 'ios'
            });
        });

        it('should return expected values for Android', function () {
            var site = {
                platform: 'android'
            };
            var result = Mozilla.Utils.getDownloadAttributionValues(site);
            expect(result).toEqual({
                os: 'Android',
                name: 'Android',
                version: 'android'
            });
        });
    });
});
