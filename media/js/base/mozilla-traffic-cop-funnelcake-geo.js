/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

/*
This library provides a common construct for running funnelcake tests via
Traffic Cop that require geolocation.

Expectations (expressed in logic below) of these kinds of tests:

- Windows
- Minimum of IE 9
- Visitor is not using Firefox
- Current URL does not contain a funnelcake param
- DNT is off
- Non-matched geo-lookup persists on client for 48 hours
*/

(function(Mozilla) {
    'use strict';

    // Traffic Cop Funnel Cake Geolocation Experiment
    var TCFCGeoExp = {};

    TCFCGeoExp.init = function(config) {
        var experimentConfig = config.experimentConfig;
        var countryCode = config.countryCode;
        var experimentId = experimentConfig.Id;
        var geoNonmatchCookieName = experimentId + '_non' + countryCode;

        // check if cookies are enabled
        var hasCookies = (typeof Mozilla.Cookies !== 'undefined' || Mozilla.Cookies.enabled());

        // all depends on cookies being enabled/available
        if (hasCookies) {
            // make sure geo lookup hasn't previously failed for this visitor
            if (TCFCGeoExp.checkGeoNonmatch(geoNonmatchCookieName)) {
                // if visitor is already in a cohort, run the experiment
                // (will send them to the same variation as before)
                if (TCFCGeoExp.checkInCohort(experimentId)) {
                    TCFCGeoExp.runExperiment(experimentConfig);
                // if visitor is not already in a cohort, make sure they are
                // eligible for the experiment. if so, perform the geo-lookup
                } else if (TCFCGeoExp.preCheckGeo()) {
                    TCFCGeoExp.geoLookup(countryCode, geoNonmatchCookieName, experimentConfig);
                }
            }
        }
    };

    // ensures current visitor did not previously fail the geo-lookup
    TCFCGeoExp.checkGeoNonmatch = function(geoNonmatchCookieName) {
        // check if user already failed geolookup
        return !Mozilla.Cookies.hasItem(geoNonmatchCookieName);
    };

    // checks to see if visitor was previously entered into a variation
    TCFCGeoExp.checkInCohort = function(experimentId) {
        // check if user already was served a variation
        return Mozilla.Cookies.hasItem(experimentId);
    };

    // checks many environmental factors to verify visitor is eligible
    TCFCGeoExp.preCheckGeo = function(ua, platform, search) {
        ua = ua || navigator.userAgent;
        platform = platform || window.site.platform;
        search = search || document.location.search;

        // make sure visitor is at least on IE 9
        var isIELT9 = /MSIE\s[1-8]\./.test(ua);

        // swiped from mozilla-client.js
        var isLikeFirefox = /Iceweasel|IceCat|SeaMonkey|Camino|like\ Firefox/i.test(ua);
        var isFirefox = /\s(Firefox|FxiOS)/.test(ua) && !isLikeFirefox;

        // check if user is on windows
        var isWindows = platform === 'windows';
        // check if current URL has a funnelcake param (in the unlikely event of navigating directly)
        var isFunnelcake = /^.*\?.*f=\d{3}.*/.test(search);
        // check if DNT is detectable and off
        var dntOk = (typeof Mozilla.dntEnabled === 'function' && !Mozilla.dntEnabled());

        return !isFunnelcake && isWindows && !isIELT9 && !isFirefox && dntOk;
    };

    // performs AJAX request to get country of current visitor
    TCFCGeoExp.geoLookup = function(countryCode, geoNonmatchCookieName, experimentConfig) {
        var xhr = new window.XMLHttpRequest();

        xhr.onload = function(r) {
            // make sure status is in the acceptable range
            if (r.target.status >= 200 && r.target.status < 300) {
                var country;

                try {
                    country = JSON.parse(r.target.responseText).country_code.toLowerCase();
                } catch (e) {
                    country = 'none';
                }

                if (country === countryCode) {
                    TCFCGeoExp.runExperiment(experimentConfig);
                } else {
                    // store cookie for two days to avoid repeated lookups
                    // that we know will fail
                    var d = new Date();
                    d.setHours(d.getHours() + 48);
                    Mozilla.Cookies.setItem(geoNonmatchCookieName, country, d);
                }
            }
        };

        xhr.open('GET', '/country-code.json');
        // must come after open call above for IE 10 & 11
        xhr.timeout = 2000;
        xhr.send();
    };

    // starts the traffic cop experiment
    TCFCGeoExp.runExperiment = function(config) {
        var rawls = new Mozilla.TrafficCop(config);
        rawls.init();
    };

    Mozilla.TCFCGeoExp = TCFCGeoExp;
})(window.Mozilla);
