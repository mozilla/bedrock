/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const SMIDownload = {};

let winDownloadID;
let macDownloadID;

SMIDownload.createCustomDownloadURL = (link, id) => {
    const url = new URL(link.href);
    url.searchParams.set('product', id);
    link.href = url;
};

SMIDownload.replaceWithCustomDownloadLinks = () => {
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

    downloadLinksWin.every((link) =>
        SMIDownload.createCustomDownloadURL(link, winDownloadID)
    );
    downloadLinksMac.every((link) =>
        SMIDownload.createCustomDownloadURL(link, macDownloadID)
    );
};

SMIDownload.init = () => {
    const strings = document.getElementById('strings');
    winDownloadID = strings.getAttribute('data-win-smi-id');
    macDownloadID = strings.getAttribute('data-mac-smi-id');

    if (typeof window.URL === 'function' && winDownloadID && macDownloadID) {
        SMIDownload.replaceWithCustomDownloadLinks();
    }
};

export default SMIDownload;
