/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const preferenceCookieID = 'moz-1st-party-data-opt-out';

const DataPreferencesCookie = {};

DataPreferencesCookie.doOptOut = function () {
    if (DataPreferencesCookie.hasOptedOut()) {
        return;
    }

    const date = new Date();
    const cookieDuration = 365 * 24 * 60 * 60 * 1000; // 1 year expiration
    const domain = DataPreferencesCookie.getCookieDomain();
    date.setTime(date.getTime() + cookieDuration);
    window.Mozilla.Cookies.setItem(
        preferenceCookieID,
        'true',
        date.toUTCString(),
        '/',
        domain,
        false,
        'lax'
    );
};

DataPreferencesCookie.doOptIn = function () {
    if (!DataPreferencesCookie.hasOptedOut()) {
        return;
    }

    const domain = DataPreferencesCookie.getCookieDomain();
    window.Mozilla.Cookies.removeItem(
        preferenceCookieID,
        '/',
        domain,
        false,
        'lax'
    );
};

DataPreferencesCookie.hasOptedOut = function () {
    return window.Mozilla.Cookies.hasItem(preferenceCookieID);
};

/**
 * When in production specify we '.mozilla.org' instead of 'www.mozilla.org'
 * so that external Mozilla websites can use the opt-out cookie (issue #12056).
 * @param {url} used for testing purposes only.
 * @returns {domain} string or null.
 */
DataPreferencesCookie.getCookieDomain = function (url) {
    const siteUrl = typeof url === 'string' ? url : window.location.href;
    let domain = null;

    if (siteUrl.indexOf('www.allizom.org') !== -1) {
        domain = '.allizom.org';
    }

    if (siteUrl.indexOf('www.mozilla.org') !== -1) {
        domain = '.mozilla.org';
    }

    return domain;
};

export default DataPreferencesCookie;
