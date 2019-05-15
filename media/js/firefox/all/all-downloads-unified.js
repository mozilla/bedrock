/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(){
    'use strict';

    var form = document.getElementById('product-select-form');
    var productSelect = document.getElementById('select-product');
    var versionSelect = document.querySelectorAll('.c-selection-version select');
    var languageSelect = document.querySelectorAll('.c-selection-language select');
    var platformSelect = document.querySelectorAll('.c-selection-platform select');
    var downloadInfo = document.querySelector('.c-download');
    var downloadInfoProduct = document.getElementById('download-info-product');
    var downloadInfoPlatform = document.getElementById('download-info-platform');
    var downloadInfoLanguage = document.getElementById('download-info-language');
    var downloadInfoButton = document.getElementById('download-button-primary');

    var FirefoxDownloader = {};

    /**
     * Get the currently selected <option> from a given <select>.
     * @param {Object} el dom element.
     * @returns {Object} product `id` and `label`.
     */
    FirefoxDownloader.getSelectOption = function(el) {
        return {
            'id': el.options[el.selectedIndex].value,
            'label': el.options[el.selectedIndex].textContent
        };
    };

    /**
     * Set the <option> for a given <select> input.
     * @param {String} platform `id`.
     * @param {Object} NodeList of <option>'s.
     */
    FirefoxDownloader.setSelectOption = function(id, options) {
        for (var i = 0; i < options.length; i++) {
            if (options[i].value === id) {
                options[i].selected = 'selected';
                break;
            }
        }
    };

    /**
     * Set the <option> for a collection of <select> inputs.
     * @param {String} platform `id`.
     * @param {Object} el dom element(s).
     */
    FirefoxDownloader.setAllSelectOptions = function(id, el) {
        for (var i = 0; i < el.length; i++) {
            FirefoxDownloader.setSelectOption(id, el[i].options);
        }
    };

    /**
     * Set the currently selected product. The data-attribute on the <form> is
     * used to display the appropriate options for each individual product item.
     * @param {String} product `id`.
     */
    FirefoxDownloader.setProductSelection = function(id) {
        form.setAttribute('data-current', id);
    };

    /**
     * Get the currently selected product.
     * @returns {Object} product `id` and `label`.
     */
    FirefoxDownloader.getProductSelection = function() {
        return FirefoxDownloader.getSelectOption(productSelect);
    };

    /**
     * Get the currently selected ESR product.
     * @param {String} `product`.
     * @returns {Object} product `id` and `label`.
     */
    FirefoxDownloader.getVersionSelection = function(product) {
        var currentOptions = document.querySelector('.c-selection-options[data-product="' + product.id + '"]');
        var currentVersion = currentOptions.querySelector('.c-selection-version select');
        return FirefoxDownloader.getSelectOption(currentVersion);
    };

    /**
     * Get platform based on user agent via window.site.platform.
     * @param {String} platform.
     * @returns {String} OS.
     */
    FirefoxDownloader.getPlatform = function(platform) {
        var system;
        /**
         * Note: we can't accurately detect 64bit arch via user agent
         * alone, so we assume most people want the fastest version.
         */
        switch(platform) {
        case 'windows':
            system = 'win64';
            break;
        case 'linux':
            system = 'linux64';
            break;
        case 'osx':
            system = 'osx';
            break;
        default:
            system = false;
        }

        return system;
    };

    /**
     * Get the currently selected platform for a given product.
     * @param {String} `product`.
     * @returns {Object} platform `id` and platform `label`.
     */
    FirefoxDownloader.getPlatformSelection = function(product) {
        var currentOptions = document.querySelector('.c-selection-options[data-product="' + product.id + '"]');
        var currentPlatform = currentOptions.querySelector('.c-selection-platform select');
        return FirefoxDownloader.getSelectOption(currentPlatform);
    };

    /**
     * Get the currently selected language for a given product.
     * @param {String} `product`.
     * @returns {Object} language `id` and language `label`.
     */
    FirefoxDownloader.getLanguageSelection = function(product) {
        var currentOptions = document.querySelector('.c-selection-options[data-product="' + product.id + '"]');
        var currentLanguage = currentOptions.querySelector('.c-selection-language select');
        return FirefoxDownloader.getSelectOption(currentLanguage);
    };

    /**
     * Get the current language of the page.
     * @param {String} `localeCode` (optional).
     * @returns {String} page language.
     */
    FirefoxDownloader.getPageLanguage = function(localeCode) {
        var lang = localeCode || document.getElementsByTagName('html')[0].getAttribute('lang');

        if (lang) {
            // bedrock uses `en` for `en-US` pages to mark content as region neutral.
            lang = lang === 'en' ? 'en-US' : lang;
            return lang;
        }
        return false;
    };

    /**
     * Get the download link for a chosen product, platform and language.
     * @param {String} product id.
     * @param {String} platform id.
     * @param {String} language id.
     * @returns {String} download URL.
     */
    FirefoxDownloader.getDownloadLink = function(product, platform, language) {
        try {
            var productList = document.querySelector('.c-locale-list[data-product="' + product + '"]');
            var languageBuild = productList.querySelector('.c-locale-list-item[data-language="' + language + '"]');
            var platformLink = languageBuild.querySelector('.c-download-list > li > a[data-download-version="' + platform + '"]');

            if (platformLink) {
                return platformLink.href;
            } else {
                return new Error('platformLink is ' + platformLink);
            }
        } catch(e) {
            return e;
        }
    };

    /**
     * Set download button to a given url and update GTM attributes.
     * @param {String} url.
     * @param {Object} product.
     * @param {Object} platform.
     * @param {Object} language.
     * @param {Object} element (optional)
     */
    FirefoxDownloader.setDownloadLink = function(url, product, platform, language, element) {
        var el = element || downloadInfoButton;
        el.href = url;
        el.setAttribute('data-display-name', product.label);
        el.setAttribute('data-download-version', platform.id);
        el.setAttribute('data-download-language', language.id);

        if ((/^android/).test(platform.id)) {
            el.setAttribute('data-download-os', 'Android');
        } else {
            el.setAttribute('data-download-os', 'Desktop');
        }
    };

    /**
     * Display form error message and show fallback locale list.
     * @param {Object} instance of `Error`.
     */
    FirefoxDownloader.onError = function(e) {
        // show form error and hide download button.
        downloadInfo.classList.add('has-error');

        // show the fallback list of locales.
        document.getElementById('all-downloads').classList.add('is-fallback');

        if (e instanceof Error) {
            window.dataLayer.push({
                'event': 'in-page-interaction',
                'eAction': 'download error',
                'eLabel': e.name + e.message
            });
        }
    };

    /**
     * Removes error form state.
     */
    FirefoxDownloader.offError = function() {
        // Remove error message is previously shown.
        if (downloadInfo.classList.contains('has-error')) {
            downloadInfo.classList.remove('has-error');
        }
    };

    /**
     * Make sure download link is from a trusted domain.
     * @param {String} url.
     * @returns {Boolean}.
     */
    FirefoxDownloader.isValidURL = function(url) {
        var bouncerURL = /^https:\/\/download.mozilla.org/;
        return typeof url === 'string' && (bouncerURL).test(url);
    };

    /**
     * Generate the download URL for the form button, based on the current for selection.
     */
    FirefoxDownloader.generateDownloadURL = function() {
        var product = FirefoxDownloader.getProductSelection();
        var platform = FirefoxDownloader.getPlatformSelection(product);
        var language = FirefoxDownloader.getLanguageSelection(product);
        var version = FirefoxDownloader.getVersionSelection(product);

        // Use `version.id` as ESR can sometimes offer 2 builds simultaneously.
        var download = FirefoxDownloader.getDownloadLink(version.id, platform.id, language.id);

        if (FirefoxDownloader.isValidURL(download)) {
            FirefoxDownloader.setDownloadLink(download, product, platform, language);
            FirefoxDownloader.setDownloadInfo(product.label, platform.label, language.label);
            FirefoxDownloader.offError();
        } else {
            FirefoxDownloader.onError(download);
        }
    };

    /**
     * Set the form info for what the current selection will download.
     */
    FirefoxDownloader.setDownloadInfo = function(product, platform, language) {
        downloadInfoProduct.textContent = product;
        downloadInfoPlatform.textContent = platform;
        downloadInfoLanguage.textContent = language;
    };

    /**
     * Product input <select> handler.
     * @param {Object} event object.
     */
    FirefoxDownloader.onProductChange = function(e) {
        FirefoxDownloader.setProductSelection(e.target.value);
        FirefoxDownloader.generateDownloadURL();
    };

    /**
     * Product ESR input <select> handler.
     * @param {Object} event object.
     */
    FirefoxDownloader.onVersionChange = function() {
        FirefoxDownloader.generateDownloadURL();
    };

    /**
     * Platform input <select> handler.
     * @param {Object} event object.
     */
    FirefoxDownloader.onPlatformChange = function(e) {
        FirefoxDownloader.setAllSelectOptions(e.target.value, platformSelect);
        FirefoxDownloader.generateDownloadURL();
    };

    /**
     * Language input <select> handler.
     * @param {Object} event object.
     */
    FirefoxDownloader.onLanguageChange = function(e) {
        FirefoxDownloader.setAllSelectOptions(e.target.value, languageSelect);
        FirefoxDownloader.generateDownloadURL();
    };

    /**
     * Initializes form input element.
     * @param {Object} el.
     * @param {Function} callback.
     */
    FirefoxDownloader.initInput = function(el, callback) {
        if (typeof callback === 'function') {
            el.addEventListener('change', callback, false);
        }
        el.removeAttribute('disabled');
    };

    /**
     * Initializes a NodeList of form inputs.
     * @param {Object} el NodeList.
     * @param {Function} callback.
     */
    FirefoxDownloader.initAllInputs = function(el, callback) {
        for (var i = 0; i < el.length; i++) {
            FirefoxDownloader.initInput(el[i], callback);
        }
    };

    /**
     * Enable form inputs, bind event handlers, and show the product options.
     */
    FirefoxDownloader.enableForm = function() {
        FirefoxDownloader.initInput(productSelect, FirefoxDownloader.onProductChange);
        FirefoxDownloader.initAllInputs(platformSelect, FirefoxDownloader.onPlatformChange);
        FirefoxDownloader.initAllInputs(languageSelect, FirefoxDownloader.onLanguageChange);
        FirefoxDownloader.initAllInputs(versionSelect, FirefoxDownloader.onVersionChange);

        // show product options.
        downloadInfo.classList.remove('hidden');
    };

    /**
     * Basic feature detect for minimum browser support.
     */
    FirefoxDownloader.isSupported = function() {
        return 'querySelector' in document &&
               'querySelectorAll' in document &&
               'addEventListener' in window &&
               'classList' in document.createElement('div');
    };

    /**
     * Initialize the form and show the default selection.
     */
    FirefoxDownloader.init = function() {
        var pageLang = FirefoxDownloader.getPageLanguage();
        var product = FirefoxDownloader.getProductSelection();
        var platform = FirefoxDownloader.getPlatform(window.site.platform);

        if (platform) {
            FirefoxDownloader.setAllSelectOptions(platform, platformSelect);
        }

        if (pageLang && product.id && product.label) {
            FirefoxDownloader.setProductSelection(product.id);
            FirefoxDownloader.setAllSelectOptions(pageLang, languageSelect);
            FirefoxDownloader.generateDownloadURL();
            FirefoxDownloader.enableForm();
        } else {
            FirefoxDownloader.onError();
        }
    };

    window.Mozilla.FirefoxDownloader = FirefoxDownloader;

})();
