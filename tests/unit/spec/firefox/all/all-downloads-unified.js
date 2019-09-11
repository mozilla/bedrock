/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* eslint camelcase: [2, {properties: "never"}] */
/* eslint new-cap: [2, {"capIsNewExceptions": ["Deferred"]}] */

describe('all-downloads-unified.js', function() {
    'use strict';

    describe('getSelectOption', function() {
        var select = [
            '<select id="select-product" class="c-selection-input">' +
                '<option value="desktop_developer">Firefox Developer Edition</option>' +
                '<option value="desktop_nightly" selected>Firefox Nightly</option>' +
            '</select>'
        ].join();

        beforeEach(function () {
            document.body.insertAdjacentHTML('beforeend', select);
        });

        afterEach(function () {
            document.getElementById('select-product').remove();
        });

        it('should return the selection option', function() {
            var el = document.getElementById('select-product');
            var result = Mozilla.FirefoxDownloader.getSelectOption(el);
            expect(result.id).toEqual('desktop_nightly');
            expect(result.label).toEqual('Firefox Nightly');
        });
    });

    describe('setAllSelectOptions', function() {
        var select = [
            '<select id="select_desktop_release_platform" class="c-selection-input">' +
                '<option value="win64">Windows 64-bit</option>' +
                '<option value="osx" selected>macOS</option>' +
                '<option value="linux64">Linux 64-bit</option>' +
                '<option value="win">Windows 32-bit</option>' +
                '<option value="linux">Linux 32-bit</option>' +
            '</select>' +
            '<select id="select_desktop_beta_platform" class="c-selection-input">' +
                '<option value="win64">Windows 64-bit</option>' +
                '<option value="osx" selected>macOS</option>' +
                '<option value="linux64">Linux 64-bit</option>' +
                '<option value="win">Windows 32-bit</option>' +
                '<option value="linux">Linux 32-bit</option>' +
            '</select>'
        ].join();

        beforeEach(function () {
            document.body.insertAdjacentHTML('beforeend', select);
        });

        afterEach(function () {
            document.getElementById('select_desktop_release_platform').remove();
            document.getElementById('select_desktop_beta_platform').remove();
        });

        it('should set all the options correctly', function() {
            var el = document.querySelectorAll('.c-selection-input');
            Mozilla.FirefoxDownloader.setAllSelectOptions('linux', el);
            var result = Mozilla.FirefoxDownloader.getSelectOption(el[0]);
            expect(result.id).toEqual('linux');
            expect(result.label).toEqual('Linux 32-bit');
            var result2 = Mozilla.FirefoxDownloader.getSelectOption(el[1]);
            expect(result2.id).toEqual('linux');
            expect(result2.label).toEqual('Linux 32-bit');
        });
    });

    describe('getPlatform', function() {
        it('should return known platforms', function() {
            expect(Mozilla.FirefoxDownloader.getPlatform('windows')).toEqual('win64');
            expect(Mozilla.FirefoxDownloader.getPlatform('linux')).toEqual('linux64');
            expect(Mozilla.FirefoxDownloader.getPlatform('osx')).toEqual('osx');
        });

        it('should return false for unknown platforms', function() {
            expect(Mozilla.FirefoxDownloader.getPlatform('other')).toBeFalsy();
        });
    });

    describe('getPageLanguage', function() {
        it('should return en-US for region neutral en values', function() {
            expect(Mozilla.FirefoxDownloader.getPageLanguage('en')).toEqual('en-US');
        });
    });

    describe('getDownloadLink', function() {
        var downloadList = [
            '<ol class="c-locale-list" data-product="desktop_release">' +
                '<li class="c-locale-list-item" data-language="ach">' +
                    '<ul class="c-download-list">' +
                        '<li>' +
                            '<a href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win64&amp;lang=ach" data-download-version="win64">Windows 64-bit</a>' +
                        '</li>' +
                    '</ul>' +
                '</li>' +
            '</ol>'
        ].join();

        beforeEach(function () {
            document.body.insertAdjacentHTML('beforeend', downloadList);
        });

        afterEach(function () {
            document.querySelector('.c-locale-list').remove();
        });

        it('should return a download link as expected', function() {
            var result = Mozilla.FirefoxDownloader.getDownloadLink('desktop_release', 'win64', 'ach');
            expect(result).toEqual('https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=ach');
        });

        it('should return an error if a download link is not found', function() {
            var result = Mozilla.FirefoxDownloader.getDownloadLink('desktop_release', 'win64', 'de');
            expect(result instanceof Error).toBeTruthy();
        });
    });

    describe('setDownloadLink', function() {
        var downloadLink = '<a href="#" id="download-button-primary">Download Now</a>';

        beforeEach(function () {
            document.body.insertAdjacentHTML('beforeend', downloadLink);
        });

        afterEach(function () {
            document.getElementById('download-button-primary').remove();
        });

        it('should set desktop download links as expected', function() {
            var el = document.getElementById('download-button-primary');
            var url = 'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=ach';

            var product = {
                id: 'desktop_beta',
                label: 'Firefox Beta'
            };

            var platform = {
                id: 'win64',
                label: 'Windows 64-bit'
            };

            var language = {
                id: 'ach',
                label: 'Acholi'
            };

            Mozilla.FirefoxDownloader.setDownloadLink(url, product, platform, language, el);
            expect(el.href).toEqual(url);
            expect(el.getAttribute('data-display-name')).toEqual(product.label);
            expect(el.getAttribute('data-download-version')).toEqual(platform.id);
            expect(el.getAttribute('data-download-language')).toEqual(language.id);
            expect(el.getAttribute('data-download-os')).toEqual('Desktop');
        });

        it('should set android download links as expected', function() {
            var el = document.getElementById('download-button-primary');
            var url = 'https://download.mozilla.org/?product=fennec-latest&os=android&lang=multi';

            var product = {
                id: 'android_release',
                label: 'Firefox Android'
            };

            var platform = {
                id: 'android',
                label: 'ARM devices (Android 4.1+)'
            };

            var language = {
                id: 'multi',
                label: 'Multi-locale'
            };

            Mozilla.FirefoxDownloader.setDownloadLink(url, product, platform, language, el);
            expect(el.href).toEqual(url);
            expect(el.getAttribute('data-display-name')).toEqual(product.label);
            expect(el.getAttribute('data-download-version')).toEqual(platform.id);
            expect(el.getAttribute('data-download-language')).toEqual(language.id);
            expect(el.getAttribute('data-download-os')).toEqual('Android');
        });
    });

    describe('isValidURL', function() {
        it('should return true for bouncer links', function() {
            var url = 'https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US';
            expect(Mozilla.FirefoxDownloader.isValidURL(url)).toBeTruthy();
        });

        it('should return false for everything else', function() {
            var url = 'https://some.other.domain/?product=firefox-latest-ssl&os=osx&lang=en-US';
            expect(Mozilla.FirefoxDownloader.isValidURL(url)).toBeFalsy();
            expect(Mozilla.FirefoxDownloader.isValidURL(null)).toBeFalsy();
            expect(Mozilla.FirefoxDownloader.isValidURL({})).toBeFalsy();
        });
    });

    describe('generateDownloadURL', function() {
        var product = {
            id: 'desktop_beta',
            label: 'Firefox Beta'
        };

        var platform = {
            id: 'win64',
            label: 'Windows 64-bit'
        };

        var language = {
            id: 'ach',
            label: 'Acholi'
        };

        var options = [
            '<div class="c-selection-options" data-product="desktop_beta">' +
                '<p class="c-selection c-selection-version">' +
                    '<label for="select_desktop_beta_version" class="c-selection-label">Which version would you like?</label>' +
                    '<select id="select_desktop_beta_version" class="c-selection-input">' +
                        '<option value="desktop_beta">67.0b19</option>' +
                    '</select>' +
                '</p>' +
                '<p class="c-selection c-selection-platform">' +
                    '<label for="select_desktop_beta_platform" class="c-selection-label">Which operating system are you using?</label>' +
                    '<select id="select_desktop_beta_platform" class="c-selection-input">' +
                        '<option value="win64">Windows 64-bit</option>' +
                    '</select>' +
                '</p>' +
                '<p class="c-selection c-selection-language">' +
                    '<label for="select_desktop_beta_language" class="c-selection-label">Would you like to select a different language?</label>' +
                    '<select id="select_desktop_beta_language" class="c-selection-input disabled">' +
                        '<option value="ach">Acholi</option>' +
                    '</select>' +
                '</p>' +
            '</div>' +
            '<ol class="c-locale-list" data-product="desktop_beta">' +
                '<li class="c-locale-list-item" data-language="ach">' +
                    '<ul class="c-download-list">' +
                        '<li>' +
                            '<a href="https://download.mozilla.org/?product=firefox-beta-latest-ssl&amp;os=win64&amp;lang=ach" data-download-version="win64">Windows 64-bit</a>' +
                        '</li>' +
                    '</ul>' +
                '</li>' +
            '</ol>'
        ].join();

        beforeEach(function () {
            document.body.insertAdjacentHTML('beforeend', options);
        });

        afterEach(function () {
            document.querySelector('.c-selection-options').remove();
            document.querySelector('.c-locale-list').remove();
        });

        it('should set the download link as expected', function() {
            spyOn(Mozilla.FirefoxDownloader, 'getProductSelection').and.returnValue(product);
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadLink');
            spyOn(Mozilla.FirefoxDownloader, 'setDownloadInfo');
            spyOn(Mozilla.FirefoxDownloader, 'offError');
            Mozilla.FirefoxDownloader.generateDownloadURL();
            expect(Mozilla.FirefoxDownloader.setDownloadLink).toHaveBeenCalledWith('https://download.mozilla.org/?product=firefox-beta-latest-ssl&os=win64&lang=ach', product, platform, language);
            expect(Mozilla.FirefoxDownloader.setDownloadInfo).toHaveBeenCalledWith(product.label, platform.label, language.label);
            expect(Mozilla.FirefoxDownloader.offError).toHaveBeenCalled();
        });

    });

    describe('getProductSelection', function() {
        it('should return the selected product', function() {
            var product = {
                id: 'desktop_esr',
                label: 'Firefox Extended Support Release'
            };

            spyOn(Mozilla.FirefoxDownloader, 'getSelectOption').and.returnValue(product);
            spyOn(Mozilla.FirefoxDownloader, 'getFormSelection');
            expect(Mozilla.FirefoxDownloader.getProductSelection()).toEqual(product);
        });

        it('should return the correct ESR product', function() {
            var next = 'desktop_esr_next';
            var product = {
                id: 'desktop_esr',
                label: 'Firefox Extended Support Release'
            };

            spyOn(Mozilla.FirefoxDownloader, 'getSelectOption').and.returnValue(product);
            spyOn(Mozilla.FirefoxDownloader, 'getFormSelection').and.returnValue(next);
            var result = Mozilla.FirefoxDownloader.getProductSelection();
            expect(result.id).toEqual(next);
            expect(result.label).toEqual(product.label);
        });
    });

    describe('onVersionChange', function() {
        it('should update the form fields and generate a download URL', function() {
            var e = {
                target: {
                    value: 'desktop_release'
                }
            };

            spyOn(Mozilla.FirefoxDownloader, 'setFormSelection');
            spyOn(Mozilla.FirefoxDownloader, 'setAllSelectOptions');
            spyOn(Mozilla.FirefoxDownloader, 'generateDownloadURL');

            Mozilla.FirefoxDownloader.onVersionChange(e);
            expect(Mozilla.FirefoxDownloader.setFormSelection).not.toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.setAllSelectOptions).toHaveBeenCalledWith(e.target.value, jasmine.any(Object));
            expect(Mozilla.FirefoxDownloader.generateDownloadURL).toHaveBeenCalled();
        });

        it('should update the product selection for ESR', function() {
            var e = {
                target: {
                    value: 'desktop_esr_next'
                }
            };

            spyOn(Mozilla.FirefoxDownloader, 'setFormSelection');
            spyOn(Mozilla.FirefoxDownloader, 'setAllSelectOptions');
            spyOn(Mozilla.FirefoxDownloader, 'generateDownloadURL');

            Mozilla.FirefoxDownloader.onVersionChange(e);
            expect(Mozilla.FirefoxDownloader.setFormSelection).toHaveBeenCalledWith(e.target.value);
        });
    });

    describe('getHash', function() {
        it('should return a product id if a valid hash identifier exists', function() {
            expect(Mozilla.FirefoxDownloader.getHash('#product-desktop-release')).toEqual('desktop_release');
            expect(Mozilla.FirefoxDownloader.getHash('#product-desktop-beta')).toEqual('desktop_beta');
            expect(Mozilla.FirefoxDownloader.getHash('#product-desktop-developer')).toEqual('desktop_developer');
            expect(Mozilla.FirefoxDownloader.getHash('#product-desktop-nightly')).toEqual('desktop_nightly');
            expect(Mozilla.FirefoxDownloader.getHash('#product-desktop-esr')).toEqual('desktop_esr');
            expect(Mozilla.FirefoxDownloader.getHash('#product-android-release')).toEqual('android_release');
            expect(Mozilla.FirefoxDownloader.getHash('#product-android-beta')).toEqual('android_beta');
            expect(Mozilla.FirefoxDownloader.getHash('#product-android-nightly')).toEqual('android_nightly');
        });

        it('should return null if the hash identifier does not map to a valid product id', function() {
            expect(Mozilla.FirefoxDownloader.getHash('#product-firefox-fortress')).toEqual(null);
        });
    });

    describe('setHash', function() {
        it('should set a hash identifier when passed a product id', function() {
            expect(Mozilla.FirefoxDownloader.setHash('desktop_nightly_dude')).toEqual('#product-desktop-nightly-dude');
        });
    });

    describe('onHashChange', function() {
        it('should update the product selection if a valid hash identifier exists', function() {
            var id = 'firefox_beta';
            spyOn(Mozilla.FirefoxDownloader, 'getHash').and.returnValue(id);
            spyOn(Mozilla.FirefoxDownloader, 'setProductSelection');
            spyOn(Mozilla.FirefoxDownloader, 'generateDownloadURL');

            Mozilla.FirefoxDownloader.onHashChange();
            expect(Mozilla.FirefoxDownloader.setProductSelection).toHaveBeenCalledWith(id);
            expect(Mozilla.FirefoxDownloader.generateDownloadURL).toHaveBeenCalled();
        });

        it('should not update the product selection if a hash identifier is invalid', function() {
            spyOn(Mozilla.FirefoxDownloader, 'getHash').and.returnValue(null);
            spyOn(Mozilla.FirefoxDownloader, 'setProductSelection');
            spyOn(Mozilla.FirefoxDownloader, 'generateDownloadURL');

            Mozilla.FirefoxDownloader.onHashChange();
            expect(Mozilla.FirefoxDownloader.setProductSelection).not.toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.generateDownloadURL).not.toHaveBeenCalled();
        });
    });

    describe('init', function() {
        var platform = 'windows';
        var language = 'de';
        var product = {
            'id': 'desktop_beta',
            'label': 'Firefox Beta'
        };

        beforeEach(function() {
            spyOn(Mozilla.FirefoxDownloader, 'setHash');
            spyOn(Mozilla.FirefoxDownloader, 'setFormSelection');
            spyOn(Mozilla.FirefoxDownloader, 'setAllSelectOptions');
            spyOn(Mozilla.FirefoxDownloader, 'generateDownloadURL');
            spyOn(Mozilla.FirefoxDownloader, 'enableForm');
        });

        it('should initialize the form as expected', function() {
            spyOn(Mozilla.FirefoxDownloader, 'getHash').and.returnValue(false);
            spyOn(Mozilla.FirefoxDownloader, 'getPageLanguage').and.returnValue(language);
            spyOn(Mozilla.FirefoxDownloader, 'getProductSelection').and.returnValue(product);
            spyOn(Mozilla.FirefoxDownloader, 'getPlatform').and.returnValue(platform);

            Mozilla.FirefoxDownloader.init();
            expect(Mozilla.FirefoxDownloader.setAllSelectOptions).toHaveBeenCalledTimes(2);
            expect(Mozilla.FirefoxDownloader.generateDownloadURL).toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.enableForm).toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.setHash).toHaveBeenCalled();
        });

        it('should update the product selection of a hash identifier exists', function() {
            spyOn(Mozilla.FirefoxDownloader, 'getHash').and.returnValue('desktop_beta');
            spyOn(Mozilla.FirefoxDownloader, 'getPageLanguage').and.returnValue(language);
            spyOn(Mozilla.FirefoxDownloader, 'getProductSelection').and.returnValue(product);
            spyOn(Mozilla.FirefoxDownloader, 'getPlatform').and.returnValue(platform);
            spyOn(Mozilla.FirefoxDownloader, 'setProductSelection');

            Mozilla.FirefoxDownloader.init();
            expect(Mozilla.FirefoxDownloader.setProductSelection).toHaveBeenCalledWith('desktop_beta');
        });

        it('should error if product or language cannot be determined', function() {
            spyOn(Mozilla.FirefoxDownloader, 'getHash').and.returnValue(false);
            spyOn(Mozilla.FirefoxDownloader, 'getPageLanguage').and.returnValue(false);
            spyOn(Mozilla.FirefoxDownloader, 'getProductSelection').and.returnValue({
                'id': undefined,
                'label': undefined
            });
            spyOn(Mozilla.FirefoxDownloader, 'getPlatform');
            spyOn(Mozilla.FirefoxDownloader, 'onError');

            Mozilla.FirefoxDownloader.init();
            expect(Mozilla.FirefoxDownloader.setAllSelectOptions).not.toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.generateDownloadURL).not.toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.enableForm).not.toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.setHash).not.toHaveBeenCalled();
            expect(Mozilla.FirefoxDownloader.onError).toHaveBeenCalled();
        });
    });
});
