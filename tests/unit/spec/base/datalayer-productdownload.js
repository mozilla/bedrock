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
        const testDownloadURL = TrackProductDownload.isValidDownloadURL(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US'
        );
        expect(testDownloadURL).toBe(true);
    });
    it('should recognize bouncer stage as a valid URL', function () {
        const testBouncerURL = TrackProductDownload.isValidDownloadURL(
            'https://bouncer-bouncer.stage.mozaws.net/?product=firefox-latest-ssl&os=osx&lang=en-US'
        );
        expect(testBouncerURL).toBe(true);
    });
    it('should recognize bouncer dev as a valid URL', function () {
        const testBouncerURL = TrackProductDownload.isValidDownloadURL(
            'https://dev.bouncer.nonprod.webservices.mozgcp.net/?product=firefox-latest-ssl&os=osx&lang=en-US'
        );
        expect(testBouncerURL).toBe(true);
    });
    it('should recognize the App Store as a valid URL', function () {
        const testAppStoreURL = TrackProductDownload.isValidDownloadURL(
            'https://itunes.apple.com/app/firefox-private-safe-browser/id989804926'
        );
        expect(testAppStoreURL).toBe(true);
    });
    it('should recognize the Play Store as a valid URL', function () {
        const testPlayStoreURL = TrackProductDownload.isValidDownloadURL(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org'
        );
        expect(testPlayStoreURL).toBe(true);
    });
    it('should recognize the Android Market as a valid URL', function () {
        const testPlayStoreURL = TrackProductDownload.isValidDownloadURL(
            'market://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org'
        );
        expect(testPlayStoreURL).toBe(true);
    });
    it('should not accept a random link to mozilla.org as a valid URL', function () {
        const testRandomURL = TrackProductDownload.isValidDownloadURL(
            'https://www.mozilla.org/en-US/firefox/all/'
        );
        expect(testRandomURL).toBe(false);
    });
});

describe('TrackProductDownload.getEventObject', function () {
    it('should insert parameters into the proper place in the event object', function () {
        const testFullEventExpectedObject = {
            event: 'testProduct_download',
            product: 'testProduct',
            platform: 'testPlatform',
            method: 'testMethod',
            release_channel: 'testReleaseChannel',
            download_language: 'testDownloadLanguage'
        };
        const testFullEventObject = TrackProductDownload.getEventObject(
            'testProduct',
            'testPlatform',
            'testMethod',
            'testReleaseChannel',
            'testDownloadLanguage'
        );
        expect(testFullEventObject).toEqual(testFullEventExpectedObject);
    });
    it('should create an event object even if there are no release_channel or download_language parameters', function () {
        const testShortEventExpectedObject = {
            event: 'testProduct_download',
            product: 'testProduct',
            platform: 'testPlatform',
            method: 'testMethod'
        };
        const testShortEventObject = TrackProductDownload.getEventObject(
            'testProduct',
            'testPlatform',
            'testMethod'
        );
        expect(testShortEventObject).toEqual(testShortEventExpectedObject);
    });
});

describe('TrackProductDownload.getEventFromUrl', function () {
    // product
    it('should identify product for Firefox Desktop', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US&_gl=1&234*_ga*ABC'
        );
        expect(testEvent['product']).toBe('firefox');
    });
    it('should identify product for Firefox in the App Store', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/app/firefox-private-safe-browser/id989804926'
        );
        expect(testEvent['product']).toBe('firefox_mobile');
    });
    it('should identify product for Firefox in the Play Store', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org'
        );
        expect(testEvent['product']).toBe('firefox_mobile');
    });
    it('should identify product for Pocket in the App Store', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/{country}/app/pocket-save-read-grow/id309601447'
        );
        expect(testEvent['product']).toBe('pocket');
    });
    it('should identify product for Pocket in the Play Store', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=com.ideashower.readitlater.pro'
        );
        expect(testEvent['product']).toBe('pocket');
    });
    it('should identify product for Focus in the App Store', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/{country}/app/firefox-focus-privacy-browser/id1055677337'
        );
        expect(testEvent['product']).toBe('focus');
    });
    it('should identify product for Focus in the Play Store', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.focus'
        );
        expect(testEvent['product']).toBe('focus');
    });
    it('should identify product for Klar in the App Store', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/{country}/app/klar-by-firefox/id1073435754'
        );
        expect(testEvent['product']).toBe('klar');
    });
    it('should identify product for Klar in the Play Store', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.klar'
        );
        expect(testEvent['product']).toBe('klar');
    });
    it('should identify product as unrecognized if App Store link is not found', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/us/app/49th-parallel-coffee-roasters/id1567407403'
        );
        expect(testEvent['product']).toBe('unrecognized');
    });
    it('should identify product as unrecognized if Play Store link is not found', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=co.tapcart.app.id_rBugj0qbKV'
        );
        expect(testEvent['product']).toBe('unrecognized');
    });
    // platform
    it('should identify platform for Firefox for Windows', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US&_gl=1&234*_ga*ABC'
        );
        expect(testEvent['platform']).toBe('win64');
    });
    it('should identify platform for Firefox for MacOS', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US'
        );
        expect(testEvent['platform']).toBe('macos');
    });
    it('should identify platform for Firefox for Linux', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US'
        );
        expect(testEvent['platform']).toBe('linux64');
    });
    it('should identify platform for msi', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-msi-latest-ssl&os=win64&lang=en-US'
        );
        expect(testEvent['platform']).toBe('win64-msi');
    });
    it('should identify platform for esr msi', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-esr-msi-latest-ssl&os=win64&lang=en-US'
        );
        expect(testEvent['platform']).toBe('win64-msi');
    });
    it('should identify platform for Firefox in the App Store', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/app/firefox-private-safe-browser/id989804926'
        );
        expect(testEvent['platform']).toBe('ios');
    });
    it('should identify platform for Firefox in the Play Store', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org'
        );
        expect(testEvent['platform']).toBe('android');
    });
    // release channel
    it('should identify release_channel for Firefox Release', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US&_gl=1&234*_ga*ABC'
        );
        expect(testEvent['release_channel']).toBe('release');
    });
    it('should identify release_channel for Firefox Beta', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-beta-latest-ssl&os=osx&lang=en-US'
        );
        expect(testEvent['release_channel']).toBe('beta');
    });
    it('should identify release_channel for Firefox Dev Edition', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-devedition-latest-ssl&os=osx&lang=en-US'
        );
        expect(testEvent['release_channel']).toBe('devedition');
    });
    it('should identify release_channel for Firefox Nightly', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-nightly-latest-ssl&os=osx&lang=en-US'
        );
        expect(testEvent['release_channel']).toBe('nightly');
    });
    it('should identify release_channel for Firefox ESR', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-esr-latest-ssl&os=osx&lang=en-US'
        );
        expect(testEvent['release_channel']).toBe('esr');
    });
    it('should identify release_channel for Firefox MSI', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-msi-latest-ssl&os=win64&lang=en-US'
        );
        expect(testEvent['release_channel']).toBe('release');
    });
    it('should identify release_channel for Firefox ESR', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-esr-latest-ssl&os=win64&lang=en-US'
        );
        expect(testEvent['release_channel']).toBe('esr');
    });
    it('should identify release_channel for Firefox iOS', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/app/firefox-private-safe-browser/id989804926'
        );
        expect(testEvent['release_channel']).toBe('release');
    });
    it('should identify release_channel for Firefox Android Release', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org'
        );
        expect(testEvent['release_channel']).toBe('release');
    });
    it('should identify release_channel for Firefox Android Beta', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox_beta'
        );
        expect(testEvent['release_channel']).toBe('beta');
    });
    it('should identify release_channel for Firefox Android Nightly', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.fenix'
        );
        expect(testEvent['release_channel']).toBe('nightly');
    });
    // language
    it('should identify en-US for Firefox Desktop', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US&_gl=1&234*_ga*ABC'
        );
        expect(testEvent['download_language']).toBe('en-US');
    });
    it('should identify DE for Firefox Desktop', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=de'
        );
        expect(testEvent['download_language']).toBe('de');
    });
    it('should not identify language for Firefox iOS', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://itunes.apple.com/app/firefox-private-safe-browser/id989804926'
        );
        expect(testEvent['download_language']).toBeFalsy();
    });
    it('should not identify language for Firefox Android', function () {
        const testEvent = TrackProductDownload.getEventFromUrl(
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dmozilla%26utm_medium%3DReferral%26utm_campaign%3Dmozilla-org'
        );
        expect(testEvent['download_language']).toBeFalsy();
    });
});

describe('TrackProductDownload.handleLink', function () {
    const download_button = `<a href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win64&amp;lang=en-CA" id="download-button-primary" class="mzp-c-button mzp-t-product c-download-button">Download Now</a>`;

    beforeEach(function () {
        // stub out google tag manager
        window.dataLayer = sinon.stub();
        window.dataLayer.push = sinon.stub();

        document.body.insertAdjacentHTML('beforeend', download_button);
        const downloadButton = document.getElementById(
            'download-button-primary'
        );
        downloadButton.addEventListener(
            'click',
            function (event) {
                event.preventDefault();
                TrackProductDownload.handleLink(event);
            },
            false
        );
    });

    afterEach(function () {
        document.getElementById('download-button-primary').remove();
    });

    it('should call the full chain of functions', function () {
        spyOn(TrackProductDownload, 'handleLink').and.callThrough();
        spyOn(TrackProductDownload, 'sendEventFromURL').and.callThrough();
        spyOn(TrackProductDownload, 'isValidDownloadURL').and.callThrough();
        spyOn(TrackProductDownload, 'getEventObject').and.callThrough();
        spyOn(TrackProductDownload, 'sendEvent').and.callThrough();

        document.getElementById('download-button-primary').click();

        expect(TrackProductDownload.handleLink).toHaveBeenCalled();
        expect(TrackProductDownload.sendEventFromURL).toHaveBeenCalled();
        expect(TrackProductDownload.isValidDownloadURL).toHaveBeenCalled();
        expect(TrackProductDownload.getEventObject).toHaveBeenCalled();
        expect(TrackProductDownload.sendEvent).toHaveBeenCalledWith({
            event: 'firefox_download',
            product: 'firefox',
            platform: 'win64',
            method: 'site',
            release_channel: 'release',
            download_language: 'en-CA'
        });
    });
});
