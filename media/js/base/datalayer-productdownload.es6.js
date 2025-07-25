/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const TrackProductDownload = {};
const prodURL = /^https:\/\/download.mozilla.org/;
const stageURL =
    /^https:\/\/(bouncer-bouncer.stage.mozaws.net|stage.bouncer.nonprod.webservices.mozgcp.net)/;
const devURL = /^https:\/\/dev.bouncer.nonprod.webservices.mozgcp.net/;
const iTunesURL = /^https:\/\/itunes.apple.com/;
const appStoreURL = /^https:\/\/apps.apple.com/;
const playStoreURL = /^https:\/\/play.google.com/;
const marketURL = /^market:\/\/play.google.com/;
const msStoreUrl = /^https:\/\/apps.microsoft.com/;
const msStoreUrl2 = /^ms-windows-store:\/\/pdp\//;
const vpnDesktopUrl =
    /^.+\/vpn\/download\/(?<platform>mac|windows|linux)(?:\/[^]*)?\/?/;

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
            msStoreUrl.test(downloadURL) ||
            msStoreUrl2.test(downloadURL) ||
            vpnDesktopUrl.test(downloadURL)
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
 * @param {string} method - site or store
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
    eventObject['event'] = product + '_download';
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
        params = {};
    }

    let eventObject = {};

    if (vpnDesktopUrl.test(downloadURL)) {
        const platform = downloadURL.match(vpnDesktopUrl).groups.platform;
        eventObject = TrackProductDownload.getEventObject(
            'vpn',
            platform,
            'site',
            'release'
        );
    } else if (
        prodURL.test(downloadURL) ||
        stageURL.test(downloadURL) ||
        devURL.test(downloadURL)
    ) {
        // expect the link to have parameters like: ?product=firefox-beta-latest-ssl&os=osx&lang=en-US
        // extract the values we need from the parameters
        const productParam = params.product;
        const productSplit = productParam.split('-');

        // product is first word of product param
        let product = productSplit[0];
        // (except partner builds are labelled as ?product=partner-firefox so class these as regular 'firefox' download events)
        product = product === 'partner' ? 'firefox' : product;

        // platform is `os` param
        let platform = params.os;
        // change platform to macos if it's osx
        platform = platform === 'osx' ? 'macos' : platform;
        // append 'msi' to platform if msi is in the product parameter
        platform =
            productParam.indexOf('msi') !== -1 ? platform + '-msi' : platform;

        // release channel uses second word of product param
        let release = productSplit[1];
        // (except partner builds - where 'partner' is the first word)
        release = productSplit[0] === 'partner' ? 'release' : release;
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
                androidProduct = 'firefox_mobile';
                androidRelease = 'release';
                break;
            case 'org.mozilla.fenix':
                androidProduct = 'firefox_mobile';
                androidRelease = 'nightly';
                break;
            case 'org.mozilla.firefox_beta':
                androidProduct = 'firefox_mobile';
                androidRelease = 'beta';
                break;
            case 'org.mozilla.focus':
                androidProduct = 'focus';
                break;
            case 'org.mozilla.klar':
                androidProduct = 'klar';
                break;
            case 'org.mozilla.firefox.vpn':
                androidProduct = 'vpn';
                break;
        }

        eventObject = TrackProductDownload.getEventObject(
            androidProduct,
            'android',
            'store',
            androidRelease
        );
    } else if (appStoreURL.test(downloadURL) || iTunesURL.test(downloadURL)) {
        const iosProduct = params.mz_pr ? params.mz_pr : 'unrecognized';
        eventObject = TrackProductDownload.getEventObject(
            iosProduct,
            'ios',
            'store',
            'release'
        );
    } else if (msStoreUrl.test(downloadURL) || msStoreUrl2.test(downloadURL)) {
        const channel =
            params.mz_cn === 'release' || params.mz_cn === 'beta'
                ? params.mz_cn
                : 'unrecognized';
        eventObject = TrackProductDownload.getEventObject(
            'firefox',
            'win',
            'store',
            channel
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

    if (eventObject) {
        // only send event for tracking if eventObject is valid (issue 14177)
        TrackProductDownload.sendEvent(eventObject);
    }
};

/**
 * Send product_download event to glean.js
 * @param {Object} - product details formatted into a product_download event
 */
TrackProductDownload.sendGleanEvent = (eventObject) => {
    if (typeof window.Mozilla.Glean !== 'undefined') {
        /**
         * Glean is more limited when it comes to the number of
         * default click event fields, so we need to combine
         * some meta data into the label.
         */
        let label = eventObject.method;

        // release_channel is optional
        if (eventObject.release_channel) {
            label += `,${eventObject.release_channel}`;
        }

        // download_language is optional
        if (eventObject.download_language) {
            label += `,${eventObject.download_language}`;
        }

        window.Mozilla.Glean.clickEvent({
            id: eventObject.event,
            type: `${eventObject.platform}`,
            label: label
        });
    }
};

/**
 * Sends an event to the data layer
 * @param {Object} - product details formatted into a product_download event
 */
TrackProductDownload.sendEvent = (eventObject) => {
    window.dataLayer.push(eventObject);
    // we also want to keep the old event name around for a few months to help with the transition
    // this can be deleted as part of the UA cleanup
    TrackProductDownload.sendOldEvent(eventObject);

    // track event in glean.js
    TrackProductDownload.sendGleanEvent(eventObject);
};

/**
 * Sends an version of the old product_download event to the data layer
 * @param {Object} - product details formatted into a product_download event
 */
TrackProductDownload.sendOldEvent = (eventObject) => {
    // deep copy of event object
    const oldEventObject = JSON.parse(JSON.stringify(eventObject));
    // replace event name with old event name
    oldEventObject['event'] = 'product_download';
    // add to dataLayer
    window.dataLayer.push(oldEventObject);
};

export default TrackProductDownload;
