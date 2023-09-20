/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* eslint camelcase: [2, {properties: "never"}] */
/* eslint new-cap: [2, {"capIsNewExceptions": ["Deferred"]}] */

describe('all-downloads-unified.js', function () {
    describe('getSelectOption', function () {
        const select = `<select id="select-product" class="c-selection-input">
                <option value="desktop_developer">Firefox Developer Edition</option>
                <option value="desktop_nightly" selected>Firefox Nightly</option>
            '</select>`;

        beforeEach(function () {
            document.body.insertAdjacentHTML('beforeend', select);
        });

        afterEach(function () {
            document.getElementById('select-product').remove();
        });

        it('should return the selection option', function () {
            const el = document.getElementById('select-product');
            const result = Mozilla.FirefoxDownloader.getSelectOption(el);
            expect(result.id).toEqual('desktop_nightly');
            expect(result.label).toEqual('Firefox Nightly');
        });
    });

    describe('setAllSelectOptions', function () {
        const select = `<select id="select_desktop_release_platform" class="c-selection-input">
                <option value="win64">Windows 64-bit</option>
                <option value="osx" selected>macOS</option>
                <option value="linux64">Linux 64-bit</option>
                <option value="win">Windows 32-bit</option>
                <option value="linux">Linux 32-bit</option>
            </select>
            <select id="select_desktop_beta_platform" class="c-selection-input">
                <option value="win64">Windows 64-bit</option>
                <option value="osx" selected>macOS</option>
                <option value="linux64">Linux 64-bit</option>
                <option value="win">Windows 32-bit</option>
                <option value="linux">Linux 32-bit</option>
            </select>`;

        beforeEach(function () {
            document.body.insertAdjacentHTML('beforeend', select);
        });

        afterEach(function () {
            document.getElementById('select_desktop_release_platform').remove();
            document.getElementById('select_desktop_beta_platform').remove();
        });

        it('should set all the options correctly', function () {
            const el = document.querySelectorAll('.c-selection-input');
            Mozilla.FirefoxDownloader.setAllSelectOptions('linux', el);
            const result = Mozilla.FirefoxDownloader.getSelectOption(el[0]);
            expect(result.id).toEqual('linux');
            expect(result.label).toEqual('Linux 32-bit');
            const result2 = Mozilla.FirefoxDownloader.getSelectOption(el[1]);
            expect(result2.id).toEqual('linux');
            expect(result2.label).toEqual('Linux 32-bit');
        });
    });

    describe('getPlatform', function () {
        it('should return known platforms', function () {
            expect(Mozilla.FirefoxDownloader.getPlatform('windows')).toEqual(
                'win64'
            );
            expect(Mozilla.FirefoxDownloader.getPlatform('linux')).toEqual(
                'linux64'
            );
            expect(Mozilla.FirefoxDownloader.getPlatform('osx')).toEqual('osx');
        });

        it('should return false for unknown platforms', function () {
            expect(Mozilla.FirefoxDownloader.getPlatform('other')).toBeFalsy();
        });
    });

    describe('getPageLanguage', function () {
        it('should return en-US for region neutral en values', function () {
            expect(Mozilla.FirefoxDownloader.getPageLanguage('en')).toEqual(
                'en-US'
            );
        });
    });

    describe('getDownloadLink', function () {
        const downloadList = `<ol class="c-locale-list" data-product="desktop_release">
                <li class="c-locale-list-item" data-language="ach">
                    <ul class="c-download-list">
                        <li>
                            <a href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win64&amp;lang=ach" data-download-version="win64">Windows 64-bit</a>
                        </li>
                    </ul>
                </li>
            </ol>`;

        beforeEach(function () {
            document.body.insertAdjacentHTML('beforeend', downloadList);
        });

        afterEach(function () {
            document.querySelector('.c-locale-list').remove();
        });

        it('should return a download link as expected', function () {
            const result = Mozilla.FirefoxDownloader.getDownloadLink(
                'desktop_release',
                'win64',
                'ach'
            );
            expect(result).toEqual(
                'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=ach'
            );
        });

        it('should return an error if a download link is not found', function () {
            const product = 'desktop_release';
            const platform = 'win64';
            const language = 'de';
            spyOn(Mozilla.FirefoxDownloader, 'onError');
            const error = new Error(
                `A download link was not found for: ${product}, platform: ${platform}, language: ${language}`
            );
            Mozilla.FirefoxDownloader.getDownloadLink(
                product,
                platform,
                language
            );
            expect(Mozilla.FirefoxDownloader.onError).toHaveBeenCalledWith(
                error
            );
        });
    });

    describe('setDownloadLink', function () {
        const downloadLink =
            '<a href="#" id="download-button-primary">Download Now</a>';

        beforeEach(function () {
            document.body.insertAdjacentHTML('beforeend', downloadLink);
        });

        afterEach(function () {
            document.getElementById('download-button-primary').remove();
        });

        it('should set desktop download links as expected', function () {
            const el = document.getElementById('download-button-primary');
            const url =
                'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=ach';

            const product = {
                id: 'desktop_beta',
                label: 'Firefox Beta'
            };

            const platform = {
                id: 'win64',
                label: 'Windows 64-bit'
            };

            const language = {
                id: 'ach',
                label: 'Acholi'
            };

            Mozilla.FirefoxDownloader.setDownloadLink(
                url,
                product,
                platform,
                language,
                el
            );
            expect(el.href).toEqual(url);
            expect(el.getAttribute('data-display-name')).toEqual(product.label);
            expect(el.getAttribute('data-download-version')).toEqual(
                platform.id
            );
            expect(el.getAttribute('data-download-language')).toEqual(
                language.id
            );
            expect(el.getAttribute('data-download-os')).toEqual('Desktop');
        });
    });

    describe('setAttributionURL', function () {
        beforeEach(function () {
            spyOn(Mozilla.StubAttribution, 'getCookie').and.returnValue({
                attribution_code: 'some-attribution-code',
                attribution_sig: 'some-attribution-signature'
            });
        });

        it('should return a well formatted attribution link if data exists', function () {
            const url =
                'https://download.mozilla.org/?product=firefox-latest-ssl&os=win&lang=en-US';
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(true);
            expect(Mozilla.FirefoxDownloader.setAttributionURL(url)).toEqual(
                'https://download.mozilla.org/?product=firefox-latest-ssl&os=win&lang=en-US&attribution_code=some-attribution-code&attribution_sig=some-attribution-signature'
            );
        });

        it('should return the original link if data does not exist', function () {
            const url =
                'https://download.mozilla.org/?product=firefox-latest-ssl&os=win&lang=en-US';
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(false);
            expect(Mozilla.FirefoxDownloader.setAttributionURL(url)).toEqual(
                url
            );
        });
    });

    describe('isValidURL', function () {
        it('should return true for bouncer prod links', function () {
            const url =
                'https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US';
            expect(Mozilla.FirefoxDownloader.isValidURL(url)).toBeTruthy();
        });

        it('should return true for bouncer stage links', function () {
            const url =
                'https://bouncer-bouncer.stage.mozaws.net/?product=firefox-latest-ssl&os=osx&lang=en-US';
            expect(Mozilla.FirefoxDownloader.isValidURL(url)).toBeTruthy();
        });

        it('should return true for bouncer dev links', function () {
            const url =
                'https://dev.bouncer.nonprod.webservices.mozgcp.net/?product=firefox-latest-ssl&os=osx&lang=en-US';
            expect(Mozilla.FirefoxDownloader.isValidURL(url)).toBeTruthy();
        });

        it('should return false for everything else', function () {
            const url =
                'https://some.other.domain/?product=firefox-latest-ssl&os=osx&lang=en-US';
            expect(Mozilla.FirefoxDownloader.isValidURL(url)).toBeFalsy();
            expect(Mozilla.FirefoxDownloader.isValidURL(null)).toBeFalsy();
            expect(Mozilla.FirefoxDownloader.isValidURL({})).toBeFalsy();
        });
    });

    describe('setDownloadButtonDesktop', function () {
        const product = {
            id: 'desktop_beta',
            label: 'Firefox Beta'
        };

        const platform = {
            id: 'win64',
            label: 'Windows 64-bit'
        };

        const language = {
            id: 'ach',
            label: 'Acholi'
        };

        const options = `<div class="c-selection-options" data-product="desktop_beta">
                <p class="c-selection c-selection-version">
                    <label for="select_desktop_beta_version" class="c-selection-label">Which version would you like?</label>
                    <select id="select_desktop_beta_version" class="c-selection-input">
                        <option value="desktop_beta">67.0b19</option>
                    </select>
                </p>
                <p class="c-selection c-selection-platform">
                    <label for="select_desktop_beta_platform" class="c-selection-label">Which operating system are you using?</label>
                    <select id="select_desktop_beta_platform" class="c-selection-input">
                        <option value="win64">Windows 64-bit</option>
                    </select>
                </p>
                <p class="c-selection c-selection-language">
                    <label for="select_desktop_beta_language" class="c-selection-label">Would you like to select a different language?</label>
                    <select id="select_desktop_beta_language" class="c-selection-input disabled">
                        <option value="ach">Acholi</option>
                    </select>
                </p>
            </div>
            <ol class="c-locale-list" data-product="desktop_beta">
                <li class="c-locale-list-item" data-language="ach">
                    <ul class="c-download-list">
                        <li>
                            <a href="https://download.mozilla.org/?product=firefox-beta-latest-ssl&amp;os=win64&amp;lang=ach" data-download-version="win64">Windows 64-bit</a>
                        </li>
                    </ul>
                </li>
            </ol>`;

        beforeEach(function () {
            document.body.insertAdjacentHTML('beforeend', options);
        });

        afterEach(function () {
            document.querySelector('.c-selection-options').remove();
            document.querySelector('.c-locale-list').remove();
        });

        it('should set the download link as expected', function () {
            spyOn(
                Mozilla.FirefoxDownloader,
                'getProductSelection'
            ).and.returnValue(product);
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadLink');
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadInfo');
            spyOn(Mozilla.FirefoxDownloader, 'offError');
            Mozilla.FirefoxDownloader.setDownloadButton();
            expect(
                Mozilla.FirefoxDownloader.setDownloadLink
            ).toHaveBeenCalledWith(
                'https://download.mozilla.org/?product=firefox-beta-latest-ssl&os=win64&lang=ach',
                product,
                platform,
                language
            );
            expect(
                Mozilla.FirefoxDownloader.setDownloadInfo
            ).toHaveBeenCalledWith(
                product.label,
                platform.label,
                language.label
            );
            expect(Mozilla.FirefoxDownloader.offError).toHaveBeenCalled();
        });

        it('should throw an error if a download link is not valid', function () {
            const badURL =
                'https://download.mozilla.org.somebadactor.com/download.exe';
            spyOn(
                Mozilla.FirefoxDownloader,
                'getProductSelection'
            ).and.returnValue(product);
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadInfo');
            spyOn(Mozilla.FirefoxDownloader, 'getDownloadLink').and.returnValue(
                badURL
            );
            spyOn(Mozilla.FirefoxDownloader, 'isValidURL').and.returnValue(
                false
            );
            spyOn(Mozilla.FirefoxDownloader, 'onError');
            Mozilla.FirefoxDownloader.setDownloadButton();
            const error = new Error(
                `An unrecognised download link was found: ${badURL}`
            );
            expect(Mozilla.FirefoxDownloader.onError).toHaveBeenCalledWith(
                error
            );
        });
    });

    describe('setDownloadButtonAndroid', function () {
        const product = {
            id: 'android_release',
            label: 'Firefox Android'
        };

        const platform = {
            id: 'android',
            label: 'Android'
        };

        const language = {
            id: 'all',
            label: 'Multiple languages'
        };

        const options = `<div class="c-selection-options" data-product="android_release">
                <p class="c-selection c-selection-version hidden">
                    <label for="select_android_release_version" class="c-selection-label">Which version would you like?</label>
                    <select id="select_android_release_version" class="c-selection-input" aria-controls="download-info">
                        <option value="android_release"></option>
                    </select>
                </p>
                <p class="c-selection c-selection-platform">
                    <label for="select_android_release_platform" class="c-selection-label">Select your preferred installer</label>
                    <a href="#installer-help" class="c-button-help icon-installer-help" title="Learn about installers">
                        Get help
                    </a>
                    <select id="select_android_release_platform" class="c-selection-input" aria-controls="download-info">
                        <option value="android">Android</option>
                    </select>
                </p>
                <p class="c-selection c-selection-language">
                    <label for="select_android_release_language" class="c-selection-label">Select your preferred language</label>
                    <select id="select_android_release_language" class="c-selection-input" aria-controls="download-info">
                        <option value="all">Multiple languages</option>
                    </select>
                </p>
            </div>
            <ol class="c-locale-list" data-product="android_release">
                <li class="c-locale-list-item" data-language="multi">
                    <h4 class="c-locale-label">Multiple languages</h4>
                    <ul class="c-download-list">
                        <li>
                            <a id="playStoreLink-list" rel="external" href="https://app.adjust.com/2uo1qc?redirect=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dorg.mozilla.firefox&amp;campaign=www.mozilla.org&amp;adgroup=all-page" data-link-type="download" data-download-os="Android" data-mozillaonline-link="https://play.google.com/store/apps/details?id=cn.mozilla.firefox&amp;referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org">
                                Google Play
                            </a>
                        </li>
                        <li><a href="/en-US/firefox/mobile/get-app/" class="c-get-app" data-cta-type="link" data-cta-text="Get It Now" data-cta-position="banner">Send a download link to your phone</a></li>
                    </ul>
                </li>
            </ol>`;

        beforeEach(function () {
            document.body.insertAdjacentHTML('beforeend', options);
        });

        afterEach(function () {
            document.querySelector('.c-selection-options').remove();
            document.querySelector('.c-locale-list').remove();
        });

        it('should set the download link as expected', function () {
            spyOn(
                Mozilla.FirefoxDownloader,
                'getProductSelection'
            ).and.returnValue(product);
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadLink');
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadInfo');
            spyOn(Mozilla.FirefoxDownloader, 'offError');
            Mozilla.FirefoxDownloader.setDownloadButton();
            expect(
                Mozilla.FirefoxDownloader.setDownloadLink
            ).not.toHaveBeenCalled();
            expect(
                Mozilla.FirefoxDownloader.setDownloadInfo
            ).toHaveBeenCalledWith(
                product.label,
                platform.label,
                language.label
            );
            expect(Mozilla.FirefoxDownloader.offError).toHaveBeenCalled();
        });
    });

    describe('getProductSelection', function () {
        it('should return the selected product', function () {
            const product = {
                id: 'desktop_esr',
                label: 'Firefox Extended Support Release'
            };

            spyOn(Mozilla.FirefoxDownloader, 'getSelectOption').and.returnValue(
                product
            );
            spyOn(Mozilla.FirefoxDownloader, 'getFormSelection');
            expect(Mozilla.FirefoxDownloader.getProductSelection()).toEqual(
                product
            );
        });

        it('should return the correct ESR product', function () {
            const next = 'desktop_esr_next';
            const product = {
                id: 'desktop_esr',
                label: 'Firefox Extended Support Release'
            };

            spyOn(Mozilla.FirefoxDownloader, 'getSelectOption').and.returnValue(
                product
            );
            spyOn(
                Mozilla.FirefoxDownloader,
                'getFormSelection'
            ).and.returnValue(next);
            const result = Mozilla.FirefoxDownloader.getProductSelection();
            expect(result.id).toEqual(next);
            expect(result.label).toEqual(product.label);
        });
    });

    describe('onVersionChange', function () {
        it('should update the form fields and generate a download URL', function () {
            const e = {
                target: {
                    value: 'desktop_release'
                }
            };

            spyOn(Mozilla.FirefoxDownloader, 'setFormSelection');
            spyOn(Mozilla.FirefoxDownloader, 'setAllSelectOptions');
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadButton');

            Mozilla.FirefoxDownloader.onVersionChange(e);
            expect(
                Mozilla.FirefoxDownloader.setFormSelection
            ).not.toHaveBeenCalled();
            expect(
                Mozilla.FirefoxDownloader.setAllSelectOptions
            ).toHaveBeenCalledWith(e.target.value, jasmine.any(Object));
            expect(
                Mozilla.FirefoxDownloader.setDownloadButton
            ).toHaveBeenCalled();
        });

        it('should update the product selection for ESR', function () {
            const e = {
                target: {
                    value: 'desktop_esr_next'
                }
            };

            spyOn(Mozilla.FirefoxDownloader, 'setFormSelection');
            spyOn(Mozilla.FirefoxDownloader, 'setAllSelectOptions');
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadButton');

            Mozilla.FirefoxDownloader.onVersionChange(e);
            expect(
                Mozilla.FirefoxDownloader.setFormSelection
            ).toHaveBeenCalledWith(e.target.value);
        });
    });

    describe('getHash', function () {
        it('should return a product id if a valid hash identifier exists', function () {
            expect(
                Mozilla.FirefoxDownloader.getHash('#product-desktop-release')
            ).toEqual('desktop_release');
            expect(
                Mozilla.FirefoxDownloader.getHash('#product-desktop-beta')
            ).toEqual('desktop_beta');
            expect(
                Mozilla.FirefoxDownloader.getHash('#product-desktop-developer')
            ).toEqual('desktop_developer');
            expect(
                Mozilla.FirefoxDownloader.getHash('#product-desktop-nightly')
            ).toEqual('desktop_nightly');
            expect(
                Mozilla.FirefoxDownloader.getHash('#product-desktop-esr')
            ).toEqual('desktop_esr');
            expect(
                Mozilla.FirefoxDownloader.getHash('#product-android-release')
            ).toEqual('android_release');
            expect(
                Mozilla.FirefoxDownloader.getHash('#product-android-beta')
            ).toEqual('android_beta');
            expect(
                Mozilla.FirefoxDownloader.getHash('#product-android-nightly')
            ).toEqual('android_nightly');
            expect(
                Mozilla.FirefoxDownloader.getHash('#product-ios-release')
            ).toEqual('ios_release');
        });

        it('should return null if the hash identifier does not map to a valid product id', function () {
            expect(
                Mozilla.FirefoxDownloader.getHash('#product-firefox-fortress')
            ).toEqual(null);
        });
    });

    describe('setHash', function () {
        it('should set a hash identifier when passed a product id', function () {
            expect(
                Mozilla.FirefoxDownloader.setHash('desktop_nightly_dude')
            ).toEqual('#product-desktop-nightly-dude');
        });
    });

    describe('onHashChange', function () {
        it('should update the product selection if a valid hash identifier exists', function () {
            const id = 'firefox_beta';
            spyOn(Mozilla.FirefoxDownloader, 'getHash').and.returnValue(id);
            spyOn(Mozilla.FirefoxDownloader, 'setProductSelection');
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadButton');

            Mozilla.FirefoxDownloader.onHashChange();
            expect(
                Mozilla.FirefoxDownloader.setProductSelection
            ).toHaveBeenCalledWith(id);
            expect(
                Mozilla.FirefoxDownloader.setDownloadButton
            ).toHaveBeenCalled();
        });

        it('should not update the product selection if a hash identifier is invalid', function () {
            spyOn(Mozilla.FirefoxDownloader, 'getHash').and.returnValue(null);
            spyOn(Mozilla.FirefoxDownloader, 'setProductSelection');
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadButton');

            Mozilla.FirefoxDownloader.onHashChange();
            expect(
                Mozilla.FirefoxDownloader.setProductSelection
            ).not.toHaveBeenCalled();
            expect(
                Mozilla.FirefoxDownloader.setDownloadButton
            ).not.toHaveBeenCalled();
        });
    });

    describe('init', function () {
        const platform = 'windows';
        const language = 'de';
        const product = {
            id: 'desktop_beta',
            label: 'Firefox Beta'
        };

        beforeEach(function () {
            spyOn(Mozilla.FirefoxDownloader, 'setHash');
            spyOn(Mozilla.FirefoxDownloader, 'setFormSelection');
            spyOn(Mozilla.FirefoxDownloader, 'setAllSelectOptions');
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadButton');
            spyOn(Mozilla.FirefoxDownloader, 'enableForm');
        });

        it('should initialize the form as expected', function () {
            spyOn(Mozilla.FirefoxDownloader, 'getHash').and.returnValue(false);
            spyOn(Mozilla.FirefoxDownloader, 'getPageLanguage').and.returnValue(
                language
            );
            spyOn(
                Mozilla.FirefoxDownloader,
                'getProductSelection'
            ).and.returnValue(product);
            spyOn(Mozilla.FirefoxDownloader, 'getPlatform').and.returnValue(
                platform
            );

            Mozilla.FirefoxDownloader.init();
            expect(
                Mozilla.FirefoxDownloader.setAllSelectOptions
            ).toHaveBeenCalledTimes(2);
            expect(
                Mozilla.FirefoxDownloader.setDownloadButton
            ).toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.enableForm).toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.setHash).toHaveBeenCalled();
        });

        it('should update the product selection of a hash identifier exists', function () {
            spyOn(Mozilla.FirefoxDownloader, 'getHash').and.returnValue(
                'desktop_beta'
            );
            spyOn(Mozilla.FirefoxDownloader, 'getPageLanguage').and.returnValue(
                language
            );
            spyOn(
                Mozilla.FirefoxDownloader,
                'getProductSelection'
            ).and.returnValue(product);
            spyOn(Mozilla.FirefoxDownloader, 'getPlatform').and.returnValue(
                platform
            );
            spyOn(Mozilla.FirefoxDownloader, 'setProductSelection');

            Mozilla.FirefoxDownloader.init();
            expect(
                Mozilla.FirefoxDownloader.setProductSelection
            ).toHaveBeenCalledWith('desktop_beta');
        });

        it('should error if product or language cannot be determined', function () {
            spyOn(Mozilla.FirefoxDownloader, 'getHash').and.returnValue(false);
            spyOn(Mozilla.FirefoxDownloader, 'getPageLanguage').and.returnValue(
                false
            );
            spyOn(
                Mozilla.FirefoxDownloader,
                'getProductSelection'
            ).and.returnValue({
                id: undefined,
                label: undefined
            });
            spyOn(Mozilla.FirefoxDownloader, 'getPlatform');
            spyOn(Mozilla.FirefoxDownloader, 'onError');

            Mozilla.FirefoxDownloader.init();
            expect(
                Mozilla.FirefoxDownloader.setAllSelectOptions
            ).not.toHaveBeenCalled();
            expect(
                Mozilla.FirefoxDownloader.setDownloadButton
            ).not.toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.enableForm).not.toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.setHash).not.toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.onError).toHaveBeenCalled();
        });
    });
});
