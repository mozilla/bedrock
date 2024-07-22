/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MozAllowList from './allow-list.es6';

const COOKIE_ID = 'moz-consent-pref'; // Cookie name
const COOKIE_EXPIRY_DAYS = 182; // 6 months expiry

/**
 * Determines if the current page requires consent.
 * Looks for a data attribute on the <html> tag.
 */
function consentRequired() {
    const attr = document
        .getElementsByTagName('html')[0]
        .getAttribute('data-needs-consent');

    return attr ? attr.toLowerCase() === 'true' : false;
}

/**
 * Determines if Do Not Track is enabled.
 * @returns {Boolean}
 */
function dntEnabled() {
    return (
        typeof window.Mozilla.dntEnabled === 'function' &&
        window.Mozilla.dntEnabled()
    );
}

/**
 * Determines the hostname to set the consent cookie on.
 * Typically, this is either .mozilla.org or .allizom.org.
 * But otherwise, it returns null so the cookie will apply
 * to the current domain.
 * @param {String} hostname - The hostname of the current page.
 * @returns {String|null} - Returns the domain or null.
 */
function getHostName(hostname) {
    let domain = null;

    if (typeof hostname !== 'string') {
        return domain;
    }

    if (hostname.indexOf('.allizom.org') !== -1) {
        domain = '.allizom.org';
    }

    if (hostname.indexOf('.mozilla.org') !== -1) {
        domain = '.mozilla.org';
    }

    return domain;
}

/**
 * Determines if the consent cookie exists.
 * @returns {Boolean}
 */
function hasConsentCookie() {
    return (
        window.Mozilla.Cookies.enabled() &&
        window.Mozilla.Cookies.hasItem(COOKIE_ID)
    );
}

/**
 * Gets the consent cookie object.
 * @returns {Object|Boolean} - Returns the consent cookie object or false.
 */
function getConsentCookie() {
    try {
        return JSON.parse(window.Mozilla.Cookies.getItem(COOKIE_ID));
    } catch (e) {
        return false;
    }
}

/**
 * Sets consent cookie with data provided.
 * @param {Object} data - Object containing consent data.
 * @returns {Boolean}
 */
function setConsentCookie(data) {
    try {
        if (typeof data !== 'object') {
            return false;
        }

        const date = new Date();
        date.setDate(date.getDate() + COOKIE_EXPIRY_DAYS);
        const expires = date.toUTCString();

        window.Mozilla.Cookies.setItem(
            COOKIE_ID,
            JSON.stringify(data),
            expires,
            '/',
            getHostName(window.location.hostname),
            false,
            'lax'
        );

        return true;
    } catch (e) {
        return false;
    }
}

/**
 * Determines if Global Privacy Control is enabled.
 * @returns {Boolean}
 */
function gpcEnabled() {
    return (
        typeof window.Mozilla.gpcEnabled === 'function' &&
        window.Mozilla.gpcEnabled()
    );
}

/**
 * Determine if the current page is /firefox/download/thanks/.
 * @param {String} location - The current page URL.
 * @return {Boolean}.
 */
function isFirefoxDownloadThanks(location) {
    if (typeof location !== 'string') {
        return false;
    }
    return location.indexOf('/firefox/download/thanks/') > -1;
}

/**
 * Determines if the current page URL contains a query string
 * that allows the consent banner to be displayed.
 * @param {String} search - The current page URL search string.
 * @returns {Boolean}
 */
function isURLExceptionAllowed(search) {
    if (typeof search !== 'string') {
        return false;
    }
    return search.indexOf('mozcb=y') > -1;
}

/**
 * Takes a given path name and checks it against the allow-list for
 * displaying the consent banner.
 * @param {String} pathname
 * @returns {Boolean}
 */
function isURLPermitted(pathname) {
    let currentPath = pathname;

    // Remove locale from current URL pathname;
    currentPath = currentPath.replace(/^(\/\w{2}-\w{2}\/|\/\w{2,3}\/)/, '/');

    for (let i = 0; i < MozAllowList.length; i++) {
        // Turn allowlist path into a regex, supporting wildcards.
        const pathRegex = new RegExp(
            '^' + MozAllowList[i].replace(/\*/g, '.*') + '$'
        );

        if (pathRegex.test(currentPath)) {
            return true;
        }
    }

    return false;
}

/**
 * A very primitive state machine to determine if a consent
 * banner needs to be displayed or if analytics can be loaded.
 * @param {Object} obj - Object containing consent state flags.
 * @returns {String} Consent state message.
 */
function getConsentState(obj) {
    /**
     * If GPC or DNT is enabled, there's no need to show
     * a banner or load analytics since we take that signal
     * as a rejection to non-essential cookies and analytics.
     */
    if (obj.gpcEnabled) {
        return 'STATE_GPC_ENABLED';
    }

    if (obj.dntEnabled) {
        return 'STATE_DNT_ENABLED';
    }

    /**
     * If the visitor is in the EU, and page is on the allow-list,
     * then show the cookie banner.
     */
    if (obj.consentRequired) {
        if (obj.isURLPermitted || obj.isURLExceptionAllowed) {
            if (obj.hasConsentCookie) {
                return 'STATE_HAS_CONSENT_COOKIE';
            } else {
                return 'STATE_SHOW_COOKIE_BANNER';
            }
        } else {
            return 'STATE_BANNER_NOT_PERMITTED';
        }
    } else {
        /**
         * For remaining users outside of EU,
         * load analytics by default.
         */
        if (obj.hasConsentCookie) {
            return 'STATE_HAS_CONSENT_COOKIE';
        } else {
            return 'STATE_COOKIES_PERMITTED';
        }
    }
}

export {
    consentRequired,
    dntEnabled,
    getConsentCookie,
    getConsentState,
    getHostName,
    gpcEnabled,
    hasConsentCookie,
    isFirefoxDownloadThanks,
    isURLExceptionAllowed,
    isURLPermitted,
    setConsentCookie
};
