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

    var downloadLinks = document.getElementsByClassName('download-link');
    var finalParams = {};
    var href;
    var linkParams;
    var linkRoot;
    var params = new window._SearchParams().params;

    // we need to propogate 'v' and/or 'xv' query params to ensure the correct template is loaded on /download/thanks/
    if (params.hasOwnProperty('v')) {
        finalParams.v = params['v'];
    }

    if (params.hasOwnProperty('xv')) {
        finalParams.xv = params['xv'];
    }

    // merge the utm params from the current URL with any query params existing on in-page links
    // that point to /download/thanks/.
    for (var i = 0; i < downloadLinks.length; i++) {
        href = downloadLinks[i].href;
        linkRoot = href.split('?')[0];

        // only alter links going to /firefox/download/thanks/
        if (href.indexOf('download/thanks/') > 0) {
            // if the link has a querystring, merge it with the utm params from the current URL
            // note: these links currently have no query params, so the code below is
            // essentially future-proofing against what could be a tough to track bug
            if (href.indexOf('?') > 0) {
                // create an object of query params on the current href
                linkParams = window._SearchParams.queryStringToObject(href.split('?')[1]);
                // properties in finalParams will be overwritten by those in linkParams
                // i.e. favor query param values in the download link over those found in the querystring of the current URL if they share a key
                finalParams = Object.assign(finalParams, linkParams);
            }

            downloadLinks[i].href = linkRoot + '?' + window._SearchParams.objectToQueryString(finalParams);
        }
    }
})();
