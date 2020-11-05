/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';
    window.site = {

        supportsClientHints: function() {
            return 'userAgentData' in navigator &&
                   typeof navigator.userAgentData.getHighEntropyValues !== 'undefined' &&
                   'Promise' in window;
        },

        getClientHintsData: function() {
            return new window.Promise(function(resolve) {
                navigator.userAgentData.getHighEntropyValues([
                    'architecture',
                    'platform',
                    'platformVersion'
                ]).then(function(ua) {
                    if (ua && ua.architecture) {
                        window.site.clientHintData.architecture = ua.architecture;
                    }
                    if (ua && ua.platform) {
                        window.site.clientHintData.platform = ua.platform;
                    }
                    if (ua && ua.platformVersion) {
                        window.site.clientHintData.platformVersion = ua.platformVersion;
                    }
                    resolve();
                });
            });
        },

        getPlatformFromCH: function (platform) {
            if (platform === 'Windows') {
                return 'windows';
            }
            if (platform === 'Android') {
                return 'android';
            }
            if (platform === 'Linux') {
                return 'linux';
            }
            // TODO: there's no implementation of Client Hints available on iOS?
            if (platform === 'iOS') {
                return 'ios';
            }
            if (platform === 'Mac OS X') {
                return 'osx';
            }

            return 'other';
        },

        getPlatformFromUA: function (ua, pf) {
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

        getPlatformVersionFromCH: function (platform, version) {
            var match;

            // On OS X, Safari and Chrome have underscores instead of dots
            if (platform === 'Windows') {
                match = version.match(/\d+\.\d+/);
            } else if (platform === 'Mac OS X') {
                match = version.match(/\d+[._]\d+/);
            } else if (platform === 'Android') {
                // TODO do we need to detect Android versions?
                match = version.match(/\d+\.\d+/);
            }

            return match ? match[0].replace('_', '.') : undefined;
        },

        getPlatformVersionFromUA: function (ua) {
            ua = ua || navigator.userAgent;

            // On OS X, Safari and Chrome have underscores instead of dots
            var match = ua.match(/Windows NT (\d+\.\d+)/) ||
                        ua.match(/Mac OS X (\d+[._]\d+)/) ||
                        ua.match(/Android (\d+\.\d+)/);

            return match ? match[1].replace('_', '.') : undefined;
        },

        getArchTypeFromCH: function (arch) {
            // ARM
            if (/armv\d+/i.test(arch)) {
                return arch.toLowerCase();
            }

            // ARMv8 64-bit
            // TODO what should ARM values be when provided by CH? `ARM64`?
            if (/aarch64/.test(arch)) {
                return 'armv8';
            }

            // We can't detect the type info. It's probably x86 but unsure.
            // For example, iOS may be running on ARM-based Apple A7 processor
            return 'x86';
        },

        getArchTypeFromUA: function (ua, pf) {
            pf = (pf === '') ? '' : pf || navigator.platform;
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

        getArchSizeFromUA: function (ua, pf) {
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

        getArchSizeFromCH: function (arch) {
            var re = /x64|x86_64|Win64|WOW64|aarch64/i;
            if (re.test(arch)) {
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

        setHTMLClassNames: function() {
            var h = document.documentElement;
            var version = window.site.platformVersion ? parseFloat(window.site.platformVersion) : 0;

            // if other than 'windows', immediately replace the platform classname on the html-element
            // to avoid lots of flickering
            if (window.site.platform === 'windows') {
                // Add class for Windows XP/Vista users to display
                // unsupported messaging on /download/thanks/ page.
                if (version >= 5.1 && version <= 6) {
                    h.className += ' xpvista';
                // Add class for Windows 10 users to display
                // disclaimer messaging on /download/thanks/ page.
                } else if (version >= 10.0 && version <= 11) {
                    h.className += ' windows10';
                }
            } else {
                h.className = h.className.replace('windows', window.site.platform);
            }

            // Used for Linux ARM processor detection.
            if (window.site.archType !== 'x86') {
                h.className = h.className.replace('x86', window.site.archType);

                if (window.site.isARM) {
                    h.className += ' arm';
                }
            }

            // Used for 64bit download link on Linux.
            if (window.site.archSize === 64) {
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
        },

        clientHintData: {
            architecture: 'x64',
            platform: 'other',
            platformVersion: undefined
        },

        platform: 'other',
        platformVersion: undefined,
        archType: 'x64',
        archSize: 32,
        isARM: false
    };
    (function () {

        if (window.site.supportsClientHints()) {
            window.site.getClientHintsData().then(function() {
                console.log(window.site.clientHintData); // TODO remove me
                window.site.platform = window.site.getPlatformFromCH(window.site.clientHintData.platform);
                window.site.platformVersion = window.site.getPlatformVersionFromCH(window.site.clientHintData.platform, window.site.clientHintData.platformVersion);
                window.site.archType = window.site.getArchTypeFromCH(window.site.clientHintData.architecture, window.site.clientHintData.platform);
                window.site.archSize = window.site.getArchSizeFromCH(window.site.clientHintData.architecture);
                window.site.isARM = window.site.archType.match(/armv(\d+)/);
                window.site.setHTMLClassNames();
            });
        } else {
            window.site.platform = window.site.getPlatformFromUA();
            window.site.platformVersion = window.site.getPlatformVersionFromUA();
            window.site.archType = window.site.getArchTypeFromUA();
            window.site.archSize = window.site.getArchSizeFromUA();
            window.site.isARM = window.site.archType.match(/armv(\d+)/);
            window.site.setHTMLClassNames();
        }
    })();
})();
