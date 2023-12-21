/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const MozConsentBanner = {};

const EVENT_NAME_STATUS = 'mozConsentStatus';
const EVENT_NAME_OPEN = 'mozConsentOpen';
const EVENT_NAME_CLOSE = 'mozConsentClose';
const COOKIE_ID = 'moz-consent-pref';
const COOKIE_EXPIRY_DAYS = 182; // 6 months
const MSG_OPTIONS_ERROR_DISABLED = 'verifyOptions(): cookies are disabled.';
const MSG_OPTIONS_ERROR_EXPIRY =
    'verifyOptions(): options.cookieExpiryDays not set.';
const MSG_OPTIONS_ERROR_HELPER = 'verifyOptions(): options.helper not set.';
const MSG_OPTIONS_ERROR_OPT_OUT = 'verifyOptions(): options.optOut not set.';
const MSG_OPTIONS_VALID = 'verifyOptions(): success.';

/**
 * Default configuration options that can be overridden via init().
 */
const options = {
    cookieDomain: null,
    cookieExpiryDays: COOKIE_EXPIRY_DAYS,
    cookieID: COOKIE_ID,
    optOut: false,
    eventName: EVENT_NAME_STATUS,
    helper: null
};

/**
 * Sets preference cookie indicating consent choice.
 * @param {Object} data - consent preference
 */
MozConsentBanner.setPrefCookie = (data) => {
    try {
        const date = new Date();
        date.setDate(date.getDate() + options.cookieExpiryDays);
        const expires = date.toUTCString();

        options.helper.setItem(
            options.cookieID,
            JSON.stringify(data),
            expires,
            '/',
            options.cookieDomain,
            false,
            'lax'
        );

        return true;
    } catch (e) {
        return false;
    }
};

/**
 * Get preference cookie value if set
 * @returns {Boolean}
 */
MozConsentBanner.getPrefCookie = () => {
    try {
        return (
            options.helper.hasItem(options.cookieID) &&
            JSON.parse(options.helper.getItem(options.cookieID))
        );
    } catch (e) {
        return false;
    }
};

/**
 * Returns the domain to set for the preference cookie. When in production
 * we want to specify '.mozilla.org' instead of 'www.mozilla.org',
 * so that all Mozilla sub domains can use the same preference cookie.
 * @returns {domain} string or null.
 */
MozConsentBanner.getHostName = () => {
    const url = window.location.hostname;
    let domain = null;

    if (url.indexOf('.allizom.org') !== -1) {
        domain = '.allizom.org';
    }

    if (url.indexOf('.mozilla.org') !== -1) {
        domain = '.mozilla.org';
    }

    return domain;
};

/**
 * Helper for dispatching a custom event with a
 * given name and data payload.
 * @param {Object} eventName
 * @param {Object} eventData
 */
MozConsentBanner.dispatchEvent = (eventName, eventData) => {
    if (typeof window.CustomEvent === 'function') {
        // Modern browsers
        window.dispatchEvent(
            new CustomEvent(eventName, {
                detail: eventData
            })
        );
    } else if (typeof document.createEvent === 'function') {
        // Internet Explorer 10
        const customEvent = document.createEvent('CustomEvent');
        customEvent.initCustomEvent(eventName, false, false, eventData);
        window.dispatchEvent(customEvent);
    } else if (typeof document.createEventObject === 'function') {
        // Internet Explorer 9
        const customEventObj = document.createEventObject();
        customEventObj.type = eventName;
        customEventObj.bubbles = false;
        customEventObj.cancelable = false;
        customEventObj.detail = eventData; // Optional data for the event
        window.fireEvent('on' + customEventObj.type, customEventObj);
    }
};

/**
 * Event handler for accepting cookies
 */
MozConsentBanner.onAcceptClick = () => {
    const preferences = {
        analytics: true,
        preference: true
    };

    MozConsentBanner.setPrefCookie(preferences);
    MozConsentBanner.dispatchEvent(EVENT_NAME_STATUS, preferences);
    MozConsentBanner.dispatchEvent(EVENT_NAME_CLOSE, {});
};

/**
 * Event handler for rejecting cookies
 */
MozConsentBanner.onRejectClick = () => {
    const preferences = {
        analytics: false,
        preference: false
    };

    MozConsentBanner.setPrefCookie(preferences);
    MozConsentBanner.dispatchEvent(EVENT_NAME_STATUS, preferences);
    MozConsentBanner.dispatchEvent(EVENT_NAME_CLOSE, {});
};

/**
 * Validates BannerOptions configuration object.
 * @param {BannerOptions} object containing one or more properties.
 * @returns {String} message to indicate either success or error.
 */
MozConsentBanner.verifyOptions = (options) => {
    // Verify cookie expiry has been set.
    if (typeof options.cookieExpiryDays !== 'number') {
        return MSG_OPTIONS_ERROR_EXPIRY;
    }

    // Verify cookie helper dependency is defined.
    if (!options.helper || typeof options.helper.setItem !== 'function') {
        return MSG_OPTIONS_ERROR_HELPER;
    }

    // Verify that optOut flag is set.
    if (typeof options.optOut !== 'boolean') {
        return MSG_OPTIONS_ERROR_OPT_OUT;
    }

    // Verify that cookies are enabled in the browser.
    if (!options.helper.enabled()) {
        return MSG_OPTIONS_ERROR_DISABLED;
    }

    return MSG_OPTIONS_VALID;
};

/**
 * MozConsentBanner.init() configuration options:
 * @typedef {Object} BannerOptions
 * @property {string} cookieDomain - Sets a preference cookie for a specific host name.
 * @property {number} cookieExpiryDays - Preference cookie expiry by number of days.
 * @property {string} cookieID - Preference cookie identifier.
 * @property {object} helper (required) - reference to @mozmeao/cookie-helper peer dependency.
 */

/**
 * Initializes cookie banner and binds events.
 * @param {BannerOptions} object containing one or more properties.
 * @returns {Boolean} to indicate if initialization succeeded.
 */
MozConsentBanner.init = (config) => {
    for (const opt in config) {
        if (Object.prototype.hasOwnProperty.call(config, opt)) {
            options[opt] = config[opt];
        }
    }

    /**
     * If domain for preference cookie has not be supplied via config,
     * set it via getHostName()
     */
    if (!options.cookieDomain) {
        options.cookieDomain = MozConsentBanner.getHostName();
    }

    /**
     * Validate options object before trying to show the banner.
     */
    const configValidationMsg = MozConsentBanner.verifyOptions(options);

    if (configValidationMsg !== MSG_OPTIONS_VALID) {
        if (window.console && window.console.error) {
            console.error(configValidationMsg); // eslint-disable-line no-console
        }
        return false;
    }

    /**
     * If preference cookie exists and consent has previously been given,
     * despatch consent event. Otherwise show the banner.
     */
    const preferences = MozConsentBanner.getPrefCookie();

    if (preferences) {
        MozConsentBanner.dispatchEvent(EVENT_NAME_STATUS, preferences);
    } else {
        const defaults = {
            functional: options.optOut,
            analytics: options.optOut
        };

        MozConsentBanner.dispatchEvent(EVENT_NAME_OPEN, {});
        MozConsentBanner.dispatchEvent(EVENT_NAME_STATUS, defaults);
    }

    return true;
};

module.exports = MozConsentBanner;
