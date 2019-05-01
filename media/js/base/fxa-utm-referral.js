/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {

    var UtmUrl = {};

    UtmUrl.getAttributionData = function () {
        var params = new window._SearchParams().utmParams();
        var finalParams = {};

        // utm_source
        if (params.hasOwnProperty('utm_source') && (/^[\w/.%-]+$/).test(params['utm_source'])) {
            // this value is already URI encoded, so we need to decode here as
            // it will get re-encoded in _SearchParams.objectToQueryString
            finalParams['source'] = decodeURIComponent(params['utm_source']);
            console.log(finalParams);
        }
        return Object.getOwnPropertyNames(finalParams);
    };

    UtmUrl.appendToDownloadURL = function (url, data) {
        var finalParams = data;
        var linkParams;

        if (url.indexOf('?') > 0) {
            linkParams = window._SearchParams.queryStringToObject(url.split('?')[1]);
            finalParams = Object.assign(finalParams, linkParams);
        }

        return url.split('?')[0] + '?' + window._SearchParams.objectToQueryString(finalParams);
    };

    UtmUrl.getAttributionData.init = function (){
        UtmUrl.getAttributionData();

        var ctaLinks = document.getElementsByClassName('js-fxa-cta-link');
        var url;

        for (var i = 0; i < ctaLinks.length; i++) {
            console.log(ctaLinks[i].href);
        }
    };

    UtmUrl.getAttributionData.init();

})(window.Mozilla);


// _SearchParams.objectToQueryString
// fxa_link_fragment
// /^[\w/.%-]+$/
// decodeURIComponent
// validate with regex
// before adding to fxa_link_fragment function looks for common classname on fxa_link_fragment
// query for that selector in DOM
