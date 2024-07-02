/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const variation = document.querySelector('main').getAttribute('data-variation');

/**
 * Update download links with the experiment and variation query parameters.
 */
function updateDownloadLinks() {
    const downloadLinks = document.querySelectorAll(
        '.c-button-download-thanks-link'
    );
    for (let i = 0; i < downloadLinks.length; ++i) {
        const link = downloadLinks[i];
        const href = link.getAttribute('href');
        if (href) {
            const separator = href.indexOf('?') !== -1 ? '&' : '?';
            link.setAttribute(
                'href',
                `${href}${separator}experiment=firefox-thanks-install-win&variation=${variation}`
            );
        }
    }
}

if (variation === '1' || variation === '2') {
    updateDownloadLinks();
}
