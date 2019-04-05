/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon */

describe('core-datalayer.js', function() {

    describe('pageHasDownload', function() {

        afterEach(function() {
            $('.download').remove();
        });

        it('will return "true" when download button is present on page.', function() {
            var downloadMarkup = '<a class="download" href="#" data-link-type="download" data-download-os="Desktop">';

            $(downloadMarkup).appendTo('body');
            expect(Mozilla.Analytics.pageHasDownload()).toBe('true');
        });

        it('will return "false" when download button is not present on page.', function() {
            expect(Mozilla.Analytics.pageHasDownload()).toBe('false');
        });
    });

    describe('pageHasVideo', function() {

        afterEach(function() {
            $('#htmlPlayer').remove();
            $('#iframePlayer').remove();
        });

        it('will return "true" when HTML5 video is present on page.', function() {
            var videoMarkup = '<video id="htmlPlayer"></video>';

            $(videoMarkup).appendTo('body');
            expect(Mozilla.Analytics.pageHasVideo()).toBe('true');
        });

        it('will return "true" when YouTube iframe video is present on page.', function() {
            var videoMarkup = '<iframe id="iframePlayer" src="https://www.youtube-nocookie.com/embed/NqxUdc0P6YE?rel=0"></iframe>';

            $(videoMarkup).appendTo('body');
            expect(Mozilla.Analytics.pageHasVideo()).toBe('true');
        });

        it('will return "false" when download button is not present on page.', function() {
            expect(Mozilla.Analytics.pageHasVideo()).toBe('false');
        });
    });

    describe('getPageVersion', function() {
        it('will return the Firefox version number form the URL if present', function() {
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/107.0.11/firstrun/')).toBe('107.0.11');
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/46.0.1/firstrun/learnmore/')).toBe('46.0.1');
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/11.0/whatsnew/')).toBe('11.0');
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/46.0.1a2/firstrun/')).toBe('46.0.1a2');
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/46.0a1/whatsnew/')).toBe('46.0a1');
        });

        it('will return null if no version number present in URL', function() {
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/')).toBeNull();
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/new')).toBeNull();
            expect(Mozilla.Analytics.getPageVersion('https://www.mozilla.org/en-US/firefox/whatsnew')).toBeNull();
        });
    });

    describe('getLatestFxVersion', function() {

        afterEach(function() {
            document.getElementsByTagName('html')[0].removeAttribute('data-latest-firefox');
        });

        it('will return the Firefox version from the data-latest-firefox attribute from the html element if present', function() {
            document.getElementsByTagName('html')[0].setAttribute('data-latest-firefox', '48.0');

            expect(Mozilla.Analytics.getLatestFxVersion()).toBe('48.0');
        });

        it('will return null if no data-latest-firefox attribute is present on the html element', function() {
            expect(Mozilla.Analytics.getLatestFxVersion()).toBe(null);
        });
    });

    describe('isWin10S', function() {

        beforeEach(function () {
            window.external = sinon.stub();
            window.external.getHostEnvironmentValue = sinon.stub();
        });

        it('should return true if Windows 10 has S mode enabled', function() {
            spyOn(window.external, 'getHostEnvironmentValue').and.returnValue('{"os-mode": "2"}');
            var result = Mozilla.Analytics.isWin10S();
            expect(window.external.getHostEnvironmentValue).toHaveBeenCalledWith('os-mode');
            expect(result).toBeTruthy();
        });

        it('should return false if Windows 10 is unlocked', function() {
            spyOn(window.external, 'getHostEnvironmentValue').and.returnValue('{"os-mode": "0"}');
            var result = Mozilla.Analytics.isWin10S();
            expect(result).toBeFalsy();
        });

        it('should return false for everyone else', function() {
            spyOn(window.external, 'getHostEnvironmentValue').and.returnValue(new TypeError('window.external.getHostEnvironmentValue is not a function'));
            var result = Mozilla.Analytics.isWin10S();
            expect(result).toBeFalsy();
        });
    });

    describe('formatFxaDetails', function() {

        it('will correctly format FxA data returned from UITour', function() {

            // Current Firefox Desktop, not logged in
            var input1 = {
                'firefox': true,
                'legacy': false,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            var output1 = {
                FxALogin: false,
                FxASegment: 'Not logged in',
            };

            // Current Firefox Desktop, logged in, 1 desktop configured
            var input2 = {
                'firefox': true,
                'legacy': false,
                'mobile': false,
                'setup': true,
                'desktopDevices': 1,
                'mobileDevices': 0
            };

            var output2 = {
                FxALogin: true,
                FxAMultiDesktopSync: false,
                FxAMobileSync: false,
                FxASegment: 'Logged in'
            };

            // Current Firefox Desktop, logged in, 2 desktops configured
            var input3 = {
                'firefox': true,
                'legacy': false,
                'mobile': false,
                'setup': true,
                'desktopDevices': 2,
                'mobileDevices': 0
            };

            var output3 = {
                FxALogin: true,
                FxAMultiDesktopSync: true,
                FxAMobileSync: false,
                FxASegment: 'Multi-Desktop Sync'
            };

            // Current Firefox Desktop, logged in, 1 desktops 1 mobile configured
            var input4 = {
                'firefox': true,
                'legacy': false,
                'mobile': false,
                'setup': true,
                'desktopDevices': 1,
                'mobileDevices': 1
            };

            var output4 = {
                FxALogin: true,
                FxAMultiDesktopSync: false,
                FxAMobileSync: true,
                FxASegment: 'Desktop and Mobile Sync'
            };

            // Current Firefox Desktop, logged in, 2 desktops 1 mobile configured
            var input5 = {
                'firefox': true,
                'legacy': false,
                'mobile': false,
                'setup': true,
                'desktopDevices': 2,
                'mobileDevices': 1
            };

            var output5 = {
                FxALogin: true,
                FxAMultiDesktopSync: true,
                FxAMobileSync: true,
                FxASegment: 'Multi-Desktop and Mobile Sync'
            };

            // Firefox Desktop < 50, logged in to FxA
            var input6 = {
                'firefox': true,
                'legacy': false,
                'mobile': false,
                'setup': true,
                'desktopDevices': 'unknown',
                'mobileDevices': 'unknown'
            };

            var output6 = {
                FxALogin: true,
                FxAMobileSync:  'unknown',
                FxAMultiDesktopSync: 'unknown',
                FxASegment: 'Logged in'
            };

            // Firefox Desktop < 50, logged out
            var input7 = {
                'firefox': true,
                'legacy': false,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            var output7 = {
                FxALogin: false,
                FxASegment: 'Not logged in'
            };

            // Firefox Desktop < FxALastSupported, logged in
            var input8 = {
                'firefox': true,
                'legacy': true,
                'mobile': false,
                'setup': true,
                'desktopDevices': 'unknown',
                'mobileDevices': 'unknown'
            };

            var output8 = {
                FxALogin: true,
                FxAMobileSync:  'unknown',
                FxAMultiDesktopSync: 'unknown',
                FxASegment: 'Legacy Firefox',
            };

            // Firefox Desktop < FxALastSupported, logged out
            var input9 = {
                'firefox': true,
                'legacy': true,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            var output9 = {
                FxALogin: 'unknown',
                FxASegment: 'Legacy Firefox',
            };

            // Firefox Desktop < 29
            var input10 = {
                'firefox': true,
                'legacy': true,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            var output10 = {
                FxALogin: 'unknown',
                FxASegment: 'Legacy Firefox'
            };

            // Firefox Android
            var input11 = {
                'firefox': true,
                'legacy': false,
                'mobile': 'android',
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            var output11 = {
                FxASegment: 'Firefox Mobile'
            };

            // Firefox iOS
            var input12 = {
                'firefox': true,
                'legacy': false,
                'mobile': 'ios',
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            var output12 = {
                FxASegment: 'Firefox Mobile'
            };

            // Not Firefox
            var input13 = {
                'firefox': false,
                'legacy': false,
                'mobile': false,
                'setup': false,
                'desktopDevices': false,
                'mobileDevices': false
            };

            var output13 = {
                FxASegment: 'Not Firefox'
            };

            // we could do a loop for this but then we loose line specific error reporting
            expect(Mozilla.Analytics.formatFxaDetails(input1)).toEqual(output1);
            expect(Mozilla.Analytics.formatFxaDetails(input2)).toEqual(output2);
            expect(Mozilla.Analytics.formatFxaDetails(input3)).toEqual(output3);
            expect(Mozilla.Analytics.formatFxaDetails(input4)).toEqual(output4);
            expect(Mozilla.Analytics.formatFxaDetails(input5)).toEqual(output5);
            expect(Mozilla.Analytics.formatFxaDetails(input6)).toEqual(output6);
            expect(Mozilla.Analytics.formatFxaDetails(input7)).toEqual(output7);
            expect(Mozilla.Analytics.formatFxaDetails(input8)).toEqual(output8);
            expect(Mozilla.Analytics.formatFxaDetails(input9)).toEqual(output9);
            expect(Mozilla.Analytics.formatFxaDetails(input10)).toEqual(output10);
            expect(Mozilla.Analytics.formatFxaDetails(input11)).toEqual(output11);
            expect(Mozilla.Analytics.formatFxaDetails(input12)).toEqual(output12);
            expect(Mozilla.Analytics.formatFxaDetails(input13)).toEqual(output13);
        });
    });

    describe('updateDataLayerPush', function() {
        var linkElement;

        beforeEach(function() {
            var link = '<a id="link" href="https://www.mozilla.org/en-US/firefox/new/">';
            $(link).appendTo('body');
            linkElement = $('#link')[0];

            window.dataLayer = [];
        });

        afterEach(function() {
            $('#link').remove();
            delete window.dataLayer;
        });

        it('will add newClickHref property to link click object when pushed to the dataLayer', function() {
            Mozilla.Analytics.updateDataLayerPush('www.allizom.org');

            window.dataLayer.push({
                'event': 'gtm.linkClick',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toBeDefined();
        });

        it('will not add newClickHref property to object pushed to dataLayer if not a link click object', function() {
            Mozilla.Analytics.updateDataLayerPush('www.allizom.org');

            window.dataLayer.push({
                'event': 'gtm.click',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toBeUndefined();
        });

        it('will keep host in newClickHref when clicked link\'s href host value is different thatn the page\'s', function() {
            Mozilla.Analytics.updateDataLayerPush('www.allizom.org');

            window.dataLayer.push({
                'event': 'gtm.linkClick',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toEqual('https://www.mozilla.org/en-US/firefox/new/');
        });

        it('will remove host and locale in newClickHref when clicked link\'s href value matches the page\'s', function() {
            Mozilla.Analytics.updateDataLayerPush('www.mozilla.org');

            // Bug 1278426
            linkElement.href = 'https://www.mozilla.org:443/en-US/firefox/new/';

            window.dataLayer.push({
                'event': 'gtm.linkClick',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toEqual('/firefox/new/');
        });

        it('will remove host and non-en-US locale', function() {
            Mozilla.Analytics.updateDataLayerPush('www.mozilla.org');

            linkElement.href = 'https://www.mozilla.org:443/de/firefox/new/';

            window.dataLayer.push({
                'event': 'gtm.linkClick',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toEqual('/firefox/new/');
        });

        it('will not remove locale if absent from the URL', function() {
            Mozilla.Analytics.updateDataLayerPush('www.mozilla.org');

            linkElement.href = 'https://www.mozilla.org/firefox/new/';

            window.dataLayer.push({
                'event': 'gtm.linkClick',
                'gtm.element': linkElement
            });

            expect(window.dataLayer[0].newClickHref).toEqual('/firefox/new/');
        });
    });
});
