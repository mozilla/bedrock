/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function (Mozilla) {
    'use strict';

    var DownloadThanks = {};

    /**
     * Determine if browser should attempt to download Firefox on page load.
     * @param {String} platform
     * @param {Boolean} fxSupported
     * @returns {Boolean}
     */
    DownloadThanks.shouldAutoDownload = function (platform, fxSupported) {
        var supportedPlatforms = ['windows', 'osx', 'android', 'ios'];

        if (fxSupported && supportedPlatforms.indexOf(platform) !== -1) {
            return true;
        }

        return false;
    };

    /**
     * Get the Firefox download link for the appropriate platform.
     * @param {Object} window.site
     * @returns {String} download url
     */
    DownloadThanks.getDownloadURL = function (site) {
        var prefix = 'thanks-download-button-';
        var link;
        var url;

        switch (site.platform) {
            case 'windows':
                link = document.getElementById(prefix + 'win');
                break;
            case 'osx':
                link = document.getElementById(prefix + 'osx');
                break;
            case 'linux':
                // Linux users get SUMO install instructions.
                link = null;
                break;
            case 'android':
                link = document.getElementById(prefix + 'android');
                break;
            case 'ios':
                link = document.getElementById(prefix + 'ios');
                break;
        }

        if (link && link.href) {
            url = link.href;
        }

        return url;
    };

    Mozilla.DownloadThanks = DownloadThanks;
})(window.Mozilla);
