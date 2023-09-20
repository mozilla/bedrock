/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const TrackProductDownload = {};
const prodURL = /^https:\/\/download.mozilla.org/;
const stageURL = /^https:\/\/bouncer-bouncer.stage.mozaws.net/;
const devURL = /^https:\/\/dev.bouncer.nonprod.webservices.mozgcp.net/;
const iTunesURL = /^https:\/\/itunes.apple.com/;
const appStoreURL = /^https:\/\/apps.apple.com/;
const playStoreURL = /^https:\/\/play.google.com/;
const marketURL = /^market:\/\/play.google.com/;
const adjustURL = /^https:\/\/app.adjust.com/;

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

/**
 * Validate we got a link to download.mozilla.org with the correct parameters
 * @param {URL}
 * @returns {Boolean}
 */
TrackProductDownload.isValidDownloadURL = (downloadURL) => {
    if (typeof downloadURL === 'string') {
        if (
            prodURL.test(downloadURL) ||
            stageURL.test(downloadURL) ||
            devURL.test(downloadURL) ||
            iTunesURL.test(downloadURL) ||
            appStoreURL.test(downloadURL) ||
            playStoreURL.test(downloadURL) ||
            marketURL.test(downloadURL) ||
            adjustURL.test(downloadURL)
        ) {
            return true;
        } else {
            return false;
        }
    } else {
        return false;
    }
};

/**
 * Create the product_download event object
 * @param {string} product
 * @param {string} platform
 * @param {string} method - site, store, or adjust
 * @param {string} release_channel - optional, we don't get it for ios downloads
 * @param {string} download_language - optional, we don't get it for mobile downloads
 * @returns {Object}
 */
TrackProductDownload.getEventObject = (
    product,
    platform,
    method,
    release_channel = false,
    download_language = false
) => {
    const eventObject = {};
    eventObject['event'] = 'product_download';
    eventObject['product'] = product;
    eventObject['platform'] = platform;
    eventObject['method'] = method;
    if (release_channel) {
        eventObject['release_channel'] = release_channel;
    }
    if (download_language) {
        eventObject['download_language'] = download_language;
    }
    return eventObject;
};

/**
 * Create the product_download event object
 * @param {string} downloadURL
 * @returns {Object}
 */
TrackProductDownload.getEventFromUrl = (downloadURL) => {
    // bail out if we don't have our helper function
    if (typeof window._SearchParams === 'undefined') {
        return false;
    }

    // bail out if the url is not what we expect
    if (!TrackProductDownload.isValidDownloadURL(downloadURL)) {
        return false;
    }

    // separate query string from URL and transform it into an object
    let params;
    if (downloadURL.indexOf('?') > 0) {
        params = window._SearchParams.queryStringToObject(
            downloadURL.split('?')[1]
        );
    } else {
        params = [];
    }

    let eventObject = {};
    if (
        prodURL.test(downloadURL) ||
        stageURL.test(downloadURL) ||
        devURL.test(downloadURL)
    ) {
        // extract the values we need from the parameters
        const productParam = params.product;
        const productSplit = productParam.split('-');
        // product is first word of product param
        const product = productSplit[0];
        let platform = params.os;
        // change platform to macos if it's osx
        platform = platform === 'osx' ? 'macos' : platform;
        // append 'msi' to platform if msi is in the product parameter
        platform =
            productParam.indexOf('msi') !== -1 ? platform + '-msi' : platform;
        // release channel is second word of product param
        let release = productSplit[1];
        // (except for latest, msi, or sub installer - we update those to say release)
        if (release === 'latest' || release === 'stub' || release === 'msi') {
            release = 'release';
        }

        eventObject = TrackProductDownload.getEventObject(
            product,
            platform,
            'site',
            release,
            params.lang
        );
    } else if (playStoreURL.test(downloadURL) || marketURL.test(downloadURL)) {
        const idParam = params.id;
        let androidProduct = 'unrecognized';
        let androidRelease = '';

        switch (idParam) {
            case 'org.mozilla.firefox':
                androidProduct = 'firefox';
                androidRelease = 'release';
                break;
            case 'org.mozilla.fenix':
                androidProduct = 'firefox';
                androidRelease = 'nightly';
                break;
            case 'org.mozilla.firefox_beta':
                androidProduct = 'firefox';
                androidRelease = 'beta';
                break;
            case 'org.mozilla.focus':
                androidProduct = 'focus';
                break;
            case 'org.mozilla.klar':
                androidProduct = 'klar';
                break;
            case 'com.ideashower.readitlater.pro':
                androidProduct = 'pocket';
                break;
        }

        eventObject = TrackProductDownload.getEventObject(
            androidProduct,
            'android',
            'store',
            androidRelease
        );
    } else if (appStoreURL.test(downloadURL) || iTunesURL.test(downloadURL)) {
        let iosProduct = 'unrecognized';
        if (downloadURL.indexOf('/id989804926') !== -1) {
            iosProduct = 'firefox';
        } else if (downloadURL.indexOf('/id1055677337') !== -1) {
            iosProduct = 'focus';
        } else if (downloadURL.indexOf('/id1073435754') !== -1) {
            iosProduct = 'klar';
        } else if (downloadURL.indexOf('/id309601447') !== -1) {
            iosProduct = 'pocket';
        }
        // Apple App Store
        eventObject = TrackProductDownload.getEventObject(
            iosProduct,
            'ios',
            'store',
            'release'
        );
    } else if (adjustURL.test(downloadURL)) {
        eventObject = TrackProductDownload.getEventObject(
            params.mz_pr,
            params.mz_pl,
            'adjust',
            'release'
        );
    }

    return eventObject;
};

/**
 * Callback for a click event attached to a link to download.mozilla.org
 * - extracts the href of the link from an event
 * - sends it along for tracking
 * @param {Event}
 */
TrackProductDownload.handleLink = (event) => {
    let el = event.target;
    // If the node isn't a link traverse up
    // but closest is not supported in IE
    // but this code should only run on the app store links because of the images
    // so it's okay to not track IE users going to the App Stores IMHO
    if (el.nodeName !== 'A' && Element.prototype.closest) {
        el = el.closest('a');
    } else if (!Element.prototype.closest) {
        return false;
    }
    const downloadURL = el.href;
    // send to be formatted then tracked
    TrackProductDownload.sendEventFromURL(downloadURL);
};

/**
 * @param {String} -  example: https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US
 */
TrackProductDownload.sendEventFromURL = (downloadURL) => {
    // get event object
    const eventObject = TrackProductDownload.getEventFromUrl(downloadURL);
    // send for tracking
    TrackProductDownload.sendEvent(eventObject);
};

/**
 * Sends an event to the data layer
 * @param {Object} - product details formatted into a product_download event
 */
TrackProductDownload.sendEvent = (eventObject) => {
    window.dataLayer.push(eventObject);
};

export default TrackProductDownload;
