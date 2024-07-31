/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function () {
    'use strict';

    var Utils = {};

    // Vanilla JS DOM Ready handler
    Utils.onDocumentReady = function (callback) {
        if (document.readyState !== 'loading') {
            callback();
        } else {
            document.addEventListener('DOMContentLoaded', callback, false);
        }
    };

    /**
     * Get platform version for download_firefox_thanks() buttons.
     * @param {Object} window.site
     * @returns {Object} version
     */
    Utils.getDownloadPlatformVersion = function (site) {
        var data = {};
        var platform = site.platform;

        switch (platform) {
            case 'windows':
                data.version = 'win';
                break;
            case 'osx':
                data.version = 'osx';
                break;
            case 'linux':
                data.version = site.archSize === 64 ? 'linux64' : 'linux';
                break;
            case 'ios':
                data.version = 'ios';
                break;
            case 'android':
                data.version = 'android';
                break;
            default:
                data.version = 'unsupported';
        }

        return data;
    };

    /**
     * Set stub attribution data attributes for download_firefox_thanks() buttons.
     */
    Utils.attributeDownloadThanksButton = function () {
        var downloadButton = document.querySelectorAll(
            '.c-button-download-thanks > .download-link'
        );
        var data = Utils.getDownloadPlatformVersion(window.site);

        for (var i = 0; i < downloadButton.length; ++i) {
            if (data && data.version) {
                downloadButton[i].setAttribute(
                    'data-download-version',
                    data.version
                );
            }
        }
    };

    // Replace Google Play links on Android devices to let them open the marketplace app
    Utils.initMobileDownloadLinks = function () {
        if (site.platform === 'android') {
            var playLinks = document.querySelectorAll(
                'a[href^="https://play.google.com/store/apps/"]'
            );
            for (var i = 0; i < playLinks.length; ++i) {
                var playLink = playLinks[i];
                var oldHref = playLink.getAttribute('href');
                var newHref = oldHref.replace(
                    'https://play.google.com/store/apps/',
                    'market://'
                );
                playLink.setAttribute('href', newHref);
            }
        }
    };

    // client-side redirects (handy for testing)
    Utils.doRedirect = function (destination) {
        if (destination) {
            window.location.href = destination;
        }
    };

    // Create text translation function using #strings element.
    // TODO: Move to docs
    // In order to use it, you need a block string_data bit inside your template,
    // then, each key name needs to be preceded by data- as this uses data attributes
    // to work. After this, you can access all strings defined inside the
    // string_data block in JS using Mozilla.Utils.trans('key-of-string'); Thank @mkelly
    Utils.trans = function (stringId) {
        var _strings = document.getElementById('strings');

        if (_strings) {
            return _strings.getAttribute('data-' + stringId);
        } else {
            return undefined;
        }
    };

    Utils.allowsMotion = function () {
        return (
            window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: no-preference)').matches
        );
    };

    window.Mozilla.Utils = Utils;
})();
