/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';
    window.site = {
        getPlatform: function (ua, pf) {
            pf = pf || navigator.platform;
            ua = ua || navigator.userAgent;

            if (pf.indexOf('Win32') !== -1 || pf.indexOf('Win64') !== -1) {
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
            if (
                pf.indexOf('iPhone') !== -1 ||
                pf.indexOf('iPad') !== -1 ||
                pf.indexOf('iPod') !== -1 ||
                (pf.indexOf('MacIntel') !== -1 && 'standalone' in navigator)
            ) {
                // iPadOS
                return 'ios';
            }
            if (
                ua.indexOf('Mac OS X') !== -1 &&
                !/Mac OS X 10.(1[0-1]|[1-9])\D/.test(ua)
            ) {
                return 'osx';
            }

            return 'other';
        },

        getPlatformVersion: function (ua) {
            ua = ua || navigator.userAgent;

            // On OS X, Safari and Chrome have underscores instead of dots
            var match =
                ua.match(/Windows NT (\d+\.\d+)/) ||
                ua.match(/Mac OS X (\d+[._]\d+)/) ||
                ua.match(/Android (\d+\.\d+)/);

            return match ? match[1].replace('_', '.') : undefined;
        },

        // Madness from https://docs.microsoft.com/microsoft-edge/web-platform/how-to-detect-win11
        getWindowsVersionClientHint: function (version) {
            var fullPlatformVersion = version ? version.toString() : '0';
            var majorPlatformVersion = parseInt(
                fullPlatformVersion.split('.')[0],
                10
            );
            if (majorPlatformVersion >= 13) {
                // Windows 11 or later.
                return '11.0.0';
            } else if (majorPlatformVersion > 0) {
                // Windows 10
                return '10.0.0';
            } else {
                // Might be any Windows version less than 10, who knows.
                // Rather than return undefined here, fallback to UA string.
                return site.getPlatformVersion();
            }
        },

        getArchType: function (ua, pf) {
            pf = pf === '' ? '' : pf || navigator.platform;
            ua = ua || navigator.userAgent;

            var re;

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

        // Returns true if CPU is an ARM processor.
        isARM: function (architecture) {
            var arch =
                typeof architecture === 'string'
                    ? architecture
                    : window.site.archType;
            if (arch && (arch === 'arm' || arch.match(/armv(\d+)/))) {
                return true;
            }
            return false;
        },

        getArchSize: function (ua, pf) {
            pf = pf === '' ? '' : pf || navigator.platform;
            ua = ua || navigator.userAgent;

            var re = /x64|x86_64|Win64|WOW64|aarch64/i;
            if (re.test(pf) || re.test(ua)) {
                return 64;
            }

            // We can't detect the bit info. It's probably 32 but unsure.
            // For example, OS X may be running on 64-bit Core i7 processor
            return 32;
        },

        // Return 64 is CPU is 64bit, else assume that it's 32.
        getArchSizeClientHint: function (bitness) {
            if (bitness && parseInt(bitness, 10) === 64) {
                return 64;
            }
            return 32;
        },

        // Universal feature detect to deliver graded browser support (targets IE 11 and above).
        cutsTheMustard: function () {
            return (
                'classList' in document.createElement('div') &&
                'MutationObserver' in window
            );
        },

        platform: 'other',
        platformVersion: undefined,
        archType: 'x64',
        archSize: 32
    };

    function updateHTML() {
        var h = document.documentElement;
        var _version = window.site.platformVersion
            ? parseFloat(window.site.platformVersion)
            : 0;

        if (window.site.platform === 'windows') {
            // Detect Windows 10 "and up" to display installation
            // messaging on the /firefox/download/thanks/ page.

            if (_version >= 10.0) {
                h.className += ' windows-10-plus';
            }

            // Add fx-unsupported class name for Windows 8.1 and below
            // https://github.com/mozilla/bedrock/issues/13317
            if (_version <= 6.3) {
                h.className += ' fx-unsupported';
            }
        } else {
            h.className = h.className.replace('windows', window.site.platform);
        }

        if (window.site.platform === 'osx') {
            // Add fx-unsupported class name for macOS 10.14 and below
            // https://github.com/mozilla/bedrock/issues/13317
            if (_version <= 10.14) {
                h.className += ' fx-unsupported';
            }
        }

        // Used to display a custom installation message and
        // SUMO link on the /firefox/download/thanks/ page.
        if (window.site.isARM()) {
            h.className += ' arm';
        }

        // Used for 64bit download link on Linux and Firefox Beta on Windows.
        if (window.site.archSize === 64) {
            h.className += ' x64';
        }

        // Add class to reflect if user agent is Firefox. Cherry-picked from mozilla-client.js.
        var isFirefox =
            /\s(Firefox|FxiOS)/.test(navigator.userAgent) &&
            !/Iceweasel|IceCat|SeaMonkey|Camino|like Firefox/i.test(
                navigator.userAgent
            );

        if (isFirefox) {
            h.className += ' is-firefox';
        }

        // Add class to reflect browsers that get 1st class JS & CSS support.
        var isModernBrowser = (window.site.isModernBrowser =
            window.site.cutsTheMustard());

        if (isModernBrowser) {
            h.className += ' is-modern-browser';
        }

        // Add class to reflect javascript availability for CSS
        h.className = h.className.replace(/\bno-js\b/, 'js');
    }

    function getHighEntropyFromUAString() {
        window.site.platformVersion = window.site.getPlatformVersion();
        window.site.archType = window.site.getArchType();
        window.site.archSize = window.site.getArchSize();
    }

    (function () {
        window.site.platform = window.site.getPlatform();

        // For browsers that support client hints, get high entropy
        // values that might be frozen in the regular user agent string.
        if (
            'userAgentData' in navigator &&
            typeof navigator.userAgentData.getHighEntropyValues === 'function'
        ) {
            navigator.userAgentData
                .getHighEntropyValues([
                    'architecture',
                    'bitness',
                    'platformVersion'
                ])
                .then(function (ua) {
                    if (ua.platformVersion) {
                        if (window.site.platform === 'windows') {
                            window.site.platformVersion =
                                window.site.getWindowsVersionClientHint(
                                    ua.platformVersion
                                );
                        } else {
                            window.site.platformVersion = ua.platformVersion;
                        }
                    }

                    if (ua.architecture) {
                        window.site.archType = ua.architecture;
                    }

                    if (ua.bitness) {
                        window.site.archSize =
                            window.site.getArchSizeClientHint(ua.bitness);
                    }

                    updateHTML();
                })
                .catch(function () {
                    // some browsers might deny accessing high entropy info
                    // and reject the promise, so fall back to UA string instead.
                    getHighEntropyFromUAString();
                    updateHTML();
                });
        }
        // Else fall back to UA string parsing for non-supporting browsers.
        else {
            getHighEntropyFromUAString();
            updateHTML();
        }
    })();
})();
