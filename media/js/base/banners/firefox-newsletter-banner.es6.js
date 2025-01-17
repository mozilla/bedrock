/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { getConsentCookie } from '../consent/utils.es6';

let _firefoxNewsletterBanner;
const FirefixNewsletterBanner = {};
const BANNER_ID = 'firefox-newsletter-banner';

FirefixNewsletterBanner.consentsToCookies = function () {
    const cookie = getConsentCookie();

    if (cookie) {
        return cookie.preference;
    } else {
        return true;
    }
};

FirefixNewsletterBanner.setCookie = function () {
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
    if (!FirefixNewsletterBanner.consentsToCookies()) {
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

FirefixNewsletterBanner.hasBeenClosed = () => {
    return (
        document.documentElement.getAttribute(
            'data-firefox-newsletter-banner-closed'
        ) === 'true'
    );
};

FirefixNewsletterBanner.close = function () {
    // Display banner in regular document flow
    document.documentElement.setAttribute(
        'data-firefox-newsletter-banner-closed',
        'true'
    );

    // Set a cookie to not display it again.
    FirefixNewsletterBanner.setCookie();

    // Record widget dismiss action in GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'banner',
        action: 'dismiss',
        name: BANNER_ID
    });
};

FirefixNewsletterBanner.bindEvents = function () {
    // Wire up close button
    _firefoxNewsletterBanner
        .querySelector('.c-banner-close')
        .addEventListener('click', FirefixNewsletterBanner.close, false);

    // Record widget display action in GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'banner',
        action: 'display',
        name: BANNER_ID,
        non_interaction: true
    });
};

FirefixNewsletterBanner.init = function () {
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
    if (cookiesEnabled && !FirefixNewsletterBanner.hasBeenClosed()) {
        FirefixNewsletterBanner.bindEvents();
    }
};

export default FirefixNewsletterBanner;
