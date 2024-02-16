/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrackProductDownload from './datalayer-productdownload.es6';

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

window.Mozilla.TrackProductDownload = TrackProductDownload;

// init tracking on links
// other methods of triggering downloads (example: /thanks) are handled separately
const productLinks = document.querySelectorAll('.ga-product-download');
for (let i = 0; i < productLinks.length; ++i) {
    productLinks[i].addEventListener(
        'click',
        function (event) {
            TrackProductDownload.handleLink(event);
        },
        false
    );
}
