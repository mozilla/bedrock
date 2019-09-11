/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';
    window.site = {
        getPlatform: function (ua, pf) {
            // Firefox OS navigator.platform is an empty string, which equates to a falsey value in JS
            // Ths means we must use an ugly ternary statement here to make testing easier.
            pf = (pf === '') ? '' : pf || navigator.platform;
            ua = ua || navigator.userAgent;

            if (/Win(16|9[x58]|NT( [1234]| 5\.0| [^0-9]|[^ -]|$))/.test(ua) ||
                    /Windows ([MC]E|9[x58]|3\.1|4\.10|NT( [1234]\D| 5\.0| [^0-9]|[^ ]|$))/.test(ua) ||
                    /Windows_95/.test(ua)) {
                /**
                 * Officially unsupported platforms are Windows 95, 98, ME, NT 4.x, 2000
                 * These regular expressions match:
                 *  - Win16
                 *  - Win9x
                 *  - Win95
                 *  - Win98
                 *  - WinNT (not followed by version or followed by version <= 5)
                 *  - Windows ME
                 *  - Windows CE
                 *  - Windows 9x
                 *  - Windows 95
                 *  - Windows 98
                 *  - Windows 3.1
                 *  - Windows 4.10
                 *  - Windows NT (not followed by version or followed by version <= 5)
                 *  - Windows_95
                 */
                return 'oldwin';
            }
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
                return 'oldmac';
            }
            if (/Mac OS X 10.[0-8]\D/.test(ua)) {
                return 'oldmac';
            }
            if (pf.indexOf('iPhone') !== -1 ||
                    pf.indexOf('iPad') !== -1 ||
                    pf.indexOf('iPod') !== -1 ) {
                return 'ios';
            }
            if (ua.indexOf('Mac OS X') !== -1) {
                return 'osx';
            }
            if (ua.indexOf('MSIE 5.2') !== -1) {
                return 'oldmac';
            }
            if (pf.indexOf('Mac') !== -1) {
                return 'oldmac';
            }
            if (pf === '' && /Firefox/.test(ua)) {
                return 'fxos';
            }

            return 'other';
        },

        getPlatformVersion: function (ua) {
            ua = ua || navigator.userAgent;

            // On OS X, Safari and Chrome have underscores instead of dots
            var match = ua.match(/Windows\ NT\ (\d+\.\d+)/) ||
                        ua.match(/Mac\ OS\ X\ (\d+[\._]\d+)/) ||
                        ua.match(/Android\ (\d+\.\d+)/);

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

            // PowerPC
            re = /PowerPC|PPC/i;
            if (re.test(pf) || re.test(ua)) {
                return 'ppc';
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

        platform: 'other',
        platformVersion: undefined,
        archType: 'x64',
        archSize: 32
    };
    (function () {
        var h = document.documentElement;

        // if other than 'windows', immediately replace the platform classname on the html-element
        // to avoid lots of flickering
        var platform = window.site.platform = window.site.getPlatform();
        var version = window.site.platformVersion = window.site.getPlatformVersion();
        var _version = version ? parseFloat(version) : 0;

        if (platform === 'windows') {
            // Add class to allow Windows XP/Vista users to download Firefox 52 ESR, though these
            // legacy platforms are now officially unsupported
            if (_version >= 5.1 && _version <= 6) {
                h.className += ' xpvista';
            }

            // Add class to support downloading Firefox for Windows 64-bit on Windows 7 and later
            if (_version >= 6.1) {
                h.className += ' win7up';
            }
        } else {
            h.className = h.className.replace('windows', platform);
        }

        // Add class to reflect the microprocessor architecture info
        var archType = window.site.archType = window.site.getArchType();
        var archSize = window.site.archSize = window.site.getArchSize();
        var isARM = archType.match(/armv(\d+)/);

        if (archType !== 'x86') {
            h.className = h.className.replace('x86', archType);

            if (isARM) {
                h.className += ' arm';

                // Add class to support downloading Firefox for Android on ARMv7 and later
                if (parseFloat(isARM[1]) >= 7) {
                    h.className += ' armv7up';
                }
            }
        }
        if (archSize === 64) {
            h.className += ' x64';
        }

        // Add class to reflect if user agent is Firefox. Cherry-picked from mozilla-client.js.
        var isFirefox = /\s(Firefox|FxiOS)/.test(navigator.userAgent) && !/Iceweasel|IceCat|SeaMonkey|Camino|like\ Firefox/i.test(navigator.userAgent);

        if (isFirefox) {
            h.className += ' is-firefox';
        }

        // Add class to reflect javascript availability for CSS
        h.className = h.className.replace(/\bno-js\b/, 'js');
    })();
})();
