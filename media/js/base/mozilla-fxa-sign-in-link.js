/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // Remove a given paramater from a URL query string
    // Taken from https://stackoverflow.com/questions/16941104/remove-a-parameter-to-the-url-with-javascript
    function removeParam(key, sourceURL) {
        var rtn = sourceURL.split('?')[0];
        var param;
        var paramsArray = [];
        var queryString = (sourceURL.indexOf('?') !== -1) ? sourceURL.split('?')[1] : '';

        if (queryString !== '') {
            paramsArray = queryString.split('&');
            for (var i = paramsArray.length - 1; i >= 0; i -= 1) {
                param = paramsArray[i].split('=')[0];
                if (param === key) {
                    paramsArray.splice(i, 1);
                }
            }
            rtn = rtn + '?' + paramsArray.join('&');
        }
        return rtn;
    }

    // Sync is Firefox only so remove the Sync params for non-Firefoxes
    if (!Mozilla.Client.isFirefox) {
        var fxaSigninLink = document.querySelectorAll('.fxa-signin > a');
        var fxaSigninURI;
        var revisedFxaSigninURI;
        var finalFxaSigninURI;

        for (var i = 0; i < fxaSigninLink.length; i++) {
            fxaSigninURI = fxaSigninLink[i].href;

            // First remove the context param
            revisedFxaSigninURI = removeParam('context', fxaSigninURI);

            // Then remove the service param
            finalFxaSigninURI = removeParam('service', revisedFxaSigninURI);

            // Set the link
            fxaSigninLink[i].href = finalFxaSigninURI;
        }
    }
})();

