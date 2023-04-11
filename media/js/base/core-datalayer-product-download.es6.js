/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/*
TODO: dev and staging have different domains
FYI: can click the simple download button from a mobile device and /thanks will forward you to an app store
*/
const ProductDownloadTracking = {};

/**
 * Callback for a click event attached to a link to download.mozilla.org
 * - extracts the href of the link from an event
 * - sends it along for tracking
 * @param {Event}
 */
ProductDownloadTracking.linkHandler = (event) => {
    const downloadHref = event.target.href;
    // send to be formatted then tracked
    ProductDownloadTracking.sendDetailsFromHref(downloadHref);
};

/**
 * Validate we got a link to download.mozilla.org with the correct parameters
 * @param {URL}
 * @returns {Boolean}
 */
ProductDownloadTracking.isValidDownloadURL = (downloadHref) => {
    // check it is a URL
    try {
        new URL(downloadHref);
        // check starts with https://download.mozilla.org

        // check it has product, os, and lang parameters

        return true;
    } catch (error) {
        return false;
    }
};

/**
 * Extract the details of the product download from a link to download.mozilla.org
 * - transforms the parameters on a download link into an object
 * - sends it along for tracking
 * @param {String} -  example: https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US
 */
ProductDownloadTracking.sendDetailsFromHref = (downloadHref) => {
    // validate downloadHref before continuing
    if (!ProductDownloadTracking.isValidDownloadURL(downloadHref)) {
        return;
    }
    const downloadURL = new URL(downloadHref);

    // extract the values we need from the parameters
    const productParam = downloadURL.searchParams.get('product');
    const productSplit = productParam.split('-');
    // product is first word of product param
    const product = productSplit[0];
    // release channel is second word of product param, but use release instead of latest
    const releaseChannel =
        productSplit[1] === 'latest' ? 'release' : productSplit[1];
    // os is os
    const platform = downloadURL.searchParams.get('os');
    // lang is lang
    const lang = downloadURL.searchParams.get('lang');

    const eventObj = { event: 'product_download' };
    eventObj['product'] = product;
    eventObj['platform'] = platform;
    eventObj['release_channel'] = releaseChannel;
    eventObj['download_language'] = lang;

    // send for tracking
    ProductDownloadTracking.sendEvent(eventObj);
};

/**
 * Sends an event to the data layer
 * @param {Object} -  product details formatted into a product_download event
 */
ProductDownloadTracking.sendEvent = (details) => {
    window.dataLayer.push(details);
};

export default ProductDownloadTracking;
