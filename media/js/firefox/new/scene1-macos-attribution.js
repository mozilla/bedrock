/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var client = Mozilla.Client;

    /**
     * If on macOS and any utm_* params exist in the URL, strip the 'utm_' part and
     * append them to the download buttons pointing to /firefox/download/thanks/.
     * https://bugzilla.mozilla.org/show_bug.cgi?id=1511104
     */
    if (client.isDesktop && window.site.platform === 'osx' && document.location.search.indexOf('utm_') > -1) {
        // if the href of the download link doesn't have any query params, finalParams will default to
        // the value of utmParams. otherwise, finalParams will be a merge of download link params and
        // utmParams.
        var downloadLinks = document.getElementsByClassName('download-link');
        var finalParams = new window._SearchParams().utmParamsUnprefixed();
        var href;
        var linkParams;

        // merge the utm params from the current URL with any query params existing on in-page links
        // that point to /download/thanks/.
        for (var i = 0; i < downloadLinks.length; i++) {
            href = downloadLinks[i].href;

            // only alter links going to /firefox/download/thanks/
            if (href.indexOf('download/thanks/') > 0) {
                // if the link has a querystring, merge it with the utm_ params in the current URL
                // note: these links currently have no query params, so the code below is
                // essentially future-proofing against what could be a tough to track bug
                if (href.indexOf('?') > 0) {
                    // create an object of query params on the current href
                    linkParams = window._SearchParams.queryStringToObject(href.split('?')[1]);
                    // properties in utmParams will be overwritten by those in linkParams
                    // i.e. favor param values in the download link over those found in the querystring of the current URL (if they share a key)
                    finalParams = Object.assign(finalParams, linkParams);
                }

                downloadLinks[i].href = href.split('?')[0] + '?' + window._SearchParams.objectToQueryString(finalParams);
            }
        }
    }
})(window.Mozilla);
