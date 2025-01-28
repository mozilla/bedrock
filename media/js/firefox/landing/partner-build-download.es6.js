/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const PartnerBuildDownload = {};

let winDownloadID;
let macDownloadID;

PartnerBuildDownload.createCustomDownloadURL = (link, id) => {
    const url = new URL(link.href);

    // partner builds are 404 on staging, so make sure we point to prod.
    url.hostname = 'download.mozilla.org';

    // update product to custom build ID.
    url.searchParams.set('product', id);

    link.href = url;
};

PartnerBuildDownload.replaceWithCustomDownloadLinks = () => {
    const downloadLinksWin = Array.from(
        document.querySelectorAll(
            '.download-button .download-list .download-link[data-download-version="win"]'
        )
    );
    const downloadLinksMac = Array.from(
        document.querySelectorAll(
            '.download-button .download-list .download-link[data-download-version="osx"]'
        )
    );

    downloadLinksWin.forEach((link) =>
        PartnerBuildDownload.createCustomDownloadURL(link, winDownloadID)
    );
    downloadLinksMac.forEach((link) =>
        PartnerBuildDownload.createCustomDownloadURL(link, macDownloadID)
    );
};

PartnerBuildDownload.init = () => {
    const strings = document.getElementById('strings');
    winDownloadID = strings.getAttribute('data-win-custom-id');
    macDownloadID = strings.getAttribute('data-mac-custom-id');

    if (
        typeof window.URL === 'function' &&
        typeof Array.from === 'function' &&
        winDownloadID &&
        macDownloadID
    ) {
        PartnerBuildDownload.replaceWithCustomDownloadLinks();
    }
};

export default PartnerBuildDownload;
