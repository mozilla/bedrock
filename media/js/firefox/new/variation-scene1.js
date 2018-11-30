/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/*
For 'standard' /new variations, this file will append all query params
(most importantly the 'xv' param) to download button links
so the correct template is rendered on /download/thanks/.
*/

(function() {
    'use strict';

    // copied from /firefox/new/scene1.js
    var downloadLinks = document.getElementsByClassName('download-link');
    var href;

    for (var i = 0; i < downloadLinks.length; i++) {
        // pull href for the download link
        href = downloadLinks[i].href;

        // only alter links going to download/thanks/
        if (href.indexOf('download/thanks/') > 0) {
            // update the href, skipping any utm_ params (lest we negatively impact analytics)
            downloadLinks[i].href = Mozilla.Utils.addQueryStringToUrl(href, document.location.search, true);
        }
    }
})();
