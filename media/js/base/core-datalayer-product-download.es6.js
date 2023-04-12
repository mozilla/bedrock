/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const TrackProductDownload = {};

/**
 * Callback for a click event attached to a link to download.mozilla.org
 * - extracts the href of the link from an event
 * - sends it along for tracking
 * @param {Event}
 */
TrackProductDownload.linkHandler = (event) => {
    const downloadURL = event.target.href;
    // send to be formatted then tracked
    TrackProductDownload.sendDetailsFromURL(downloadURL);
};

/**
 * Validate we got a link to download.mozilla.org with the correct parameters
 * @param {URL}
 * @returns {Boolean}
 */
TrackProductDownload.isValidDownloadURL = (downloadURL) => {
    const prodURL = /^https:\/\/download.mozilla.org/;
    const stageURL = /^https:\/\/bouncer-bouncer.stage.mozaws.net/;
    if (
        typeof downloadURL === 'string' &&
        (prodURL.test(downloadURL) || stageURL.test(downloadURL))
    ) {
        // TODO check it has product, os, and lang parameters
        return true;
    } else {
        return false;
    }
};

/**
 * Extract the details of the product download from a link to download.mozilla.org
 * - transforms the parameters on a download link into an object
 * - sends it along for tracking
 * @param {String} -  example: https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US
 */
TrackProductDownload.sendDetailsFromURL = (downloadURL) => {
    // validate downloadURL before continuing
    if (!TrackProductDownload.isValidDownloadURL(downloadURL)) {
        return;
    }

    // check for SearchParams helper
    if (typeof window._SearchParams !== 'undefined') {
        // check for query string
        if (downloadURL.indexOf('?') > 0) {
            // convert query string to object
            const params = window._SearchParams.queryStringToObject(
                downloadURL.split('?')[1]
            );
            // extract the values we need from the parameters
            const productParam = params.product;
            const productSplit = productParam.split('-');
            // product is first word of product param
            const product = productSplit[0];
            // release channel is second word of product param
            // (except for release which says 'latest' but we want 'release')
            const releaseChannel =
                productSplit[1] === 'latest' ? 'release' : productSplit[1];

            // put the object together
            const eventObj = { event: 'product_download' };
            eventObj['product'] = product;
            eventObj['platform'] = params.os;
            eventObj['release_channel'] = releaseChannel;
            eventObj['download_language'] = params.lang;

            // send for tracking
            TrackProductDownload.sendEvent(eventObj);
        }
    }
};

/**
 * Sends an event to the data layer
 * @param {Object} - product details formatted into a product_download event
 */
TrackProductDownload.sendEvent = (details) => {
    window.dataLayer.push(details);
};

export default TrackProductDownload;
