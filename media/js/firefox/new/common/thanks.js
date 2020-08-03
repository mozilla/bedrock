/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function(Mozilla) {
    'use strict';

    var DownloadThanks = {};

    /**
     * Determine if browser should attempt to download Firefox on page load.
     * @param {String} platform
     * @returns {Boolean}
     */
    DownloadThanks.shouldAutoDownload = function(platform) {
        var supportedPlatforms = ['windows', 'osx', 'linux', 'android', 'ios'];

        if (supportedPlatforms.indexOf(platform) !== -1) {
            return true;
        }

        return false;
    };

    /**
     * Get the Firefox download link for the appropriate platform.
     * @param {Object} window.site
     * @returns {String} download url
     */
    DownloadThanks.getDownloadURL = function(site) {
        var prefix = 'thanks-download-button-';
        var link;
        var url;

        switch(site.platform) {
        case 'windows':
            if (site.isARM) {
                // Detect ARM64 / AArch64 builds for Windows.
                link = document.getElementById(prefix + 'win64-aarch64');
            } else {
                link = document.getElementById(prefix + 'win');
            }
            break;
        case 'osx':
            link = document.getElementById(prefix + 'osx');
            break;
        case 'linux':
            if (site.isARM) {
                // Linux ARM users get SUMO install instructions.
                link = null;
            } else if (site.archSize === 64) {
                // Detect 64bit / 32bit builds for Linux.
                link = document.getElementById(prefix + 'linux64');
            } else {
                link = document.getElementById(prefix + 'linux');
            }

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
