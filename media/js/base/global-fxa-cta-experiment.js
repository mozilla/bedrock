/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * Global FxA CTA experiment: issue #6629
 */
(function() {
    'use strict';

    var SAMPLE_RATE = 0.9; // FxA button is shown at 90% sample rate.
    var COOKIE_EXPIRATION_DAYS = 2;
    var COOKIE_ID = 'global-fxa-cta-exp';
    var nav = document.querySelector('.mzp-c-navigation');

    function isWithinSampleRate() {
        return (Math.random() < SAMPLE_RATE) ? true : false;
    }

    function cookieExpiresDate(date) {
        var d = date || new Date();
        d.setTime(d.getTime() + (COOKIE_EXPIRATION_DAYS * 24 * 60 * 60 * 1000));
        return d.toUTCString();
    }

    function setCookie(cohort) {
        Mozilla.Cookies.setItem(COOKIE_ID, cohort, cookieExpiresDate(), '/');
    }

    function getCookie() {
        return Mozilla.Cookies.getItem(COOKIE_ID);
    }

    function hasCookie() {
        return Mozilla.Cookies.hasItem(COOKIE_ID);
    }

    function shouldShowFxAButton() {
        var cohort;

        // If a cookie already exists then use that value to determine what to show.
        if (hasCookie()) {
            cohort = getCookie();
        }
        // Else roll the dice!
        else {
            cohort = isWithinSampleRate() ? 'fxa' : 'download';
            setCookie(cohort);
        }

        return cohort === 'fxa' ? true : false;
    }

    function showFxAButton() {
        nav.classList.add('show-fxa-button');

        window.dataLayer.push({
            'data-ex-variant': 'accounts-button',
            'data-ex-name': 'global-fxa-button'
        });
    }

    function showDownloadButton() {
        // Since the download button is already visible by default,
        // there's nothing to do here except tag the variant in GA.
        window.dataLayer.push({
            'data-ex-variant': 'download-button',
            'data-ex-name': 'global-fxa-button'
        });
    }

    function meetsRequirements() {
        if (typeof Mozilla.Client === 'undefined' || typeof Mozilla.Cookies === 'undefined') {
            return false;
        }

        // Respect privacy!
        if (!Mozilla.Cookies.enabled() || Mozilla.dntEnabled()) {
            return false;
        }

        // User should be on Firefox desktop and nav should be present on page.
        if (!Mozilla.Client.isFirefoxDesktop || !nav) {
            return false;
        }

        var userMajorVersion = Mozilla.Client._getFirefoxMajorVersion();
        var latestMajorVersion = parseInt(document.documentElement.getAttribute('data-latest-firefox'), 10);

        if (!userMajorVersion || !latestMajorVersion) {
            return false;
        }

        // User should be on Firefox Quantum or greater.
        return userMajorVersion >= 57;
    }

    function init() {
        if (meetsRequirements()) {
            if (shouldShowFxAButton()) {
                showFxAButton();
            } else {
                showDownloadButton();
            }
        }
    }

    init();
})();
