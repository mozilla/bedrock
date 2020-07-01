/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global sinon */

describe('site.js', function () {

    'use strict';

    describe('getPlatform', function () {

        it('should identify Windows', function () {
            expect(window.site.getPlatform('Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)', 'Win64')).toBe('windows');
            expect(window.site.getPlatform('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)', 'Win32')).toBe('windows');
            expect(window.site.getPlatform('Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36 Edge/12.0', 'Win32')).toBe('windows');
        });

        it('should identify Android', function () {
            expect(window.site.getPlatform('Mozilla/5.0 (Android; Mobile; rv:26.0) Gecko/26.0 Firefox/26.0', 'foo')).toBe('android');
            expect(window.site.getPlatform('Mozilla/5.0 (Android; Tablet; rv:26.0) Gecko/26.0 Firefox/26.0', 'foo')).toBe('android');
        });

        it('should identify Linux', function () {
            expect(window.site.getPlatform('foo', 'Linux')).toBe('linux');
            expect(window.site.getPlatform('Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:32.0) Gecko/20100101 Firefox/32.0', 'Linux armv7l')).toBe('linux');
        });

        it('should identify old-Mac', function () {
            expect(window.site.getPlatform('Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27', 'foo')).toBe('other');
            expect(window.site.getPlatform('Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; nl-nl) AppleWebKit/533.16 (KHTML, like Gecko) Version/4.1 Safari/533.16', 'foo')).toBe('other');
            expect(window.site.getPlatform('Mozilla/4.0 (compatible; MSIE 5.23; Mac_PowerPC)', 'foo')).toBe('other');
            expect(window.site.getPlatform('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10', 'foo')).toBe('other');
            expect(window.site.getPlatform('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0', 'foo')).toBe('other');
            expect(window.site.getPlatform('Mozilla/4.0 (compatible; MSIE 5.23; Mac_PowerPC)', 'foo')).toBe('other');
        });

        it('should identify iOS', function () {
            expect(window.site.getPlatform('foo', 'iPhone')).toBe('ios');
            expect(window.site.getPlatform('foo', 'iPad')).toBe('ios');
            expect(window.site.getPlatform('foo', 'iPod')).toBe('ios');
            expect(window.site.getPlatform('foo', 'iPhone Simulator')).toBe('ios');
        });

        it('should identify iPadOS', function () {
            window.navigator.standalone = sinon.stub();
            expect(window.site.getPlatform('foo', 'MacIntel')).toBe('ios');
        });

        it('should identify OSX', function () {
            expect(window.site.getPlatform('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0', 'foo')).toBe('osx');
            expect(window.site.getPlatform('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/538.10.3 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1', 'foo')).toBe('osx');
        });
    });

    describe('getPlatformVersion', function () {
        it('should identify a Windows version', function () {
            expect(window.site.getPlatformVersion('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)')).toBe('7.1');
            expect(window.site.getPlatformVersion('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2249.0 Safari/537.36')).toBe('10.0');
        });

        it('should identify an OS X version', function () {
            expect(window.site.getPlatformVersion('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:30.0) Gecko/20100101 Firefox/30.0')).toBe('10.8');
            expect(window.site.getPlatformVersion('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/538.10.3 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')).toBe('10.10');
        });

        it('should identify an Android version', function () {
            expect(window.site.getPlatformVersion('Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')).toBe('2.3');
            expect(window.site.getPlatformVersion('Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30')).toBe('4.1');
        });

        it('should return undefined if a platform version cannot be found in the UA string', function () {
            expect(window.site.getPlatformVersion('Mozilla/5.0 (Android; Mobile; rv:27.0) Gecko/27.0 Firefox/27.0', 'Linux armv7l')).toBe(undefined);
            expect(window.site.getPlatformVersion('Mozilla/4.0 (compatible; MSIE 4.01; Windows 95)')).toBe(undefined);
            expect(window.site.getPlatformVersion('Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:32.0) Gecko/20100101 Firefox/32.0')).toBe(undefined);
        });
    });

    describe('getArchType', function () {

        it('should identify x86', function () {
            expect(window.site.getArchType('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0', 'Win64')).toBe('x86');
            expect(window.site.getArchType('Mozilla/5.0 (Windows NT 6.3; rv:27.0) Gecko/20100101 Firefox/27.0', 'Win32')).toBe('x86');
            expect(window.site.getArchType('Mozilla/5.0 (Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko', 'Win32')).toBe('x86');
            expect(window.site.getArchType('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0', 'MacIntel')).toBe('x86');
            expect(window.site.getArchType('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0', 'Linux x86_64')).toBe('x86');
            expect(window.site.getArchType('Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:27.0) Gecko/20100101 Firefox/27.0', 'Linux i686')).toBe('x86');
        });

        it('should identify ARM', function () {
            expect(window.site.getArchType('Mozilla/5.0 (Android; Mobile; rv:27.0) Gecko/27.0 Firefox/27.0', 'Linux armv7l')).toBe('armv7');
            expect(window.site.getArchType('Mozilla/5.0 (Android 5.0.2; Mobile; rv:42.0) Gecko/42.0 Firefox/42.0', 'Linux aarch64')).toBe('armv8');
            expect(window.site.getArchType('Mozilla/5.0 (X11; U; Linux armv6l; en-US; rv:1.9.1b2pre) Gecko/20081116 Fennec/1.0a2pre', 'Linux armv6l')).toBe('armv6');
            expect(window.site.getArchType('Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:32.0) Gecko/20100101 Firefox/32.0', 'Linux armv7l')).toBe('armv7');
            expect(window.site.getArchType('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; ARM; Trident/6.0)')).toBe('armv7');
            expect(window.site.getArchType('Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/7.0; Touch; rv:11; IEMobile/11.0; NOKIA; Lumia 928) like Gecko')).toBe('armv7');
        });
    });

    describe('getArchSize', function () {

        it('should identify 64', function () {
            expect(window.site.getArchSize('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0', 'Win64')).toBe(64);
            expect(window.site.getArchSize('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0', 'Linux x86_64')).toBe(64);
            expect(window.site.getArchSize('Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko', 'Win64')).toBe(64);
            expect(window.site.getArchSize('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36', 'Win64')).toBe(64);
            expect(window.site.getArchSize('Mozilla/5.0 (Android 5.0.2; Mobile; rv:42.0) Gecko/42.0 Firefox/42.0', 'Linux aarch64')).toBe(64);
        });

        it('should identify 32', function () {
            expect(window.site.getArchSize('Mozilla/5.0 (Windows NT 6.3; rv:27.0) Gecko/20100101 Firefox/27.0', 'Win32')).toBe(32);
            expect(window.site.getArchSize('Mozilla/5.0 (Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko', 'Win32')).toBe(32);
            expect(window.site.getArchSize('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0', 'MacIntel')).toBe(32);
            expect(window.site.getArchSize('Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:27.0) Gecko/20100101 Firefox/27.0', 'Linux i686')).toBe(32);
            expect(window.site.getArchSize('Mozilla/5.0 (X11; U; Linux armv6l; en-US; rv:1.9.1b2pre) Gecko/20081116 Fennec/1.0a2pre', 'Linux armv6l')).toBe(32);
            expect(window.site.getArchSize('Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:32.0) Gecko/20100101 Firefox/32.0', 'Linux armv7l')).toBe(32);
        });
    });
});
