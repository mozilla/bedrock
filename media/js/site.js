/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
(function () {
    'use strict';
    function getPlatform() {
        if (navigator.platform.indexOf("Win32") !== -1 ||
                navigator.platform.indexOf("Win64") !== -1) {
            return 'windows';
        }
        if (navigator.platform.indexOf("armv7l") !== -1) {
            return 'android';
        }
        if (navigator.platform.indexOf("Linux") !== -1) {
            return 'linux';
        }
        if (navigator.platform.indexOf("MacPPC") !== -1) {
            return 'oldmac';
        }
        if (/Mac OS X 10.[0-5]/.test(navigator.userAgent)) {
            return 'oldmac';
        }
        if (navigator.userAgent.indexOf("Mac OS X") !== -1) {
            return 'osx';
        }
        if (navigator.userAgent.indexOf("MSIE 5.2") !== -1) {
            return 'oldmac';
        }
        if (navigator.platform.indexOf("Mac") !== -1) {
            return 'oldmac';
        }
        return 'other';
    }
    (function () {
        // if other than 'windows', immediately replace the platform classname on the html-element
        // to avoid lots of flickering
        var h = document.documentElement;
        window.site = {
            platform : getPlatform()
        };
        if (window.site.platform !== 'windows') {
            h.className = h.className.replace("windows", window.site.platform);
        }
        // Add class to reflect javascript availability for CSS
        h.className = h.className.replace(/\bno-js\b/, 'js');
    })();
})();