/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('site.js', function () {
    describe('getPlatform', function () {
        it('should identify Windows', function () {
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'Win64'
                )
            ).toBe('windows');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Win64'
                )
            ).toBe('windows');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)',
                    'Win32'
                )
            ).toBe('windows');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36 Edge/12.0',
                    'Win32'
                )
            ).toBe('windows');
        });

        it('should identify Android', function () {
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Android; Mobile; rv:26.0) Gecko/26.0 Firefox/26.0',
                    'foo'
                )
            ).toBe('android');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Android; Tablet; rv:26.0) Gecko/26.0 Firefox/26.0',
                    'foo'
                )
            ).toBe('android');
        });

        it('should identify Linux', function () {
            expect(window.site.getPlatform('foo', 'Linux')).toBe('linux');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:32.0) Gecko/20100101 Firefox/32.0',
                    'Linux armv7l'
                )
            ).toBe('linux');
        });

        it('should identify old-Mac', function () {
            expect(
                window.site.getPlatform(
                    'Mozilla/4.0 (compatible; MSIE 5.23; Mac_PowerPC)',
                    'foo'
                )
            ).toBe('other');
            expect(
                window.site.getPlatform(
                    'Mozilla/4.0 (compatible; MSIE 5.23; Mac_PowerPC)',
                    'foo'
                )
            ).toBe('other');
        });

        it('should identify iOS', function () {
            expect(window.site.getPlatform('foo', 'iPhone')).toBe('ios');
            expect(window.site.getPlatform('foo', 'iPad')).toBe('ios');
            expect(window.site.getPlatform('foo', 'iPod')).toBe('ios');
            expect(window.site.getPlatform('foo', 'iPhone Simulator')).toBe(
                'ios'
            );
        });

        it('should identify iPadOS', function () {
            window.ontouchstart = sinon.stub();
            expect(window.site.getPlatform('foo', 'MacIntel')).toBe('ios');
        });

        it('should identify OSX', function () {
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0',
                    'foo'
                )
            ).toBe('osx');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                    'foo'
                )
            ).toBe('osx');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
                    'foo'
                )
            ).toBe('osx');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
                    'foo'
                )
            ).toBe('osx');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; nl-nl) AppleWebKit/533.16 (KHTML, like Gecko) Version/4.1 Safari/533.16',
                    'foo'
                )
            ).toBe('osx');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
                    'foo'
                )
            ).toBe('osx');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
                    'foo'
                )
            ).toBe('osx');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/538.10.3 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
                    'foo'
                )
            ).toBe('osx');
            expect(
                window.site.getPlatform(
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                    'foo'
                )
            ).toBe('osx');
        });
    });

    describe('getPlatformVersion', function () {
        it('should identify a Windows version', function () {
            expect(
                window.site.getPlatformVersion(
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
                )
            ).toBe('6.1');
            expect(
                window.site.getPlatformVersion(
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)'
                )
            ).toBe('7.1');
            expect(
                window.site.getPlatformVersion(
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2249.0 Safari/537.36'
                )
            ).toBe('10.0');
        });

        it('should identify an OS X version', function () {
            expect(
                window.site.getPlatformVersion(
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:30.0) Gecko/20100101 Firefox/30.0'
                )
            ).toBe('10.8');
            expect(
                window.site.getPlatformVersion(
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/538.10.3 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'
                )
            ).toBe('10.10');
        });

        it('should identify an Android version', function () {
            expect(
                window.site.getPlatformVersion(
                    'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
                )
            ).toBe('2.3');
            expect(
                window.site.getPlatformVersion(
                    'Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30'
                )
            ).toBe('4.1');
        });

        it('should return undefined if a platform version cannot be found in the UA string', function () {
            expect(
                window.site.getPlatformVersion(
                    'Mozilla/5.0 (Android; Mobile; rv:27.0) Gecko/27.0 Firefox/27.0',
                    'Linux armv7l'
                )
            ).toBe(undefined);
            expect(
                window.site.getPlatformVersion(
                    'Mozilla/4.0 (compatible; MSIE 4.01; Windows 95)'
                )
            ).toBe(undefined);
            expect(
                window.site.getPlatformVersion(
                    'Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:32.0) Gecko/20100101 Firefox/32.0'
                )
            ).toBe(undefined);
        });
    });

    describe('getArchType', function () {
        it('should identify x86', function () {
            expect(
                window.site.getArchType(
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0',
                    'Win64'
                )
            ).toBe('x86');
            expect(
                window.site.getArchType(
                    'Mozilla/5.0 (Windows NT 6.3; rv:27.0) Gecko/20100101 Firefox/27.0',
                    'Win32'
                )
            ).toBe('x86');
            expect(
                window.site.getArchType(
                    'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko',
                    'Win32'
                )
            ).toBe('x86');
            expect(
                window.site.getArchType(
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0',
                    'MacIntel'
                )
            ).toBe('x86');
            expect(
                window.site.getArchType(
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',
                    'Linux x86_64'
                )
            ).toBe('x86');
            expect(
                window.site.getArchType(
                    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:27.0) Gecko/20100101 Firefox/27.0',
                    'Linux i686'
                )
            ).toBe('x86');
        });

        it('should identify ARM', function () {
            expect(
                window.site.getArchType(
                    'Mozilla/5.0 (Android; Mobile; rv:27.0) Gecko/27.0 Firefox/27.0',
                    'Linux armv7l'
                )
            ).toBe('armv7');
            expect(
                window.site.getArchType(
                    'Mozilla/5.0 (Android 5.0.2; Mobile; rv:42.0) Gecko/42.0 Firefox/42.0',
                    'Linux aarch64'
                )
            ).toBe('armv8');
            expect(
                window.site.getArchType(
                    'Mozilla/5.0 (X11; U; Linux armv6l; en-US; rv:1.9.1b2pre) Gecko/20081116 Fennec/1.0a2pre',
                    'Linux armv6l'
                )
            ).toBe('armv6');
            expect(
                window.site.getArchType(
                    'Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:32.0) Gecko/20100101 Firefox/32.0',
                    'Linux armv7l'
                )
            ).toBe('armv7');
        });
    });

    describe('getArchSize', function () {
        it('should identify 64', function () {
            expect(
                window.site.getArchSize(
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0',
                    'Win64'
                )
            ).toBe(64);
            expect(
                window.site.getArchSize(
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',
                    'Linux x86_64'
                )
            ).toBe(64);
            expect(
                window.site.getArchSize(
                    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
                    'Win64'
                )
            ).toBe(64);
            expect(
                window.site.getArchSize(
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
                    'Win64'
                )
            ).toBe(64);
            expect(
                window.site.getArchSize(
                    'Mozilla/5.0 (Android 5.0.2; Mobile; rv:42.0) Gecko/42.0 Firefox/42.0',
                    'Linux aarch64'
                )
            ).toBe(64);
        });

        it('should identify 32', function () {
            expect(
                window.site.getArchSize(
                    'Mozilla/5.0 (Windows NT 6.3; rv:27.0) Gecko/20100101 Firefox/27.0',
                    'Win32'
                )
            ).toBe(32);
            expect(
                window.site.getArchSize(
                    'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko',
                    'Win32'
                )
            ).toBe(32);
            expect(
                window.site.getArchSize(
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0',
                    'MacIntel'
                )
            ).toBe(32);
            expect(
                window.site.getArchSize(
                    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:27.0) Gecko/20100101 Firefox/27.0',
                    'Linux i686'
                )
            ).toBe(32);
            expect(
                window.site.getArchSize(
                    'Mozilla/5.0 (X11; U; Linux armv6l; en-US; rv:1.9.1b2pre) Gecko/20081116 Fennec/1.0a2pre',
                    'Linux armv6l'
                )
            ).toBe(32);
            expect(
                window.site.getArchSize(
                    'Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:32.0) Gecko/20100101 Firefox/32.0',
                    'Linux armv7l'
                )
            ).toBe(32);
        });
    });

    describe('getArchSizeClientHint', function () {
        it('should identify 64', function () {
            expect(window.site.getArchSizeClientHint(64)).toBe(64);
            expect(window.site.getArchSizeClientHint('64')).toBe(64);
        });

        it('should identify 32', function () {
            expect(window.site.getArchSizeClientHint(32)).toBe(32);
            expect(window.site.getArchSizeClientHint('32')).toBe(32);
        });

        it('should default to 32', function () {
            expect(window.site.getArchSizeClientHint()).toBe(32);
            expect(window.site.getArchSizeClientHint(null)).toBe(32);
            expect(window.site.getArchSizeClientHint(undefined)).toBe(32);
            expect(window.site.getArchSizeClientHint('abcd')).toBe(32);
            expect(window.site.getArchSizeClientHint('')).toBe(32);
            expect(window.site.getArchSizeClientHint(1234)).toBe(32);
        });
    });

    describe('getWindowsVersionClientHint', function () {
        it('should identify 13 and up as Windows 11 or later', function () {
            expect(window.site.getWindowsVersionClientHint('13.0.0')).toBe(
                '11.0'
            );
            expect(window.site.getWindowsVersionClientHint('14.0.0')).toBe(
                '11.0'
            );
        });

        it('should identify 1 through 12 as Windows 10', function () {
            expect(window.site.getWindowsVersionClientHint('12.0.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('12.1.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('11.0.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('10.0.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('9.0.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('8.0.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('7.0.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('6.0.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('5.0.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('4.0.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('3.0.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('2.0.0')).toBe(
                '10.0'
            );
            expect(window.site.getWindowsVersionClientHint('1.0.0')).toBe(
                '10.0'
            );
        });

        it('should identify 0.3 as Windows 8.1', function () {
            expect(window.site.getWindowsVersionClientHint('0.3')).toBe('6.3');
            expect(window.site.getWindowsVersionClientHint('0.3.1')).toBe(
                '6.3'
            );
        });

        it('should identify 0.2 as Windows 8', function () {
            expect(window.site.getWindowsVersionClientHint('0.2')).toBe('6.2');
            expect(window.site.getWindowsVersionClientHint('0.2.0')).toBe(
                '6.2'
            );
        });

        it('should identify 0.1 as Windows 7', function () {
            expect(window.site.getWindowsVersionClientHint('0.1')).toBe('6.1');
            expect(window.site.getWindowsVersionClientHint('0.1.2')).toBe(
                '6.1'
            );
        });

        it('should identify 0.1 as Windows 7', function () {
            expect(window.site.getWindowsVersionClientHint('0.1')).toBe('6.1');
            expect(window.site.getWindowsVersionClientHint('0.1.2')).toBe(
                '6.1'
            );
        });

        it('should return anything else as zero / unknown', function () {
            expect(window.site.getWindowsVersionClientHint('0.9')).toBe('0');
            expect(window.site.getWindowsVersionClientHint('0.8')).toBe('0');
            expect(window.site.getWindowsVersionClientHint('0.7')).toBe('0');
            expect(window.site.getWindowsVersionClientHint('0.6')).toBe('0');
            expect(window.site.getWindowsVersionClientHint('0.5')).toBe('0');
            expect(window.site.getWindowsVersionClientHint('0.4')).toBe('0');
            expect(window.site.getWindowsVersionClientHint('0.0.1')).toBe('0');
        });
    });

    describe('isARM', function () {
        beforeEach(function () {
            // don't fall back to `window.site.archType` in tests.
            sinon.stub(window.site, 'archType').value(null);
        });

        it('should return true for ARM processors', function () {
            expect(window.site.isARM('arm')).toBeTrue();
            expect(window.site.isARM('armv8')).toBeTrue();
            expect(window.site.isARM('armv7')).toBeTrue();
        });

        it('should return false for other values', function () {
            expect(window.site.isARM('x86')).toBeFalse();
            expect(window.site.isARM('')).toBeFalse();
            expect(window.site.isARM(null)).toBeFalse();
            expect(window.site.isARM(undefined)).toBeFalse();
        });
    });

    describe('getPlatformClass', function () {
        beforeEach(function () {
            document.documentElement.className = 'windows no-js';
            window.site.fxSupported = true;
        });

        afterEach(function () {
            document.documentElement.className = '';
            window.site.fxSupported = true;
        });

        it('should return the appropriate HTML class for Windows 10', function () {
            spyOn(window.site, 'cutsTheMustard').and.returnValue(true);
            spyOn(window.site, 'isARM').and.returnValue(false);
            spyOn(window.site, 'isFirefox').and.returnValue(false);
            const classString = window.site.getPlatformClass(
                'windows',
                10.0,
                32
            );
            expect(classString).toEqual(
                'windows js windows-10-plus is-modern-browser'
            );
            expect(window.site.fxSupported).toBeTrue;
        });

        it('should return the appropriate HTML class for macOS 10.15', function () {
            spyOn(window.site, 'cutsTheMustard').and.returnValue(true);
            spyOn(window.site, 'isARM').and.returnValue(false);
            spyOn(window.site, 'isFirefox').and.returnValue(false);
            const classString = window.site.getPlatformClass('osx', 10.15, 32);
            expect(classString).toEqual('osx js is-modern-browser');
        });

        it('should return the appropriate HTML class for Linux', function () {
            spyOn(window.site, 'cutsTheMustard').and.returnValue(true);
            spyOn(window.site, 'isARM').and.returnValue(false);
            spyOn(window.site, 'isFirefox').and.returnValue(false);
            const classString = window.site.getPlatformClass(
                'linux',
                undefined,
                32
            );
            expect(classString).toEqual('linux js is-modern-browser');
            expect(window.site.fxSupported).toBeTrue;
        });

        it('should return the appropriate HTML class for Android', function () {
            spyOn(window.site, 'cutsTheMustard').and.returnValue(true);
            spyOn(window.site, 'isARM').and.returnValue(false);
            spyOn(window.site, 'isFirefox').and.returnValue(false);
            const classString = window.site.getPlatformClass(
                'android',
                '4.1',
                64
            );
            expect(classString).toEqual('android js x64 is-modern-browser');
            expect(window.site.fxSupported).toBeTrue;
        });

        it('should return the appropriate HTML class for iOS', function () {
            spyOn(window.site, 'cutsTheMustard').and.returnValue(true);
            spyOn(window.site, 'isARM').and.returnValue(false);
            spyOn(window.site, 'isFirefox').and.returnValue(false);
            const classString = window.site.getPlatformClass(
                'ios',
                undefined,
                64
            );
            expect(classString).toEqual('ios js x64 is-modern-browser');
            expect(window.site.fxSupported).toBeTrue;
        });

        it('should return the appropriate HTML class for unknown platforms', function () {
            spyOn(window.site, 'cutsTheMustard').and.returnValue(true);
            spyOn(window.site, 'isARM').and.returnValue(false);
            spyOn(window.site, 'isFirefox').and.returnValue(false);
            const classString = window.site.getPlatformClass(
                'other',
                undefined,
                32
            );
            expect(classString).toEqual('other js is-modern-browser');
            expect(window.site.fxSupported).toBeTrue; // we don't know for sure here to say false.
        });

        it('should return the appropriate HTML class for outdated browsers', function () {
            spyOn(window.site, 'cutsTheMustard').and.returnValue(false);
            spyOn(window.site, 'isARM').and.returnValue(false);
            spyOn(window.site, 'isFirefox').and.returnValue(false);
            const classString = window.site.getPlatformClass(
                'windows',
                10.0,
                32
            );
            expect(classString).toEqual('windows js windows-10-plus');
            expect(window.site.fxSupported).toBeTrue;
        });

        it('should return the appropriate HTML class for Firefox browsers', function () {
            spyOn(window.site, 'cutsTheMustard').and.returnValue(true);
            spyOn(window.site, 'isARM').and.returnValue(false);
            spyOn(window.site, 'isFirefox').and.returnValue(true);
            const classString = window.site.getPlatformClass(
                'windows',
                10.0,
                64
            );
            expect(classString).toEqual(
                'windows js windows-10-plus x64 is-firefox is-modern-browser'
            );
            expect(window.site.fxSupported).toBeTrue;
        });

        it('should return the appropriate HTML class for ARM based CPUs', function () {
            spyOn(window.site, 'cutsTheMustard').and.returnValue(true);
            spyOn(window.site, 'isARM').and.returnValue(true);
            spyOn(window.site, 'isFirefox').and.returnValue(false);
            const classString = window.site.getPlatformClass(
                'windows',
                10.0,
                32
            );
            expect(classString).toEqual(
                'windows js windows-10-plus arm is-modern-browser'
            );
            expect(window.site.fxSupported).toBeTrue;
        });

        it('should return the appropriate HTML class for outdated Windows operating systems', function () {
            spyOn(window.site, 'cutsTheMustard').and.returnValue(false);
            spyOn(window.site, 'isARM').and.returnValue(false);
            spyOn(window.site, 'isFirefox').and.returnValue(false);
            const classString = window.site.getPlatformClass(
                'windows',
                6.3,
                32
            );
            expect(classString).toEqual('windows js fx-unsupported');
            expect(window.site.fxSupported).toBeFalse;
        });

        it('should return the appropriate HTML class for outdated macOS operating systems', function () {
            spyOn(window.site, 'cutsTheMustard').and.returnValue(false);
            spyOn(window.site, 'isARM').and.returnValue(false);
            spyOn(window.site, 'isFirefox').and.returnValue(false);
            const classString = window.site.getPlatformClass('osx', 10.14, 64);
            expect(classString).toEqual('osx js fx-unsupported x64');
            expect(window.site.fxSupported).toBeFalse;
        });
    });
});
