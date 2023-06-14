/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import TrackProductDownload from '../../../../media/js/base/datalayer-productdownload.es6.js';

describe('TrackProductDownload.isValidDownloadURL', function () {
    it('should recognize downloads.m.o as a valid URL', function () {
        let testDownloadURL = TrackProductDownload.isValidDownloadURL(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US'
        );
        expect(testDownloadURL).toBe(true);
    });
    it('should recognize bouncer as a valid URL', function () {
        let testBouncerURL = TrackProductDownload.isValidDownloadURL(
            'https://bouncer-bouncer.stage.mozaws.net/?product=firefox-latest-ssl&os=osx&lang=en-US'
        );
        expect(testBouncerURL).toBe(true);
    });
    it('should recognize the App Store as a valid URL', function () {
        let testAppStoreURL = TrackProductDownload.isValidDownloadURL(
            'https://itunes.apple.com/app/firefox-private-safe-browser/id989804926'
        );
        expect(testAppStoreURL).toBe(true);
    });
    it('should recognize the Play Store as a valid URL', function () {
        let testPlayStoreURL = TrackProductDownload.isValidDownloadURL(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org'
        );
        expect(testPlayStoreURL).toBe(true);
    });
    it('should not accept Adjust as a valid URL', function () {
        let testAdjustURL = TrackProductDownload.isValidDownloadURL(
            'https://app.adjust.com/2uo1qc?redirect=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dorg.mozilla.firefox&campaign=www.mozilla.org&adgroup=mobile-android-page'
        );
        expect(testAdjustURL).toBe(false);
    });
    it('should not accept a random link to mozilla.org as a valid URL', function () {
        let testRandomURL = TrackProductDownload.isValidDownloadURL(
            'https://www.mozilla.org/en-US/firefox/all/'
        );
        expect(testRandomURL).toBe(false);
    });
});

describe('TrackProductDownload.getEventObject', function () {
    it('should insert parameters into the proper place in the event object', function () {
        let testFullEventExpectedObject = {
            event: 'product_download',
            product: 'testProduct',
            platform: 'testPlatform',
            release_channel: 'testReleaseChannel',
            download_language: 'testDownloadLanguage'
        };
        let testFullEventObject = TrackProductDownload.getEventObject(
            'testProduct',
            'testPlatform',
            'testReleaseChannel',
            'testDownloadLanguage'
        );
        expect(testFullEventObject).toEqual(testFullEventExpectedObject);
    });
    it('should create an event object even if there are no release_channel or download_language parameters', function () {
        let testShortEventExpectedObject = {
            event: 'product_download',
            product: 'testProduct',
            platform: 'testPlatform',
            release_channel: '',
            download_language: ''
        };
        let testShortEventObject = TrackProductDownload.getEventObject(
            'testProduct',
            'testPlatform'
        );
        expect(testShortEventObject).toEqual(testShortEventExpectedObject);
    });
});

describe('TrackProductDownload.getEventFromUrl', function () {
    // product
    it('should identify product for Firefox Desktop', function () {
        let testProductDesktop = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US&_gl=1&234*_ga*ABC'
        );
        expect(testProductDesktop['product']).toBe('firefox');
    });
    it('should identify product for Firefox iOS', function () {
        let testProductIOS = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/app/firefox-private-safe-browser/id989804926'
        );
        expect(testProductIOS['product']).toBe('firefox');
    });
    it('should identify product for Firefox Android', function () {
        let testProductAndroid = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org'
        );
        expect(testProductAndroid['product']).toBe('firefox');
    });
    // platform
    it('should identify platform for Windows', function () {
        let testPlatformWindows = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US&_gl=1&234*_ga*ABC'
        );
        expect(testPlatformWindows['platform']).toBe('win64');
    });
    it('should identify platform for MacOS', function () {
        let testPlatformMacOS = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US'
        );
        expect(testPlatformMacOS['platform']).toBe('macos');
    });
    it('should identify platform for Linux', function () {
        let testPlatformLinux = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US'
        );
        expect(testPlatformLinux['platform']).toBe('linux64');
    });
    it('should identify platform for iOS', function () {
        let testPlatformIOS = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/app/firefox-private-safe-browser/id989804926'
        );
        expect(testPlatformIOS['platform']).toBe('ios');
    });
    it('should identify platform for Android', function () {
        let testPlatformAndroid = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org'
        );
        expect(testPlatformAndroid['platform']).toBe('android');
    });
    // release channel
    it('should identify release_channel for Firefox Release', function () {
        let testReleaseRelease = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US&_gl=1&234*_ga*ABC'
        );
        expect(testReleaseRelease['release_channel']).toBe('release');
    });
    it('should identify release_channel for Firefox Beta', function () {
        let testBetaRelease = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-beta-latest-ssl&os=osx&lang=en-US'
        );
        expect(testBetaRelease['release_channel']).toBe('beta');
    });
    it('should identify release_channel for Firefox Dev Edition', function () {
        let testDevRelease = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-devedition-latest-ssl&os=osx&lang=en-US'
        );
        expect(testDevRelease['release_channel']).toBe('devedition');
    });
    it('should identify release_channel for Firefox Nightly', function () {
        let testNightlyRelease = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-nightly-latest-ssl&os=osx&lang=en-US'
        );
        expect(testNightlyRelease['release_channel']).toBe('nightly');
    });
    it('should identify release_channel for Firefox ESR', function () {
        let testNightlyRelease = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-esr-latest-ssl&os=osx&lang=en-US'
        );
        expect(testNightlyRelease['release_channel']).toBe('esr');
    });
    it('should identify release_channel for Firefox iOS', function () {
        let testIOSRelease = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/app/firefox-private-safe-browser/id989804926'
        );
        expect(testIOSRelease['release_channel']).toBe('release');
    });
    it('should identify release_channel for Firefox Android Release', function () {
        let testAndroidRelease = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org'
        );
        expect(testAndroidRelease['release_channel']).toBe('release');
    });
    it('should identify release_channel for Firefox Android Beta', function () {
        let testAndroidBetaRelease = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox_beta'
        );
        expect(testAndroidBetaRelease['release_channel']).toBe('beta');
    });
    it('should identify release_channel for Firefox Android Nightly', function () {
        let testAndroidNightlyRelease = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.fenix'
        );
        expect(testAndroidNightlyRelease['release_channel']).toBe('nightly');
    });
    // language
    it('should identify en-US for Firefox Desktop', function () {
        let testLanguageDesktop = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US&_gl=1&234*_ga*ABC'
        );
        expect(testLanguageDesktop['download_language']).toBe('en-US');
    });
    it('should identify DE for Firefox Desktop', function () {
        let testLanguageDesktop = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=de'
        );
        expect(testLanguageDesktop['download_language']).toBe('de');
    });
    it('should not identify language for Firefox iOS', function () {
        let testLanguageIOS = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/app/firefox-private-safe-browser/id989804926'
        );
        expect(testLanguageIOS['download_language']).toBeFalsy();
    });
    it('should not identify language for Firefox Android', function () {
        let testLanguageAndroid = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org'
        );
        expect(testLanguageAndroid['download_language']).toBeFalsy();
    });
});

describe('TrackProductDownload.linkHandler', function () {
    const download_button = `<a href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win64&amp;lang=en-CA" id="download-button-primary" class="mzp-c-button mzp-t-product c-download-button">Download Now</a>`;

    beforeEach(function () {
        window.dataLayer = [];

        document.body.insertAdjacentHTML('beforeend', download_button);
        const downloadButton = document.getElementById(
            'download-button-primary'
        );
        downloadButton.addEventListener(
            'click',
            function (event) {
                event.preventDefault();
                TrackProductDownload.linkHandler(event);
            },
            false
        );
    });

    afterEach(function () {
        document.getElementById('download-button-primary').remove();
        window.dataLayer = [];
    });

    it('should call the full chain of functions', function () {
        spyOn(TrackProductDownload, 'linkHandler').and.callThrough();
        spyOn(TrackProductDownload, 'sendEventFromURL').and.callThrough();
        spyOn(TrackProductDownload, 'isValidDownloadURL').and.callThrough();
        spyOn(TrackProductDownload, 'getEventObject').and.callThrough();
        spyOn(TrackProductDownload, 'sendEvent').and.callThrough();

        document.getElementById('download-button-primary').click();

        expect(TrackProductDownload.linkHandler).toHaveBeenCalled();
        expect(TrackProductDownload.sendEventFromURL).toHaveBeenCalled();
        expect(TrackProductDownload.isValidDownloadURL).toHaveBeenCalled();
        expect(TrackProductDownload.getEventObject).toHaveBeenCalled();
        expect(TrackProductDownload.sendEvent).toHaveBeenCalledWith({
            event: 'product_download',
            product: 'firefox',
            platform: 'win64',
            release_channel: 'release',
            download_language: 'en-CA'
        });
    });
});
