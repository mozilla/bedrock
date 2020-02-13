/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var Yandex = {
        RUSSIA_COUNTRY_CODE: 'ru',
        COOKIE_ID: 'firefox-yandex',
        COOKIE_EXPIRATION_DAYS: 3
    };

    var _client = Mozilla.Client;
    var _geoTimeout;
    var _requestComplete = false;

    Yandex.getLocation = function() {
        // should /country-code.json be slow to load,
        // just show the regular messaging after 3 seconds waiting.
        _geoTimeout = setTimeout(Yandex.onRequestComplete, 3000);

        var xhr = new window.XMLHttpRequest();

        xhr.onload = function(r) {
            var country = 'none';

            // make sure status is in the acceptable range
            if (r.target.status >= 200 && r.target.status < 300) {

                try {
                    country = JSON.parse(r.target.responseText).country_code.toLowerCase();
                } catch (e) {
                    country = 'none';
                }
            }

            Yandex.onRequestComplete(country);
        };

        xhr.open('GET', '/country-code.json');
        // must come after open call above for IE 10 & 11
        xhr.timeout = 2000;
        xhr.send();
    };

    Yandex.hasGeoOverride = function(location) {
        var loc = location || window.location.search;
        if (loc.indexOf('geo=') !== -1) {
            var urlRe = /geo=([a-z]{2})/i;
            var match = urlRe.exec(loc);
            if (match) {
                return match[1].toLowerCase();
            }
            return false;
        }
        return false;
    };

    Yandex.verifyLocation = function(location) {
        if (location) {
            return location === Yandex.RUSSIA_COUNTRY_CODE;
        }

        return false;
    };

    Yandex.onRequestComplete = function(data) {
        var country = typeof data === 'string' ? data : 'none';

        clearTimeout(_geoTimeout);

        if (!_requestComplete) {
            _requestComplete = true;

            // Set a cookie so we don't have to query location on repeated page loads.
            Yandex.setCookie(country);

            // Update page content based on location.
            Yandex.updatePageContent();
        }
    };

    Yandex.updatePageContent = function() {
        if (Yandex.shouldShowYandex()) {
            Yandex.showYandexContent();
        } else {
            Yandex.showRegularContent();
        }
    };

    Yandex.showYandexContent = function() {
        document.body.classList.add('show-yandex');

        // Update page title and description.
        document.title = Mozilla.Utils.trans('page-title');
        document.querySelector('meta[name="description"]').setAttribute('content', Mozilla.Utils.trans('page-desc'));

        window.dataLayer.push({
            'data-ex-variant': 'yandex-content',
            'data-ex-name': 'firefox-new-ru-yandex'
        });
    };

    Yandex.showRegularContent = function() {
        window.dataLayer.push({
            'data-ex-variant': 'regular-content',
            'data-ex-name': 'firefox-new-ru-yandex'
        });
    };

    Yandex.shouldShowYandex = function() {
        // Is user in Russia?
        return Yandex.verifyLocation(Yandex.getCookie(Yandex.COOKIE_ID));
    };

    Yandex.cookieExpiresDate = function(date) {
        var d = date || new Date();
        d.setTime(d.getTime() + (Yandex.COOKIE_EXPIRATION_DAYS * 24 * 60 * 60 * 1000));
        return d.toUTCString();
    };

    Yandex.setCookie = function(country) {
        Mozilla.Cookies.setItem(Yandex.COOKIE_ID, country, Yandex.cookieExpiresDate());
    };

    Yandex.getCookie = function(id) {
        return Mozilla.Cookies.getItem(id);
    };

    Yandex.hasCookie = function() {
        return Mozilla.Cookies.hasItem(Yandex.COOKIE_ID);
    };

    Yandex.init = function() {
        var cookiesEnabled = typeof Mozilla.Cookies !== 'undefined' || Mozilla.Cookies.enabled();
        var override = Yandex.hasGeoOverride();

        // only show Yandex content if on desktop with cookies enabled.
        if (_client.isDesktop && cookiesEnabled) {

            // if override URL is used, skip doing anything with cookies & show the expected content.
            if (override) {
                if (Yandex.verifyLocation(override)) {
                    Yandex.showYandexContent();
                } else {
                    Yandex.showRegularContent();
                }
            } else {
                // if user already has a cookie, use that data and update page content straight away.
                if (Yandex.hasCookie()) {
                    Yandex.updatePageContent();
                }
                // else make a remote call to query location.
                else {
                    Yandex.getLocation();
                }
            }

        } else {
            Yandex.showRegularContent();
        }
    };

    window.Mozilla.Yandex = Yandex;

})();
