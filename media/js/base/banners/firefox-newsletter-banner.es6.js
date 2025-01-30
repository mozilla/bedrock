/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { getConsentCookie } from '../consent/utils.es6';

let _firefoxNewsletterBanner;
const FirefoxNewsletterBanner = {};
const BANNER_ID = 'firefox-newsletter-banner';

FirefoxNewsletterBanner.consentsToCookies = function () {
    const cookie = getConsentCookie();

    if (cookie) {
        return cookie.preference;
    } else {
        return true;
    }
};

FirefoxNewsletterBanner.setCookie = function () {
    /**
     * When closing a banner we set a "preference cookie" to remember
     * that a user no longer wishes to see it on repeat page visits.
     * Legal are OK to set this cookie without explicit consent in
     * EU/EAA countries because:
     *
     * 1) The cookie is not used for tracking purposes in any way.
     * 2) The cookie is set only after an explicit action by the user
     *    that signals clear intent.
     *
     * We still honor not setting this cookie if preference cookies
     * have been explicitly rejected by the user.
     */
    if (!FirefoxNewsletterBanner.consentsToCookies()) {
        return;
    }

    const date = new Date();
    const cookieDuration = 7 * 24 * 60 * 60 * 1000; // 7 day expiration
    date.setTime(date.getTime() + cookieDuration);
    window.Mozilla.Cookies.setItem(
        BANNER_ID,
        true,
        date.toUTCString(),
        '/',
        undefined,
        false,
        'lax'
    );
};

FirefoxNewsletterBanner.hasBeenClosed = () => {
    return (
        document.documentElement.getAttribute(
            'data-firefox-newsletter-banner-closed'
        ) === 'true'
    );
};

FirefoxNewsletterBanner.close = function () {
    // Display banner in regular document flow
    document.documentElement.setAttribute(
        'data-firefox-newsletter-banner-closed',
        'true'
    );

    // Set a cookie to not show it as a banner again.
    FirefoxNewsletterBanner.setCookie();

    // Record widget dismiss action in GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'banner',
        action: 'dismiss',
        name: BANNER_ID
    });
};

FirefoxNewsletterBanner.bindEvents = function () {
    // Wire up close button
    _firefoxNewsletterBanner
        .querySelector('.c-banner-close')
        .addEventListener('click', FirefoxNewsletterBanner.close, false);

    // Record widget display action in GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'banner',
        action: 'display',
        name: BANNER_ID,
        non_interaction: true
    });
};

FirefoxNewsletterBanner.init = function () {
    const cookiesEnabled =
        typeof window.Mozilla.Cookies !== 'undefined' &&
        window.Mozilla.Cookies.enabled();

    _firefoxNewsletterBanner = document.querySelector(
        '.c-banner-fx-newsletter'
    );

    // If the banner does not exist on a page then do nothing.
    if (!_firefoxNewsletterBanner) {
        return false;
    }

    // Show only if cookies enabled & banner not previously dismissed.
    if (cookiesEnabled && !FirefoxNewsletterBanner.hasBeenClosed()) {
        FirefoxNewsletterBanner.bindEvents();
    }
};

export default FirefoxNewsletterBanner;
