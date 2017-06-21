/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var experimentId = 'experiment_search_retention_funnelcake';
    var geoNonmatchCookie = experimentId + '_nonUS';

    // IE 9 can't handle the truth
    var isIELT10 = /MSIE\s[1-9]\./.test(navigator.userAgent);

    // swiped from mozilla-client.js
    var ua = navigator.userAgent;
    var isLikeFirefox = /Iceweasel|IceCat|SeaMonkey|Camino|like\ Firefox/i.test(ua);
    var isFirefox = /\s(Firefox|FxiOS)/.test(ua) && !isLikeFirefox;
    var isMobile = /^(android|ios|fxos)$/.test(window.site.platform);

    // check if cookies are enabled
    var hasCookies = (typeof Mozilla.Cookies !== 'undefined' || Mozilla.Cookies.enabled());
    // check if user already was served a variation
    var hasVariationCookie = hasCookies && Mozilla.Cookies.hasItem(experimentId);
    // check if user already failed geolookup
    var hasGeoNonmatchCookie = hasCookies && Mozilla.Cookies.hasItem(geoNonmatchCookie);
    // check if user is on windows
    var isWindows = window.site.platform === 'windows';
    // check if current URL has a funnelcake param (in the unlikely event of navigating directly)
    var isFunnelcake = /^.*\?.*f=\d{3}.*/.test(document.location.search);
    // check if DNT is detectable and off
    var dntOk = (typeof Mozilla.dntEnabled === 'function' && !Mozilla.dntEnabled());

    // 0. if visitor previously failed the geolookup, skip everything
    if (hasGeoNonmatchCookie) {
        return;
    }

    // 1. if visitor already has a cookie for this experiment, skip the expensive
    // checks below and run experiment (uses variation in the cookie)
    if (hasVariationCookie) {
        runExperiment();
    }
    // 2. experiment criteria prior to expensive geolookup check:
    //      a. is not currently on a funnelcake URL (sanity infinite loop check)
    //      b. is on Windows
    //      c. on IE 10 or greater
    //      d. is not on Firefox
    //      e. is not on a mobile browser
    //      f. DNT is detectable and off
    else if (!isFunnelcake && isWindows && !isIELT10 && !isFirefox && !isMobile && dntOk) {
        // 2. check geolocation for US
        var xhr = new XMLHttpRequest();

        xhr.onload = function(r) {
            // make sure status is in the acceptable range
            if (r.target.status >= 200 && r.target.status < 300) {
                var country;

                try {
                    country = JSON.parse(r.target.response).country_code.toLowerCase();
                } catch (e) {
                    country = 'none';
                }

                if (country === 'us') {
                    runExperiment();
                } else {
                    if (hasCookies) {
                        // store cookie for two days to avoid repeated lookups
                        // that we know will fail
                        var d = new Date();
                        d.setHours(d.getHours() + 48);
                        Mozilla.Cookies.setItem(geoNonmatchCookie, country, d);
                    }
                }
            }
        };

        xhr.open('GET', '/country-code.json');
        // must come after open call above for IE 10 & 11
        xhr.timeout = 2000;
        xhr.send();
    }

    function runExperiment() {
        var landsman = new Mozilla.TrafficCop({
            id: experimentId,
            variations: {
                'f=114': 9,
                'f=115': 9,
                'f=116': 34,
                'f=117': 9,
                'f=118': 34
            }
        });

        landsman.init();
    }
})(window.Mozilla);
