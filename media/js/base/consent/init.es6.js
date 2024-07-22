/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MozConsentBanner from '@mozmeao/consent-banner';
import {
    consentRequired,
    dntEnabled,
    getConsentCookie,
    getConsentState,
    gpcEnabled,
    hasConsentCookie,
    isURLExceptionAllowed,
    isURLPermitted
} from './utils.es6';

const banner = document.querySelector('.moz-consent-banner');
const footer = document.getElementById('colophon');

/**
 * Helper to debounce a function.
 * @param {Function} func - Function to debounce.
 * @param {Number} delay - The delay in milliseconds.
 * @returns
 */
function debounce(func, delay) {
    let timer;
    return function () {
        clearTimeout(timer);
        timer = setTimeout(() => {
            func.apply(this, arguments);
        }, delay);
    };
}

/**
 * Adds extra padding to the page footer to prevent the banner
 * from overlapping.
 */
function updateBodyPadding() {
    if (!footer) {
        return;
    }

    if (window.innerHeight > 600) {
        footer.style.paddingBottom = banner.offsetHeight + 'px';
    } else {
        footer.style.paddingBottom = '0px';
    }
}

const onResize = debounce(updateBodyPadding, 200);

/**
 * If user clicks back button from /cookie-settings/ and
 * the page is in bfcache, reload the page if they have
 * set a consent cookie to avoid showing the banner again
 * inadvertently.
 * @param {Object} e - The page navigation event.
 */
function handleBfCacheNavigation(e) {
    if (e.persisted && hasConsentCookie()) {
        window.location.reload();
    }
}

/**
 * Opens the consent banner and binds button click event listeners.
 */
function openBanner() {
    // Bind event listeners
    document
        .getElementById('moz-consent-banner-button-accept')
        .addEventListener('click', MozConsentBanner.onAcceptClick, false);
    document
        .getElementById('moz-consent-banner-button-reject')
        .addEventListener('click', MozConsentBanner.onRejectClick, false);
    window.addEventListener('pageshow', handleBfCacheNavigation, false);

    // Show banner
    document.getElementById('moz-consent-banner').classList.add('is-visible');

    // Add padding to the footer
    setTimeout(updateBodyPadding, 0);
    window.addEventListener('resize', onResize, false);
}

/**
 * Close the consent banner and unbinds button click event listeners.
 */
function closeBanner() {
    // Unbind event listeners
    document
        .getElementById('moz-consent-banner-button-accept')
        .removeEventListener('click', MozConsentBanner.onAcceptClick, false);
    document
        .getElementById('moz-consent-banner-button-reject')
        .removeEventListener('click', MozConsentBanner.onRejectClick, false);
    window.removeEventListener('pageshow', handleBfCacheNavigation, false);

    // Hide banner
    document
        .getElementById('moz-consent-banner')
        .classList.remove('is-visible');

    // Remove padding from the footer
    document.body.style.paddingBottom = '0';
    window.removeEventListener('resize', onResize, false);
}

/**
 * Initialize the consent banner and bind open and close events.
 */
function initializeBanner() {
    // Make sure to bind open and close events before calling init().
    window.addEventListener('mozConsentOpen', openBanner, false);
    window.addEventListener('mozConsentClose', closeBanner, false);

    MozConsentBanner.init({
        helper: window.Mozilla.Cookies
    });
}

/**
 * Helper function to dispatch the mozConsentStatus event.
 * @param {Object} consent - The consent object.
 */
function dispatchEvent(consent) {
    MozConsentBanner.dispatchEvent('mozConsentStatus', consent);
}

/**
 * Initialize the consent banner based on the current state.
 */
function init() {
    const state = getConsentState({
        hasConsentCookie: hasConsentCookie(),
        gpcEnabled: gpcEnabled(),
        dntEnabled: dntEnabled(),
        consentRequired: consentRequired(),
        isURLExceptionAllowed: isURLExceptionAllowed(window.location.search),
        isURLPermitted: isURLPermitted(window.location.pathname)
    });

    switch (state) {
        case 'STATE_GPC_ENABLED':
        case 'STATE_DNT_ENABLED': {
            /**
             * If GPC or DNT are enabled we interpret this as a
             * rejection signal for cookie and analytics. As such,
             * we do not show a consent banner and no not load
             * analytics that require opt-in.
             */
            break;
        }
        case 'STATE_HAS_CONSENT_COOKIE': {
            const cookie = getConsentCookie();

            if (cookie) {
                dispatchEvent(cookie);
            }
            break;
        }
        case 'STATE_SHOW_COOKIE_BANNER': {
            initializeBanner();
            break;
        }
        case 'STATE_COOKIES_PERMITTED': {
            dispatchEvent({
                analytics: true,
                preference: true
            });
            break;
        }
        default:
            break;
    }

    // Global helper function to get consent state for debugging purposes.
    if (typeof window.Mozilla !== 'undefined') {
        window.Mozilla.getConsentStateMsg = () => {
            return state;
        };
    }
}

init();
