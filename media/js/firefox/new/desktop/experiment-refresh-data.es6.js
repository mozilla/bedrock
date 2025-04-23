/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const href = window.location.href;

const init = () => {
    let v = '';

    if (typeof window._SearchParams !== 'undefined') {
        // get experiment variant
        const searchParams = window._SearchParams.queryStringToObject(
            href.split('?')[1]
        );
        v = searchParams.v ? searchParams.v : '';
    }

    // get download buttons
    const downloadButtons = document.querySelectorAll('.download-link');
    if (downloadButtons.length > 0) {
        for (let i = 0; i < downloadButtons.length; i++) {
            const downloadButton = downloadButtons[i];
            // add cta-name values that are cta position + experiment variant
            const ctaPosition = downloadButton.getAttribute('data-cta-position')
                ? downloadButton.getAttribute('data-cta-position')
                : 'unsupported';
            const ctaName = 'exp-new-refresh-' + v + ' : ' + ctaPosition;
            downloadButton.setAttribute('data-cta-name', ctaName);
        }
    }
};

init();
