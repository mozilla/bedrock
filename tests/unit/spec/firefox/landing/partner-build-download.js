/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import PartnerBuildDownload from '../../../../../media/js/firefox/landing/partner-build-download.es6';

describe('partner-build-download.es6.js', function () {
    describe('init()', function () {
        beforeEach(function () {
            const strings = `<div id="strings" data-win-custom-id="partner-firefox-release-smi-smi-001-stub" data-mac-custom-id="partner-firefox-release-smi-smi-001-latest"></div>`;

            const button1 = `<div id="download-primary" class="download-button mzp-c-button-download-container">
                <ul class="download-list">
                    <li class="os_win64">
                        <a class="download-link button" id="download-primary-win64" href="https://download.mozilla.org/?product=firefox-stub&amp;os=win64&amp;lang=en-GB" data-download-version="win64">
                            Download Firefox
                        </a>
                    </li>
                    <li class="os_win64-msi">
                        <a class="download-link button" id="download-primary-win64-msi" href="https://download.mozilla.org/?product=firefox-msi-latest-ssl&amp;os=win64&amp;lang=en-GB" data-download-version="win64-msi">
                            >Download Firefox
                        </a>
                    </li>
                    <li class="os_win64-aarch64">
                        <a class="download-link button" id="download-primary-win64-aarch64" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win64-aarch64&amp;lang=en-GB" data-download-version="win64-aarch64">
                            Download Firefox
                        </a>
                    </li>
                    <li class="os_win">
                        <a class="download-link button" id="download-primary-win" href="https://download.mozilla.org/?product=firefox-stub&amp;os=win&amp;lang=en-GB" data-download-version="win">
                            Download Firefox
                        </a>
                    </li>
                    <li class="os_win-msi">
                        <a class="download-link button" id="download-primary-win-msi" href="https://download.mozilla.org/?product=firefox-msi-latest-ssl&amp;os=win&amp;lang=en-GB" data-download-version="win-msi">
                            Download Firefox
                        </a>
                    </li>
                    <li class="os_osx">
                        <a class="download-link button" id="download-primary-osx" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=osx&amp;lang=en-GB" data-download-version="osx">
                            Download Firefox
                        </a>
                    </li>
                    <li class="os_linux64">
                        <a class="download-link button" id="download-primary-linux64" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=linux64&amp;lang=en-GB" data-download-version="linux64">
                            Download for Linux 64-bit
                        </a>
                    </li>
                    <li class="os_linux">
                        <a class="download-link button" id="download-primary-linux" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=linux&amp;lang=en-GB" data-download-version="linux">
                            Download for Linux 32-bit
                        </a>
                    </li>
                    <li class="os_android">
                        <a class="download-link button" id="download-primary-android" href="https://play.google.com/store/apps/details?id=org.mozilla.firefox&amp;referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org" data-download-version="android">
                            Firefox for Android
                        </a>
                    </li>
                    <li class="os_ios">
                        <a class="download-link button" id="download-primary-ios" href="https://apps.apple.com/us/app/apple-store/id989804926" data-download-version="ios">
                            Firefox for iOS
                        </a>
                    </li>
                </ul>
            </div>`;

            const button2 = `<div id="download-secondary" class="download-button mzp-c-button-download-container">
                <ul class="download-list">
                    <li class="os_win64">
                        <a class="download-link button" id="download-primary-win64" href="https://download.mozilla.org/?product=firefox-stub&amp;os=win64&amp;lang=en-GB" data-download-version="win64">
                            Download Firefox
                        </a>
                    </li>
                    <li class="os_win64-msi">
                        <a class="download-link button" id="download-primary-win64-msi" href="https://download.mozilla.org/?product=firefox-msi-latest-ssl&amp;os=win64&amp;lang=en-GB" data-download-version="win64-msi">
                            >Download Firefox
                        </a>
                    </li>
                    <li class="os_win64-aarch64">
                        <a class="download-link button" id="download-primary-win64-aarch64" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win64-aarch64&amp;lang=en-GB" data-download-version="win64-aarch64">
                            Download Firefox
                        </a>
                    </li>
                    <li class="os_win">
                        <a class="download-link button" id="download-primary-win" href="https://download.mozilla.org/?product=firefox-stub&amp;os=win&amp;lang=en-GB" data-download-version="win">
                            Download Firefox
                        </a>
                    </li>
                    <li class="os_win-msi">
                        <a class="download-link button" id="download-primary-win-msi" href="https://download.mozilla.org/?product=firefox-msi-latest-ssl&amp;os=win&amp;lang=en-GB" data-download-version="win-msi">
                            Download Firefox
                        </a>
                    </li>
                    <li class="os_osx">
                        <a class="download-link button" id="download-primary-osx" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=osx&amp;lang=en-GB" data-download-version="osx">
                            Download Firefox
                        </a>
                    </li>
                    <li class="os_linux64">
                        <a class="download-link button" id="download-primary-linux64" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=linux64&amp;lang=en-GB" data-download-version="linux64">
                            Download for Linux 64-bit
                        </a>
                    </li>
                    <li class="os_linux">
                        <a class="download-link button" id="download-primary-linux" href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=linux&amp;lang=en-GB" data-download-version="linux">
                            Download for Linux 32-bit
                        </a>
                    </li>
                    <li class="os_android">
                        <a class="download-link button" id="download-primary-android" href="https://play.google.com/store/apps/details?id=org.mozilla.firefox&amp;referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org" data-download-version="android">
                            Firefox for Android
                        </a>
                    </li>
                    <li class="os_ios">
                        <a class="download-link button" id="download-primary-ios" href="https://apps.apple.com/us/app/apple-store/id989804926" data-download-version="ios">
                            Firefox for iOS
                        </a>
                    </li>
                </ul>
            </div>`;

            document.body.insertAdjacentHTML('beforeend', strings);
            document.body.insertAdjacentHTML('beforeend', button1);
            document.body.insertAdjacentHTML('beforeend', button2);
        });

        afterEach(function () {
            const strings = document.getElementById('strings');
            strings.parentNode.removeChild(strings);

            const button1 = document.getElementById('download-primary');
            button1.parentNode.removeChild(button1);

            const button2 = document.getElementById('download-secondary');
            button2.parentNode.removeChild(button2);
        });

        it('should update Windows and macOS download URLs with a custom build link', function () {
            PartnerBuildDownload.init();

            const downloadLinksWin = Array.from(
                document.querySelectorAll(
                    '.download-button .download-list .download-link[data-download-version="win"]'
                )
            );
            const downloadLinksMac = Array.from(
                document.querySelectorAll(
                    '.download-button .download-list .download-link[data-download-version="osx"]'
                )
            );

            downloadLinksWin.forEach((link) =>
                expect(link.href).toContain(
                    '?product=partner-firefox-release-smi-smi-001-stub'
                )
            );
            downloadLinksMac.forEach((link) =>
                expect(link.href).toContain(
                    '?product=partner-firefox-release-smi-smi-001-latest'
                )
            );
        });

        it('should not update Windows URLs that are not visible on landing page', function () {
            PartnerBuildDownload.init();

            const downloadLinksWin64 = Array.from(
                document.querySelectorAll(
                    '.download-button .download-list .download-link[data-download-version="win64"]'
                )
            );
            const downloadLinksWinMsi = Array.from(
                document.querySelectorAll(
                    '.download-button .download-list .download-link[data-download-version="win64-msi"]'
                )
            );
            const downloadLinksWinAarch64 = Array.from(
                document.querySelectorAll(
                    '.download-button .download-list .download-link[data-download-version="win64-aarch64"]'
                )
            );

            downloadLinksWin64.forEach((link) =>
                expect(link.href).not.toContain(
                    '?product=partner-firefox-release-smi-smi-001-stub'
                )
            );
            downloadLinksWinMsi.forEach((link) =>
                expect(link.href).not.toContain(
                    '?product=partner-firefox-release-smi-smi-001'
                )
            );
            downloadLinksWinAarch64.forEach((link) =>
                expect(link.href).not.toContain(
                    '?product=partner-firefox-release-smi-smi-001'
                )
            );
        });

        it('should not update Linux download URLs with a custom build link', function () {
            PartnerBuildDownload.init();

            const downloadLinksLinux = Array.from(
                document.querySelectorAll(
                    '.download-button .download-list .download-link[data-download-version="linux"]'
                )
            );
            const downloadLinksLinux64 = Array.from(
                document.querySelectorAll(
                    '.download-button .download-list .download-link[data-download-version="linux64"]'
                )
            );

            downloadLinksLinux.forEach((link) =>
                expect(link.href).not.toContain(
                    '?product=partner-firefox-release-smi-smi-001'
                )
            );
            downloadLinksLinux64.forEach((link) =>
                expect(link.href).not.toContain(
                    '?product=partner-firefox-release-smi-smi-001'
                )
            );
        });

        it('should not update iOS download URLs with a custom build link', function () {
            PartnerBuildDownload.init();

            const downloadLinksIOS = Array.from(
                document.querySelectorAll(
                    '.download-button .download-list .download-link[data-download-version="ios"]'
                )
            );

            downloadLinksIOS.forEach((link) =>
                expect(link.href).not.toContain(
                    '?product=partner-firefox-release-smi-smi-001'
                )
            );
        });

        it('should not update Android download URLs with a custom build link', function () {
            PartnerBuildDownload.init();

            const downloadLinksAndroid = Array.from(
                document.querySelectorAll(
                    '.download-button .download-list .download-link[data-download-version="android"]'
                )
            );

            downloadLinksAndroid.forEach((link) =>
                expect(link.href).not.toContain(
                    '?product=partner-firefox-release-smi-smi-001'
                )
            );
        });
    });
});
