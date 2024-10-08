/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.4/introduction
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-utils.js', function () {
    describe('trans', function () {
        let stringDiv;

        beforeEach(function () {
            stringDiv = `<div id="strings" data-global-close="Close"
                    data-global-next="Next"
                    data-global-previous="Previous">
                </div>`;

            document.body.insertAdjacentHTML('beforeend', stringDiv);
        });

        afterEach(function () {
            const strings = document.getElementById('strings');
            strings.parentNode.removeChild(strings);
        });

        it('should correctly return translation value', function () {
            const translation = Mozilla.Utils.trans('global-next');
            expect(translation).toEqual('Next');
        });
    });

    describe('initMobileDownloadLinks', function () {
        beforeEach(function () {
            const link =
                '<a class="download-link" href="https://play.google.com/store/apps/details?id=org.mozilla.firefox">Download Firefox</a>';
            document.body.insertAdjacentHTML('beforeend', link);
        });

        afterEach(function () {
            window.site.platform = 'other';

            document.querySelectorAll('.download-link').forEach((e) => {
                e.parentNode.removeChild(e);
            });
        });

        it('should set a URL with the market scheme on Android', function () {
            window.site.platform = 'android';
            Mozilla.Utils.initMobileDownloadLinks();
            const link = document.querySelector('.download-link');
            expect(link.href).toEqual(
                'market://details?id=org.mozilla.firefox'
            );
        });
    });

    describe('getDownloadPlatformVersion', function () {
        it('should return expected values for Windows', function () {
            const site = {
                platform: 'windows'
            };
            const result = Mozilla.Utils.getDownloadPlatformVersion(site);
            expect(result).toEqual({
                version: 'win'
            });
        });

        it('should return expected values for macOS', function () {
            const site = {
                platform: 'osx'
            };
            const result = Mozilla.Utils.getDownloadPlatformVersion(site);
            expect(result).toEqual({
                version: 'osx'
            });
        });

        it('should return expected values for Linux', function () {
            const site = {
                platform: 'linux',
                archSize: 32
            };
            const result = Mozilla.Utils.getDownloadPlatformVersion(site);
            expect(result).toEqual({
                version: 'linux'
            });
        });

        it('should return expected values for Linux 64-Bit builds', function () {
            const site = {
                platform: 'linux',
                archSize: 64
            };
            const result = Mozilla.Utils.getDownloadPlatformVersion(site);
            expect(result).toEqual({
                version: 'linux64'
            });
        });

        it('should return expected values for iOS', function () {
            const site = {
                platform: 'ios'
            };
            const result = Mozilla.Utils.getDownloadPlatformVersion(site);
            expect(result).toEqual({
                version: 'ios'
            });
        });

        it('should return expected values for Android', function () {
            const site = {
                platform: 'android'
            };
            const result = Mozilla.Utils.getDownloadPlatformVersion(site);
            expect(result).toEqual({
                version: 'android'
            });
        });

        it('should return expected values for unsupported / unknown platforms', function () {
            const site = {
                platform: 'other'
            };
            const result = Mozilla.Utils.getDownloadPlatformVersion(site);
            expect(result).toEqual({
                version: 'unsupported'
            });
        });
    });
});
