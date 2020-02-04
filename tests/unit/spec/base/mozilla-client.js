/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-client.js', function() {

    'use strict';

    // User-agent strings for the most of the following tests
    var uas = {
        // Firefox family
        'firefox': {
            'windows': 'Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0',
            'osx': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0',
            'linux': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0',
            'maemo': 'Mozilla/5.0 (Maemo; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1',
            'android': {
                'mobile': 'Mozilla/5.0 (Android; Mobile; rv:26.0) Gecko/26.0 Firefox/26.0',
                'tablet': 'Mozilla/5.0 (Android; Tablet; rv:26.0) Gecko/26.0 Firefox/26.0'
            },
            'ios': {
                'mobile': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.1 Mobile/12F69 Safari/600.1.4',
                'tablet': 'Mozilla/5.0 (iPad; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4'
            },
            'fxos': {
                'mobile': 'Mozilla/5.0 (Mobile; rv:26.0) Gecko/26.0 Firefox/26.0',
                'tablet': 'Mozilla/5.0 (Tablet; rv:26.0) Gecko/26.0 Firefox/26.0'
            }
        },
        // Other Gecko browsers
        'camino': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; en; rv:1.9.2.24) Gecko/20111114 Camino/2.1 (like Firefox/3.6.24)',
        'caminolikefx': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; en; rv:1.9.2.24) Gecko/20111114 (like Firefox/3.6.24)',
        'seamonkey': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0 SeaMonkey/2.37a1',
        'icecat': 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121201 icecat/17.0.1',
        'iceweasel': 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1',
        // Non-Gecko browsers
        'chrome': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
        'safari': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'ie': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
    };

    describe('_isFirefox', function() {

        var test = function(ua) {
            return expect(window.Mozilla.Client._isFirefox(ua));
        };

        it('should return true for Firefox on desktop', function() {
            test(uas.firefox.windows).toBeTruthy();
            test(uas.firefox.osx).toBeTruthy();
            test(uas.firefox.linux).toBeTruthy();
        });

        it('should return true for Firefox on Maemo', function() {
            test(uas.firefox.maemo).toBeTruthy();
        });

        it('should return true for Firefox on Android', function() {
            test(uas.firefox.android.mobile).toBeTruthy();
            test(uas.firefox.android.tablet).toBeTruthy();
        });

        it('should return true for Firefox on iOS', function() {
            test(uas.firefox.ios.mobile).toBeTruthy();
            test(uas.firefox.ios.tablet).toBeTruthy();
        });

        it('should return true for Firefox OS', function() {
            test(uas.firefox.fxos.mobile).toBeTruthy();
            test(uas.firefox.fxos.tablet).toBeTruthy();
        });

        it('should return false for other Gecko browsers', function() {
            test(uas.camino).toBeFalsy();
            test(uas.caminolikefx).toBeFalsy();
            test(uas.seamonkey).toBeFalsy();
            test(uas.icecat).toBeFalsy();
            test(uas.iceweasel).toBeFalsy();
        });

        it('should return false for non-Gecko browsers', function() {
            test(uas.chrome).toBeFalsy();
            test(uas.safari).toBeFalsy();
            test(uas.ie).toBeFalsy();
        });

    });

    describe('_isFirefoxDesktop', function () {

        var test = function(ua) {
            return expect(window.Mozilla.Client._isFirefoxDesktop(ua));
        };

        it('should return true for Firefox on desktop', function() {
            test(uas.firefox.windows).toBeTruthy();
            test(uas.firefox.osx).toBeTruthy();
            test(uas.firefox.linux).toBeTruthy();
        });

        it('should return false for Firefox on Maemo', function() {
            test(uas.firefox.maemo).toBeFalsy();
        });

        it('should return false for Firefox on Android', function() {
            test(uas.firefox.android.mobile).toBeFalsy();
            test(uas.firefox.android.tablet).toBeFalsy();
        });

        it('should return false for Firefox on iOS', function() {
            test(uas.firefox.ios.mobile).toBeFalsy();
            test(uas.firefox.ios.tablet).toBeFalsy();
        });

        it('should return false for Firefox OS', function() {
            test(uas.firefox.fxos.mobile).toBeFalsy();
            test(uas.firefox.fxos.tablet).toBeFalsy();
        });

        it('should return false for other Gecko browsers', function() {
            test(uas.camino).toBeFalsy();
            test(uas.caminolikefx).toBeFalsy();
            test(uas.seamonkey).toBeFalsy();
            test(uas.icecat).toBeFalsy();
            test(uas.iceweasel).toBeFalsy();
        });

        it('should return false for non-Gecko browsers', function() {
            test(uas.chrome).toBeFalsy();
            test(uas.safari).toBeFalsy();
            test(uas.ie).toBeFalsy();
        });

    });

    describe('_isFirefoxAndroid', function () {

        var test = function(ua) {
            return expect(window.Mozilla.Client._isFirefoxAndroid(ua));
        };

        it('should return false for Firefox on desktop', function() {
            test(uas.firefox.windows).toBeFalsy();
            test(uas.firefox.osx).toBeFalsy();
            test(uas.firefox.linux).toBeFalsy();
        });

        it('should return false for Firefox on Maemo', function() {
            test(uas.firefox.maemo).toBeFalsy();
        });

        it('should return true for Firefox on Android', function() {
            test(uas.firefox.android.mobile).toBeTruthy();
            test(uas.firefox.android.tablet).toBeTruthy();
        });

        it('should return false for Firefox on iOS', function() {
            test(uas.firefox.ios.mobile).toBeFalsy();
            test(uas.firefox.ios.tablet).toBeFalsy();
        });

        it('should return false for Firefox OS', function() {
            test(uas.firefox.fxos.mobile).toBeFalsy();
            test(uas.firefox.fxos.tablet).toBeFalsy();
        });

        it('should return false for other Gecko browsers', function() {
            test(uas.camino).toBeFalsy();
            test(uas.caminolikefx).toBeFalsy();
            test(uas.seamonkey).toBeFalsy();
            test(uas.icecat).toBeFalsy();
            test(uas.iceweasel).toBeFalsy();
        });

        it('should return false for non-Gecko browsers', function() {
            test(uas.chrome).toBeFalsy();
            test(uas.safari).toBeFalsy();
            test(uas.ie).toBeFalsy();
        });

    });

    describe('_isFirefoxiOS', function () {

        var test = function(ua) {
            return expect(window.Mozilla.Client._isFirefoxiOS(ua));
        };

        it('should return false for Firefox on desktop', function() {
            test(uas.firefox.windows).toBeFalsy();
            test(uas.firefox.osx).toBeFalsy();
            test(uas.firefox.linux).toBeFalsy();
        });

        it('should return false for Firefox on Maemo', function() {
            test(uas.firefox.maemo).toBeFalsy();
        });

        it('should return false for Firefox on Android', function() {
            test(uas.firefox.android.mobile).toBeFalsy();
            test(uas.firefox.android.tablet).toBeFalsy();
        });

        it('should return true for Firefox on iOS', function() {
            test(uas.firefox.ios.mobile).toBeTruthy();
            test(uas.firefox.ios.tablet).toBeTruthy();
        });

        it('should return false for Firefox OS', function() {
            test(uas.firefox.fxos.mobile).toBeFalsy();
            test(uas.firefox.fxos.tablet).toBeFalsy();
        });

        it('should return false for other Gecko browsers', function() {
            test(uas.camino).toBeFalsy();
            test(uas.caminolikefx).toBeFalsy();
            test(uas.seamonkey).toBeFalsy();
            test(uas.icecat).toBeFalsy();
            test(uas.iceweasel).toBeFalsy();
        });

        it('should return false for non-Gecko browsers', function() {
            test(uas.chrome).toBeFalsy();
            test(uas.safari).toBeFalsy();
            test(uas.ie).toBeFalsy();
        });

    });

    describe('_isFirefoxFxOS', function () {

        var test = function(ua, pf) {
            return expect(window.Mozilla.Client._isFirefoxFxOS(ua, pf));
        };

        it('should return false for Firefox on desktop', function() {
            test(uas.firefox.windows, 'Win32').toBeFalsy();
            test(uas.firefox.osx, 'MacIntel').toBeFalsy();
            test(uas.firefox.linux, 'Linux i686').toBeFalsy();
        });

        it('should return false for Firefox on Maemo', function() {
            test(uas.firefox.maemo, 'Linux armv6l').toBeFalsy();
        });

        it('should return false for Firefox on Android', function() {
            test(uas.firefox.android.mobile, 'Android').toBeFalsy();
            test(uas.firefox.android.tablet, 'Android').toBeFalsy();
        });

        it('should return false for Firefox on iOS', function() {
            test(uas.firefox.ios.mobile, 'iPhone').toBeFalsy();
            test(uas.firefox.ios.tablet, 'iPod').toBeFalsy();
        });

        it('should return false for Firefox OS', function() {
            test(uas.firefox.fxos.mobile, '').toBeTruthy();
            test(uas.firefox.fxos.tablet, '').toBeTruthy();
        });

        it('should return false for other Gecko browsers', function() {
            test(uas.camino, 'MacIntel').toBeFalsy();
            test(uas.caminolikefx, 'MacIntel').toBeFalsy();
            test(uas.seamonkey, 'Win32').toBeFalsy();
            test(uas.icecat, 'Linux i686').toBeFalsy();
            test(uas.iceweasel, 'Linux i686').toBeFalsy();
        });

        it('should return false for non-Gecko browsers', function() {
            test(uas.chrome, 'Win32').toBeFalsy();
            test(uas.safari, 'MacIntel').toBeFalsy();
            test(uas.ie, 'Win32').toBeFalsy();
        });

    });

    describe('_isLikeFirefox', function() {

        var test = function(ua) {
            return expect(window.Mozilla.Client._isLikeFirefox(ua));
        };

        it('should return false for Firefox on desktop', function() {
            test(uas.firefox.windows).toBeFalsy();
            test(uas.firefox.osx).toBeFalsy();
            test(uas.firefox.linux).toBeFalsy();
        });

        it('should return false for Firefox on Maemo', function() {
            test(uas.firefox.maemo).toBeFalsy();
        });

        it('should return false for Firefox on Android', function() {
            test(uas.firefox.android.mobile).toBeFalsy();
            test(uas.firefox.android.tablet).toBeFalsy();
        });

        it('should return false for Firefox on iOS', function() {
            test(uas.firefox.ios.mobile).toBeFalsy();
            test(uas.firefox.ios.tablet).toBeFalsy();
        });

        it('should return false for Firefox OS', function() {
            test(uas.firefox.fxos.mobile).toBeFalsy();
            test(uas.firefox.fxos.tablet).toBeFalsy();
        });

        it('should return true for other Gecko browsers', function() {
            test(uas.camino).toBeTruthy();
            test(uas.caminolikefx).toBeTruthy();
            test(uas.seamonkey).toBeTruthy();
            test(uas.icecat).toBeTruthy();
            test(uas.iceweasel).toBeTruthy();
        });

        it('should return false for non-Gecko browsers', function() {
            test(uas.chrome).toBeFalsy();
            test(uas.safari).toBeFalsy();
            test(uas.ie).toBeFalsy();
        });

    });

    describe('_getFirefoxVersion', function () {

        var test = function(ua) {
            return expect(window.Mozilla.Client._getFirefoxVersion(ua));
        };

        it('should return a version number for Firefox on desktop', function() {
            test(uas.firefox.windows).toEqual('10.0');
            test(uas.firefox.osx).toEqual('23.0');
            test(uas.firefox.linux).toEqual('10.0');
        });

        it('should return a version number for Firefox on Maemo', function() {
            test(uas.firefox.maemo).toEqual('10.0.1');
        });

        it('should return a version number for Firefox on Android', function() {
            test(uas.firefox.android.mobile).toEqual('26.0');
            test(uas.firefox.android.tablet).toEqual('26.0');
        });

        it('should return 0 for Firefox on iOS', function() {
            test(uas.firefox.ios.mobile).toEqual('0');
            test(uas.firefox.ios.tablet).toEqual('0');
        });

        it('should return a version number for Firefox OS', function() {
            test(uas.firefox.fxos.mobile).toEqual('26.0');
            test(uas.firefox.fxos.tablet).toEqual('26.0');
        });

        it('should return 0 for other Gecko browsers', function() {
            test(uas.camino).toEqual('0');
            test(uas.caminolikefx).toEqual('0');
            test(uas.seamonkey).toEqual('0');
            test(uas.icecat).toEqual('0');
            test(uas.iceweasel).toEqual('0');
        });

        it('should return 0 for non-Gecko browsers', function() {
            test(uas.chrome).toEqual('0');
            test(uas.safari).toEqual('0');
            test(uas.ie).toEqual('0');
        });

    });

    describe('_getFirefoxMajorVersion', function () {

        var test = function(ua) {
            return expect(window.Mozilla.Client._getFirefoxMajorVersion(ua));
        };

        it('should return a version number for Firefox on desktop', function() {
            test(uas.firefox.windows).toEqual(10);
            test(uas.firefox.osx).toEqual(23);
            test(uas.firefox.linux).toEqual(10);
        });

        it('should return a version number for Firefox on Maemo', function() {
            test(uas.firefox.maemo).toEqual(10);
        });

        it('should return a version number for Firefox on Android', function() {
            test(uas.firefox.android.mobile).toEqual(26);
            test(uas.firefox.android.tablet).toEqual(26);
        });

        it('should return 0 for Firefox on iOS', function() {
            test(uas.firefox.ios.mobile).toEqual(0);
            test(uas.firefox.ios.tablet).toEqual(0);
        });

        it('should return a version number for Firefox OS', function() {
            test(uas.firefox.fxos.mobile).toEqual(26);
            test(uas.firefox.fxos.tablet).toEqual(26);
        });

        it('should return 0 for other Gecko browsers', function() {
            test(uas.camino).toEqual(0);
            test(uas.caminolikefx).toEqual(0);
            test(uas.seamonkey).toEqual(0);
            test(uas.icecat).toEqual(0);
            test(uas.iceweasel).toEqual(0);
        });

        it('should return 0 for non-Gecko browsers', function() {
            test(uas.chrome).toEqual(0);
            test(uas.safari).toEqual(0);
            test(uas.ie).toEqual(0);
        });

    });

    describe('_isFirefoxUpToDate', function () {

        var h = document.documentElement;

        var test = function(strict, isESR, userVer) {
            return expect(window.Mozilla.Client._isFirefoxUpToDate(strict, isESR, userVer));
        };

        beforeEach(function () {
            h.setAttribute('data-latest-firefox', '46.0.2');
            h.setAttribute('data-esr-versions', '38.8.0 45.1.0');
        });

        afterEach(function () {
            h.removeAttribute('data-latest-firefox');
            h.removeAttribute('data-esr-versions');
        });

        it('should consider up to date if user version is equal to latest version', function() {
            test(true, false, '46.0.2').toBeTruthy();
            test(true, true, '38.8.0').toBeTruthy();
            test(true, true, '45.1.0').toBeTruthy();
        });

        it('should consider up to date if user version is greater than latest version', function() {
            test(true, false, '46.0.3').toBeTruthy();
            test(true, false, '47.0').toBeTruthy();
            test(true, true, '38.9.0').toBeTruthy();
            test(true, true, '45.2.0').toBeTruthy();
        });

        it('should consider up to date if user version is slightly less than latest version but strict option is false', function() {
            test(false, false, '46.0.1').toBeTruthy();
            test(false, false, '46.0').toBeTruthy();
            test(false, true, '38.7.0').toBeTruthy();
            test(false, true, '45.0').toBeTruthy();
        });

        it('should consider outdated if user version is slightly less than latest version and strict option is true', function() {
            test(true, false, '46.0.1').toBeFalsy();
            test(true, false, '46.0').toBeFalsy();
            test(true, false, '38.7.0').toBeFalsy();
            test(true, false, '45.0').toBeFalsy();
        });

        it('should consider outdated if user version is much less than latest version, regardless of strict option', function() {
            test(true, false, '40.0.2').toBeFalsy();
            test(false, false, '40.0.2').toBeFalsy();
            test(true, true, '31.7.0').toBeFalsy();
            test(false, true, '31.7.0').toBeFalsy();
        });

    });

    describe('getFirefoxDetails', function () {

        var h = document.documentElement;

        beforeEach(function () {
            h.setAttribute('data-latest-firefox', '46.0.2');
            h.setAttribute('data-esr-versions', '38.8.0 45.1.0');
            jasmine.clock().install();
        });

        afterEach(function () {
            h.removeAttribute('data-latest-firefox');
            h.removeAttribute('data-esr-versions');
            delete window.Mozilla.Client.FirefoxDetails;
            jasmine.clock().uninstall();
        });

        it('should fire the callback function with a Firefox details object', function() {
            var callback1 = jasmine.createSpy('callback1');
            var callback2 = jasmine.createSpy('callback2');
            var result = {
                'accurate': false, // Because the mozUITour API doesn't get called in tests, this won't be true
                'version': '46.0.2',
                'channel': 'release',
                'distribution': undefined,
                'isUpToDate': true,
                'isESR': false
            };

            spyOn(window.Mozilla.Client, '_isFirefoxUpToDate').and.returnValue(true);
            spyOn(window.Mozilla.Client, '_getFirefoxVersion').and.returnValue('46.0.2');
            window.Mozilla.Client.getFirefoxDetails(callback1);
            jasmine.clock().tick(500);
            expect(callback1).toHaveBeenCalledWith(result);
            expect(window.Mozilla.Client.FirefoxDetails).toEqual(result);
            window.Mozilla.Client.getFirefoxDetails(callback2);
            jasmine.clock().tick(500);
            expect(callback2).toHaveBeenCalledWith(result);
            expect(window.Mozilla.Client._isFirefoxUpToDate.calls.count()).toEqual(1);
        });

    });

    describe('getFxaDetails', function () {

        beforeEach(function () {
            jasmine.clock().install();
        });

        afterEach(function () {
            delete window.Mozilla.Client.FxaDetails;
            jasmine.clock().uninstall();
        });

        it('should fire the callback function with a FxA details object', function() {
            var callback1 = jasmine.createSpy('callback1');

            window.Mozilla.Client.getFxaDetails(callback1);
            jasmine.clock().tick(500);
            expect(callback1).toHaveBeenCalled();
            expect(typeof window.Mozilla.Client.FxaDetails.firefox).toEqual('boolean');
            expect(typeof window.Mozilla.Client.FxaDetails.legacy).toEqual('boolean');
            expect(typeof window.Mozilla.Client.FxaDetails.mobile).toEqual('boolean');
            expect(typeof window.Mozilla.Client.FxaDetails.setup).toEqual('boolean');
            expect(typeof window.Mozilla.Client.FxaDetails.browserServices.sync.desktopDevices).toEqual('boolean');
            expect(typeof window.Mozilla.Client.FxaDetails.browserServices.sync.mobileDevices).toEqual('boolean');
            expect(typeof window.Mozilla.Client.FxaDetails.browserServices.sync.totalDevices).toEqual('boolean');
        });

        it('should identify Firefox for desktop as expected', function() {
            var callback1 = jasmine.createSpy('callback1');
            spyOn(Mozilla.Client, '_isFirefoxDesktop').and.returnValue(true);

            window.Mozilla.Client.getFxaDetails(callback1);
            jasmine.clock().tick(500);
            expect(callback1).toHaveBeenCalled();
            expect(typeof window.Mozilla.Client.FxaDetails.firefox).toBeTruthy();
        });

        it('should identify Firefox for Android as expected', function() {
            var callback1 = jasmine.createSpy('callback1');
            spyOn(Mozilla.Client, '_isFirefoxAndroid').and.returnValue(true);

            window.Mozilla.Client.getFxaDetails(callback1);
            jasmine.clock().tick(500);
            expect(callback1).toHaveBeenCalled();
            expect(window.Mozilla.Client.FxaDetails.firefox).toBeTruthy();
            expect(window.Mozilla.Client.FxaDetails.mobile).toEqual('android');
        });

        it('should identify Firefox for iOS as expected', function() {
            var callback1 = jasmine.createSpy('callback1');
            spyOn(Mozilla.Client, '_isFirefoxiOS').and.returnValue(true);

            window.Mozilla.Client.getFxaDetails(callback1);
            jasmine.clock().tick(500);
            expect(callback1).toHaveBeenCalled();
            expect(window.Mozilla.Client.FxaDetails.firefox).toBeTruthy();
            expect(window.Mozilla.Client.FxaDetails.mobile).toEqual('ios');
        });

        it('should identify legacy Firefox browsers as expected', function() {
            var callback1 = jasmine.createSpy('callback1');
            spyOn(Mozilla.Client, '_isFirefoxDesktop').and.returnValue(true);
            spyOn(Mozilla.Client, '_getFirefoxVersion').and.returnValue(Mozilla.Client.FxALastSupported - 1);

            window.Mozilla.Client.getFxaDetails(callback1);
            jasmine.clock().tick(500);
            expect(callback1).toHaveBeenCalled();
            expect(window.Mozilla.Client.FxaDetails.firefox).toBeTruthy();
            expect(window.Mozilla.Client.FxaDetails.legacy).toBeTruthy();
        });

    });

    describe('getFxaConnections', function () {

        beforeEach(function () {
            jasmine.clock().install();
        });

        afterEach(function () {
            delete window.Mozilla.Client.FxaConnections;
            jasmine.clock().uninstall();
        });

        it('should fire the callback function with a FxaConnections details object', function() {
            var callback1 = jasmine.createSpy('callback1');

            window.Mozilla.Client.getFxaConnections(callback1);
            jasmine.clock().tick(2100);
            expect(callback1).toHaveBeenCalled();
            expect(typeof window.Mozilla.Client.FxaConnections.firefox).toEqual('boolean');
            expect(typeof window.Mozilla.Client.FxaConnections.unsupported).toEqual('boolean');
            expect(typeof window.Mozilla.Client.FxaConnections.setup).toEqual('boolean');
            expect(typeof window.Mozilla.Client.FxaConnections.numOtherDevices).toEqual('boolean');
            expect(typeof window.Mozilla.Client.FxaConnections.numDevicesByType).toEqual('object');
            expect(typeof window.Mozilla.Client.FxaConnections.accountServices).toEqual('object');
        });

        it('should identify legacy Firefox browsers as expected', function() {
            var callback1 = jasmine.createSpy('callback1');
            spyOn(Mozilla.Client, '_isFirefoxDesktop').and.returnValue(true);
            spyOn(Mozilla.Client, '_getFirefoxVersion').and.returnValue(72);

            window.Mozilla.Client.getFxaConnections(callback1);
            jasmine.clock().tick(2100);
            expect(callback1).toHaveBeenCalled();
            expect(window.Mozilla.Client.FxaConnections.firefox).toBeTruthy();
            expect(window.Mozilla.Client.FxaConnections.unsupported).toBeTruthy();
        });

        it('should identify non Firefox browsers as expected', function() {
            var callback1 = jasmine.createSpy('callback1');
            spyOn(Mozilla.Client, '_isFirefoxDesktop').and.returnValue(false);

            window.Mozilla.Client.getFxaConnections(callback1);
            jasmine.clock().tick(2100);
            expect(callback1).toHaveBeenCalled();
            expect(window.Mozilla.Client.FxaConnections.firefox).toBeFalsy();
            expect(window.Mozilla.Client.FxaConnections.unsupported).toBeTruthy();
        });

    });

    describe('isFirefoxOutOfDate', function () {

        it('should return true if client version is equal to or less than the major version considered out of date', function () {
            var result = Mozilla.Client.isFirefoxOutOfDate('50.0', 2, '56.0.1');
            expect(result).toBeTruthy();

            var result2 = Mozilla.Client.isFirefoxOutOfDate('54.0', 2, '56.0');
            expect(result2).toBeTruthy();

            var result3 = Mozilla.Client.isFirefoxOutOfDate('54.0a1', 2, '56.0.1a1');
            expect(result3).toBeTruthy();

            var result4 = Mozilla.Client.isFirefoxOutOfDate('55.0.1', 1, '56.0');
            expect(result4).toBeTruthy();
        });

        it('should return false if client version is greater than the major version considered out of date', function () {
            var result = Mozilla.Client.isFirefoxOutOfDate('56.0', 2, '56.0.1');
            expect(result).toBeFalsy();

            var result2 = Mozilla.Client.isFirefoxOutOfDate('58.0a2', 2, '56.0.1');
            expect(result2).toBeFalsy();

            var result3 = Mozilla.Client.isFirefoxOutOfDate('55.0', 2, '56.0.1');
            expect(result3).toBeFalsy();

            var result4 = Mozilla.Client.isFirefoxOutOfDate('56.0', 1, '56.0.1');
            expect(result4).toBeFalsy();
        });

    });

    describe('isFirefoxURLOutOfDate', function () {

        it('should return true if URL version is equal to or less than the major version considered out of date', function () {
            var result = Mozilla.Client.isFirefoxURLOutOfDate(2, '/firefox/54.0/', '56.0');
            expect(result).toBeTruthy();

            var result2 = Mozilla.Client.isFirefoxURLOutOfDate(2, '/firefox/54.0a1/', '56.0');
            expect(result2).toBeTruthy();

            var result3 = Mozilla.Client.isFirefoxURLOutOfDate(2, '/firefox/54.0a2/', '56.0');
            expect(result3).toBeTruthy();

            var result4 = Mozilla.Client.isFirefoxURLOutOfDate(1, '/firefox/55.0.1/', '56.0');
            expect(result4).toBeTruthy();

            var result5 = Mozilla.Client.isFirefoxURLOutOfDate(2, '/firefox/53.0/', '56.0');
            expect(result5).toBeTruthy();
        });

        it('should return false if URL version is greater than the major version considered out of date', function () {
            var result = Mozilla.Client.isFirefoxURLOutOfDate(2, '/firefox/55.0/', '56.0');
            expect(result).toBeFalsy();

            var result2 = Mozilla.Client.isFirefoxURLOutOfDate(2, '/firefox/55.0a1/', '56.0');
            expect(result2).toBeFalsy();

            var result3 = Mozilla.Client.isFirefoxURLOutOfDate(2, '/firefox/55.0a2/', '56.0');
            expect(result3).toBeFalsy();

            var result4 = Mozilla.Client.isFirefoxURLOutOfDate(1, '/firefox/56.0/', '56.0.1');
            expect(result4).toBeFalsy();

            var result5 = Mozilla.Client.isFirefoxURLOutOfDate(2, '/firefox/58.0/', '56.0');
            expect(result5).toBeFalsy();
        });

        it('should return false if the URL version is invalid', function() {
            var result = Mozilla.Client.isFirefoxURLOutOfDate(2, '/firefox/foo/', '56.0');
            expect(result).toBeFalsy();

            var result2 = Mozilla.Client.isFirefoxURLOutOfDate(2, '/firefox/10/', '56.0');
            expect(result2).toBeFalsy();
        });

    });

});
