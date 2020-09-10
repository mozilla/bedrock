/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';
    window.site = {
        getPlatform: function (ua, pf) {
            pf = pf || navigator.platform;
            ua = ua || navigator.userAgent;

            if (pf.indexOf('Win32') !== -1 ||
                pf.indexOf('Win64') !== -1) {
                return 'windows';
            }
            if (/android/i.test(ua)) {
                return 'android';
            }
            if (/linux/i.test(pf) || /linux/i.test(ua)) {
                return 'linux';
            }
            if (pf.indexOf('MacPPC') !== -1) {
                return 'other';
            }
            if (pf.indexOf('iPhone') !== -1 ||
                pf.indexOf('iPad') !== -1 ||
                pf.indexOf('iPod') !== -1 ||
                pf.indexOf('MacIntel') !== -1 && 'standalone' in navigator) { // iPadOS
                return 'ios';
            }
            if (ua.indexOf('Mac OS X') !== -1 && !/Mac OS X 10.[0-8]\D/.test(ua)) {
                return 'osx';
            }

            return 'other';
        },

        getPlatformVersion: function (ua) {
            ua = ua || navigator.userAgent;

            // On OS X, Safari and Chrome have underscores instead of dots
            var match = ua.match(/Windows NT (\d+\.\d+)/) ||
                        ua.match(/Mac OS X (\d+[._]\d+)/) ||
                        ua.match(/Android (\d+\.\d+)/);

            return match ? match[1].replace('_', '.') : undefined;
        },

        getArchType: function (ua, pf) {
            pf = (pf === '') ? '' : pf || navigator.platform;
            ua = ua || navigator.userAgent;

            var re;

            // Windows RT and Windows Phone using ARMv7
            if (/Windows/.test(ua) && /ARM/.test(ua)) {
                return 'armv7';
            }

            // IE-specific property
            if (navigator.cpuClass) {
                return navigator.cpuClass.toLowerCase();
            }

            // ARM
            re = /armv\d+/i;
            if (re.test(pf) || re.test(ua)) {
                return RegExp.lastMatch.toLowerCase();
            }

            // ARMv8 64-bit
            if (/aarch64/.test(pf)) {
                return 'armv8';
            }

            // We can't detect the type info. It's probably x86 but unsure.
            // For example, iOS may be running on ARM-based Apple A7 processor
            return 'x86';
        },

        getArchSize: function (ua, pf) {
            pf = (pf === '') ? '' : pf || navigator.platform;
            ua = ua || navigator.userAgent;

            var re = /x64|x86_64|Win64|WOW64|aarch64/i;
            if (re.test(pf) || re.test(ua)) {
                return 64;
            }

            // We can't detect the bit info. It's probably 32 but unsure.
            // For example, OS X may be running on 64-bit Core i7 processor
            return 32;
        },

        // Universal feature detect to deliver graded browser support (targets IE 11 and above).
        cutsTheMustard: function () {
            return 'classList' in document.createElement('div') && 'MutationObserver' in window;
        },

        platform: 'other',
        platformVersion: undefined,
        archType: 'x64',
        archSize: 32,
        isARM: false
    };
    (function () {
        var h = document.documentElement;

        // if other than 'windows', immediately replace the platform classname on the html-element
        // to avoid lots of flickering
        var platform = window.site.platform = window.site.getPlatform();
        var version = window.site.platformVersion = window.site.getPlatformVersion();
        var _version = version ? parseFloat(version) : 0;

        if (platform === 'windows') {
            // Add class for Windows XP/Vista users to display
            // unsupported messaging on /download/thanks/ page.
            if (_version >= 5.1 && _version <= 6) {
                h.className += ' xpvista';
            }
        } else {
            h.className = h.className.replace('windows', platform);
        }

        // Add class to reflect the microprocessor architecture info
        var archType = window.site.archType = window.site.getArchType();
        var archSize = window.site.archSize = window.site.getArchSize();
        var isARM = window.site.isARM = archType.match(/armv(\d+)/);

        // Used for Windows and Linux ARM processor detection.
        if (archType !== 'x86') {
            h.className = h.className.replace('x86', archType);

            if (isARM) {
                h.className += ' arm';
            }
        }

        // Used for 64bit download link on Linux.
        if (archSize === 64) {
            h.className += ' x64';
        }

        // Add class to reflect if user agent is Firefox. Cherry-picked from mozilla-client.js.
        var isFirefox = /\s(Firefox|FxiOS)/.test(navigator.userAgent) && !/Iceweasel|IceCat|SeaMonkey|Camino|like Firefox/i.test(navigator.userAgent);

        if (isFirefox) {
            h.className += ' is-firefox';
        }

        // Add class to reflect browsers that get 1st class JS & CSS support.
        var isModernBrowser = window.site.isModernBrowser = window.site.cutsTheMustard();

        if (isModernBrowser) {
            h.className += ' is-modern-browser';
        }

        // Add class to reflect javascript availability for CSS
        h.className = h.className.replace(/\bno-js\b/, 'js');
    })();
})();
