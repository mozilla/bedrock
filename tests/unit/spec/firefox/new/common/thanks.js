/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('thanks.js', function () {
    describe('shouldAutoDownload', function () {
        it('should return true for supported platforms', function () {
            expect(
                Mozilla.DownloadThanks.shouldAutoDownload('windows')
            ).toBeTruthy();
            expect(
                Mozilla.DownloadThanks.shouldAutoDownload('osx')
            ).toBeTruthy();
            expect(
                Mozilla.DownloadThanks.shouldAutoDownload('linux')
            ).toBeTruthy();
            expect(
                Mozilla.DownloadThanks.shouldAutoDownload('android')
            ).toBeTruthy();
            expect(
                Mozilla.DownloadThanks.shouldAutoDownload('ios')
            ).toBeTruthy();
        });

        it('should return false for unknown platforms', function () {
            expect(
                Mozilla.DownloadThanks.shouldAutoDownload('other')
            ).toBeFalsy();
        });
    });

    describe('getDownloadURL', function () {
        beforeEach(function () {
            const button = `<ul class="download-list">
                    <li><a id="thanks-download-button-win64" href="https://download.mozilla.org/?product=firefox-stub&amp;os=win64&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-download-button-win64-msi" href="https://download.mozilla.org/?product=firefox-msi-latest-ssl&amp;os=win64&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-download-button-win64-aarch64" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win64-aarch64&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-download-button-win" href="https://download.mozilla.org/?product=firefox-stub&amp;os=win&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-download-button-win-msi" href="https://download.mozilla.org/?product=firefox-msi-latest-ssl&amp;os=win&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-download-button-osx" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=osx&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-download-button-linux64" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=linux64&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-download-button-linux" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=linux&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-download-button-android" href="https://play.google.com/store/apps/details?id=org.mozilla.firefox">Firefox for Android</a></li>
                    <li><a id="thanks-download-button-ios" href="https://itunes.apple.com/us/app/firefox-private-safe-browser/id989804926" data-link-type="download" data-display-name="iOS" data-download-version="ios" data-download-os="iOS">Firefox for iOS</a></li>
                </ul>`;

            const fullInstallerButton = `<ul class="download-list">
                    <li><a id="thanks-full-installer-win64" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win64&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-full-installer-win64-msi" href="https://download.mozilla.org/?product=firefox-msi-latest-ssl&amp;os=win64&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-full-installer-win64-aarch64" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win64-aarch64&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-full-installer-win" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-full-installer-win-msi" href="https://download.mozilla.org/?product=firefox-msi-latest-ssl&amp;os=win&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-full-installer-osx" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=osx&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-full-installer-linux64" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=linux64&amp;lang=en-US">Download Firefox</a></li>
                    <li><a id="thanks-full-installer-linux" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=linux&amp;lang=en-US">Download Firefox</a></li>

                </ul>`;

            document.body.insertAdjacentHTML('beforeend', button);
            document.body.insertAdjacentHTML('beforeend', fullInstallerButton);
        });

        afterEach(function () {
            document.querySelectorAll('.download-list').forEach((e) => {
                e.parentNode.removeChild(e);
            });
        });

        it('should return the correct download for Windows', function () {
            const site = {
                platform: 'windows'
            };
            const result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual(
                'https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US'
            );
        });

        it('should return the full installer download for Windows 7', function () {
            const site = {
                platform: 'windows',
                platformVersion: '6.1'
            };
            const result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual(
                'https://download.mozilla.org/?product=firefox-latest-ssl&os=win&lang=en-US'
            );
        });

        it('should return the correct download for macOS', function () {
            const site = {
                platform: 'osx'
            };
            const result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual(
                'https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US'
            );
        });

        it('should return the correct download for Linux 32bit', function () {
            const site = {
                platform: 'linux',
                isARM: false,
                archSize: 32
            };
            const result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual(
                'https://download.mozilla.org/?product=firefox-latest-ssl&os=linux&lang=en-US'
            );
        });

        it('should return the correct download for Linux 64bit', function () {
            const site = {
                platform: 'linux',
                isARM: false,
                archSize: 64
            };
            const result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual(
                'https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US'
            );
        });

        it('should not return a download for Linux ARM', function () {
            const site = {
                platform: 'linux',
                isARM: true,
                archSize: 64
            };
            const result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toBeFalsy();
        });

        it('should return the correct download for Android', function () {
            const site = {
                platform: 'android'
            };
            const result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual(
                'https://play.google.com/store/apps/details?id=org.mozilla.firefox'
            );
        });

        it('should return the correct download for iOS', function () {
            const site = {
                platform: 'ios'
            };
            const result = Mozilla.DownloadThanks.getDownloadURL(site);
            expect(result).toEqual(
                'https://itunes.apple.com/us/app/firefox-private-safe-browser/id989804926'
            );
        });
    });
});
