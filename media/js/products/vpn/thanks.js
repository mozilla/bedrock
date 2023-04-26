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
     * Determine if browser should attempt to download Mozilla VPN on page load.
     * @param {String} platform
     * @returns {Boolean}
     */
    DownloadThanks.shouldAutoDownload = function (platform) {
        var supportedPlatforms = ['windows', 'osx'];

        if (supportedPlatforms.indexOf(platform) !== -1) {
            return true;
        }

        return false;
    };

    /**
     * Get the VPN download link for the appropriate platform.
     * @param {Object} window.site
     * @returns {String} download url
     */
    DownloadThanks.getDownloadURL = function (site) {
        var prefix = 'vpn-download-link-';
        var link;
        var url;

        switch (site.platform) {
            case 'windows':
                link = document.getElementById(prefix + 'win');
                break;
            case 'osx':
                link = document.getElementById(prefix + 'mac');
                break;
        }

        if (link && link.href) {
            url = link.href;
        }

        return url;
    };

    Mozilla.DownloadThanks = DownloadThanks;
})(window.Mozilla);
