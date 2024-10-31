/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { getConsentCookie } from '../consent/utils.es6';

let _pencilBanner;
const M24PencilBanner = {};
const BANNER_ID = 'pencil-banner';

M24PencilBanner.consentsToCookies = function () {
    const cookie = getConsentCookie();

    if (cookie) {
        return cookie.preference;
    } else {
        return true;
    }
};

M24PencilBanner.setCookie = function () {
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
    if (!M24PencilBanner.consentsToCookies()) {
        return;
    }

    const date = new Date();
    const cookieDuration = 1 * 24 * 60 * 60 * 1000; // 1 day expiration
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

M24PencilBanner.hasCookie = function () {
    return Mozilla.Cookies.hasItem(BANNER_ID);
};

M24PencilBanner.close = function () {
    // Remove the banner from the DOM.
    _pencilBanner.parentNode.removeChild(_pencilBanner);

    // Set a cookie to not display it again.
    M24PencilBanner.setCookie();

    // Record widget dismiss action in GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'banner',
        action: 'dismiss',
        name: BANNER_ID
    });
};

M24PencilBanner.show = function () {
    // Display the banner
    _pencilBanner.classList.remove('hidden');

    // Wire up close button
    _pencilBanner
        .querySelector('.m24-pencil-banner-close')
        .addEventListener('click', M24PencilBanner.close, false);

    // Record widget display action in GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'banner',
        action: 'display',
        name: BANNER_ID,
        non_interaction: true
    });
};

M24PencilBanner.init = function () {
    const cookiesEnabled =
        typeof window.Mozilla.Cookies !== 'undefined' &&
        window.Mozilla.Cookies.enabled();

    _pencilBanner = document.querySelector('.m24-pencil-banner');

    // If the banner does not exist on a page then do nothing.
    if (!_pencilBanner) {
        return false;
    }

    // Show only if cookies enabled & banner not previously dismissed.
    if (cookiesEnabled && !M24PencilBanner.hasCookie()) {
        M24PencilBanner.show();
    }
};

export default M24PencilBanner;
