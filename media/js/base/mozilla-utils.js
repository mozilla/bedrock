/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function() {
    'use strict';

    var Utils = {};

    // Replace Google Play links on Android devices to let them open the marketplace app
    Utils.initMobileDownloadLinks = function() {
        if (site.platform === 'android') {
            $('a[href^="https://play.google.com/store/apps/"]').each(function() {
                $(this).attr('href', $(this).attr('href')
                    .replace('https://play.google.com/store/apps/', 'market://'));
            });
        }
    };

    // Bug 1264843: link to China build of Fx4A, for display within Fx China repack
    Utils.maybeSwitchToDistDownloadLinks = function(client) {
        if (!client.distribution || client.distribution === 'default') {
            return;
        }

        var distribution = client.distribution.toLowerCase();
        $('a[data-' + distribution + '-link]').each(function() {
            $(this).attr('href', $(this).data(distribution + 'Link'));
        });
        $('img[data-' + distribution + '-link]').each(function() {
            $(this).attr('src', $(this).data(distribution + 'Link'));
        });
    };

    Utils.switchPathLanguage = function(location, newLang) {
        // get path without locale
        var urlpath = location.pathname.slice(1).split('/').slice(1).join('/');
        return '/' + newLang + '/' + urlpath + location.search;
    };

    // language switcher
    Utils.initLangSwitcher = function() {
        var $language = $('#page-language-select');
        var previousLanguage = $language.val();
        $language.on('change', function() {
            var newLanguage = $language.val();
            window.dataLayer.push({
                'event': 'change-language',
                'languageSelected': newLanguage,
                'previousLanguage': previousLanguage
            });
            Utils.doRedirect(Utils.switchPathLanguage(window.location, newLanguage));
        });
    };

    // client-side redirects (handy for testing)
    Utils.doRedirect = function(destination) {
        if (destination) {
            window.location.href = destination;
        }
    };

    // Create text translation function using #strings element.
    // TODO: Move to docs
    // In order to use it, you need a block string_data bit inside your template,
    // then, each key name needs to be preceded by data- as this uses data attributes
    // to work. After this, you can access all strings defined inside the
    // string_data block in JS using Mozilla.Utils.trans('keyofstring'); Thank @mkelly
    var _$strings = $('#strings');
    Utils.trans = function(stringId) {
        return _$strings.data(stringId);
    };

    Utils.queryStringToObject = function(queryString, skipUtmParams) {
        var keyVals;
        var keyValParts;
        var obj = {};
        var i;
        var plusIndex;

        // ignore preceeding '?' (if present)
        if (queryString.indexOf('?') > -1) {
            queryString = queryString.split('?')[1];
        }

        // split into an array of key=val items
        keyVals = queryString.split('&');

        for (i = 0; i < keyVals.length; i++) {
            // for some links, we don't want to add utm params
            // TODO: update tests
            if (skipUtmParams && keyVals[i].indexOf('utm_') === 0) {
                continue;
            }

            // find out where in the key=val pair the first = sign sits
            // (indexOf finds the first occurrence)
            plusIndex = keyVals[i].indexOf('=');

            // skip malformed parts of the query string
            // the first '=' must be present and not at the start or end of the string
            if (plusIndex > 0 && plusIndex < keyVals[i].length - 1) {
                // TODO: can there be more than one = sign in a key/val pair?
                keyValParts = keyVals[i].split('=');
                obj[keyValParts[0]] = keyValParts[1];
            }
        }

        return obj;
    };

    /**
     *
     * @param {String} url - Any URL
     * @param {String} queryString - A URL formatted querystring, e.g. walter=calm&dude=abides. Preceeding '?' is optional.
     */
    Utils.addQueryStringToUrl = function(url, queryString, skipUtmParams) {
        // all potentially required vars
        var baseUrl;
        var urlParams = {};
        var qsParams = {};
        var mergedParams;
        var finalQs = '';

        // ensure querySting has the preceeding '?' (for consistency)
        if (queryString.indexOf('?') !== 0) {
            queryString = '?' + queryString;
        }

        // first, check to see if url already has query params
        if (url.indexOf('?')) {
            // if so, get the base URL
            baseUrl = url.split('?')[0];

            // convert the querystrings to objects for easy merging
            urlParams = Mozilla.Utils.queryStringToObject(url);
            qsParams = Mozilla.Utils.queryStringToObject(queryString, skipUtmParams);

            // merge the two objects, favoring values in url over queryString
            // (e.g. if a property exists in both, the value in url wins out)
            mergedParams = Object.assign(qsParams, urlParams);

            // construct a querystring from the merged params
            for (var key in mergedParams) {
                if (mergedParams.hasOwnProperty(key)) {
                    finalQs += key + '=' + mergedParams[key] + '&';
                }
            }

            // remove the trailing '&'
            finalQs = finalQs.slice(0, -1);

            // finally, append the constructed querystring on to the base url
            url = baseUrl + '?' + finalQs;
            // if url does not have query params, we just need to append the
        } else {
            url += queryString;
        }

        return url;
    };

    window.Mozilla.Utils = Utils;

})();
