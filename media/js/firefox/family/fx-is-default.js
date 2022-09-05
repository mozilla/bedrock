/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    // copy/pasted from thanks.js
    function isDefaultBrowser() {
        return new window.Promise(function (resolve, reject) {
            Mozilla.UITour.getConfiguration('appinfo', function (details) {
                if (details.defaultBrowser) {
                    resolve();
                } else {
                    reject();
                }
            });
        });
    }

    function isSupported() {
        return Mozilla.Client.isFirefoxDesktop && 'Promise' in window;
    }

    function onLoad() {
        if (!isSupported()) {
            return;
        }

        /**
         * Check to see if Firefox is the default browser.
         * If true, add class to main
         */
        isDefaultBrowser().then(function () {
            document.querySelector('main').classList.add('is-firefox-default');
        });
    }

    Mozilla.run(onLoad);
})(window.Mozilla);
