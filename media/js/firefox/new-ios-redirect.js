/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function(Mozilla, site) {
    'use strict';

    if (site.platform === 'ios') {
        var referrer = window.document.referrer;
        var qs = '';
        var isSearchEngine, medium, source;

        // make sure a referrer exists
        if (referrer) {
            // get the base domain
            source = Mozilla.FirefoxNewIosRedirectHelper.getDomainFromURL(referrer);

            if (source) {
                // check if base domain is a pre-defined search engine
                isSearchEngine = Mozilla.FirefoxNewIosRedirectHelper.isSearchEngine(source);

                if (isSearchEngine) {
                    // change source to TLD-less domain (e.g. 'yahoo' instead of 'yahoo.com')
                    // this is to match existing GA conventions
                    source = isSearchEngine;
                    medium = 'organic';
                } else {
                    medium = 'referral';
                }

                qs = '?utm_source=' + encodeURIComponent(source) + '&utm_medium=' + medium;
            }
        }

        // send user to firefox iOS page
        window.location.href = window.location.protocol + '//' + window.location.host + '/firefox/ios/' + qs;
    }
})(window.Mozilla, window.site);
