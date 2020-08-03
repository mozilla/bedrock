/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global sinon */

describe('thanks.js', function() {
    'use strict';

    describe('shouldAutoDownload', function() {

        it('should return true for supported platforms', function() {
            expect(Mozilla.DownloadThanks.shouldAutoDownload('windows')).toBeTruthy();
            expect(Mozilla.DownloadThanks.shouldAutoDownload('osx')).toBeTruthy();
            expect(Mozilla.DownloadThanks.shouldAutoDownload('linux')).toBeTruthy();
            expect(Mozilla.DownloadThanks.shouldAutoDownload('android')).toBeTruthy();
            expect(Mozilla.DownloadThanks.shouldAutoDownload('ios')).toBeTruthy();
        });

        it('should return false for unknown platforms', function() {
            expect(Mozilla.DownloadThanks.shouldAutoDownload('other')).toBeFalsy();
        });
    });

    describe('getDownloadURL', function() {

        beforeEach(function() {
            var button = '<ul class="download-list">' +
                         '<li><a id="thanks-download-button-win64" href="https://download.mozilla.org/?product=firefox-stub&amp;os=win64&amp;lang=en-US">Download Firefox</a></li>' +
                         '<li><a id="thanks-download-button-win64-msi" href="https://download.mozilla.org/?product=firefox-msi-latest-ssl&amp;os=win64&amp;lang=en-US">Download Firefox</a></li>' +
                         '<li><a id="thanks-download-button-win64-aarch64" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win64-aarch64&amp;lang=en-US">Download Firefox</a></li>' +
                         '<li><a id="thanks-download-button-win" href="https://download.mozilla.org/?product=firefox-stub&amp;os=win&amp;lang=en-US">Download Firefox</a></li>' +
                         '<li><a id="thanks-download-button-win-msi" href="https://download.mozilla.org/?product=firefox-msi-latest-ssl&amp;os=win&amp;lang=en-US">Download Firefox</a></li>' +
                         '<li><a id="thanks-download-button-osx" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=osx&amp;lang=en-US">Download Firefox</a></li>' +
                         '<li><a id="thanks-download-button-linux64" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=linux64&amp;lang=en-US">Download Firefox</a></li>' +
                         '<li><a id="thanks-download-button-linux" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=linux&amp;lang=en-US">Download Firefox</a></li>' +
                         '<li><a id="thanks-download-button-android" href="https://play.google.com/store/apps/details?id=org.mozilla.firefox">Firefox for Android</a></li>' +
                         '<li><a id="thanks-download-button-ios" href="https://itunes.apple.com/us/app/firefox-private-safe-browser/id989804926" data-link-type="download" data-display-name="iOS" data-download-version="ios" data-download-os="iOS">Firefox for iOS</a></li>' +
                         '</ul>';

            document.body.insertAdjacentHTML('beforeend', button);
        });

        afterEach(function() {
            document.querySelectorAll('.download-list').forEach(function(e)  {
                e.parentNode.removeChild(e);
            });
        });

        it('should return the correct download for Windows', function() {
            var site = {
                platform: 'windows',
                isARM: false
            };
            var result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual('https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US');
        });

        it('should return the correct download for Windows ARM64 / AArch64', function() {
            var site = {
                platform: 'windows',
                isARM: true
            };
            var result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual('https://download.mozilla.org/?product=firefox-latest-ssl&os=win64-aarch64&lang=en-US');
        });

        it('should return the correct download for macOS', function() {
            var site = {
                platform: 'osx',
            };
            var result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual('https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US');
        });

        it('should return the correct download for Linux 32bit', function() {
            var site = {
                platform: 'linux',
                isARM: false,
                archSize: 32
            };
            var result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual('https://download.mozilla.org/?product=firefox-latest-ssl&os=linux&lang=en-US');
        });

        it('should return the correct download for Linux 64bit', function() {
            var site = {
                platform: 'linux',
                isARM: false,
                archSize: 64
            };
            var result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual('https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US');
        });

        it('should not return a download for Linux ARM', function() {
            var site = {
                platform: 'linux',
                isARM: true,
                archSize: 64
            };
            var result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toBeFalsy();
        });

        it('should return the correct download for Android', function() {
            var site = {
                platform: 'android',
            };
            var result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual('https://play.google.com/store/apps/details?id=org.mozilla.firefox');
        });

        it('should return the correct download for iOS', function() {
            var site = {
                platform: 'ios',
            };
            var result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual('https://itunes.apple.com/us/app/firefox-private-safe-browser/id989804926');
        });
    });
});
