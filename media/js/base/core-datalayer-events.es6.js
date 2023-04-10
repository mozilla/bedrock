/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function getDownloadDetails(downloadHref) {
    const downloadURL = new URL(downloadHref);
    const productParam = downloadURL.searchParams.get('product');
    const productSplit = productParam.split('-');
    const product = productSplit[0];
    const releaseChannel =
        productSplit[1] === 'latest' ? 'release' : productSplit[1];
    const platform = downloadURL.searchParams.get('os');
    const lang = downloadURL.searchParams.get('lang');

    const eventObj = { event: 'product_download' };
    eventObj['product'] = product;
    eventObj['platform'] = platform;
    eventObj['release_channel'] = releaseChannel;
    eventObj['download_language'] = lang;

    return eventObj;
}

function pushEvent(downloadDetails) {
    //send event
    window.dataLayer.push(downloadDetails);
}

const init = () => {
    // add watcher to all links to download.mozilla.org
    const downloadLinks = document.querySelectorAll(
        'a[href^="https://download.mozilla.org/"]'
    );
    for (const downloadLink of downloadLinks) {
        downloadLink.addEventListener('click', (event) => {
            const downloadHref = event.target.href;
            const downloadDetails = getDownloadDetails(downloadHref);
            pushEvent(downloadDetails);
            // TODO: delete
            event.preventDefault();
        });
    }

    // add watcher for /thanks
};

export default init;
