/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { getConsentCookie } from '../consent/utils.es6';

let _pageBanner;
const MozBanner = {};

MozBanner.consentsToCookies = function () {
    const cookie = getConsentCookie();

    if (cookie) {
        return cookie.preference;
    } else {
        return true;
    }
};

MozBanner.setCookie = function (id) {
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
    if (!MozBanner.consentsToCookies()) {
        return;
    }

    const date = new Date();
    const cookieDuration = 1 * 24 * 60 * 60 * 1000; // 1 day expiration
    date.setTime(date.getTime() + cookieDuration); // 1 day expiration
    window.Mozilla.Cookies.setItem(
        'moz-banner-' + id,
        true,
        date.toUTCString(),
        '/',
        undefined,
        false,
        'lax'
    );
};

MozBanner.hasCookie = function (id) {
    return Mozilla.Cookies.hasItem('moz-banner-' + id);
};

MozBanner.close = function () {
    // Remove the banner from the DOM.
    _pageBanner.parentNode.removeChild(_pageBanner);

    // Set a cookie to not display it again.
    MozBanner.setCookie(MozBanner.id);

    // GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'banner',
        action: 'dismiss',
        name: MozBanner.id
    });
};

MozBanner.show = function (renderAtTopOfPage) {
    const outerWrapper = document.getElementById('outer-wrapper');

    // if for some reason there's no outer-wrapper on the page, do nothing.
    if (!outerWrapper) {
        return;
    }

    // remove banner from bottom of page.
    _pageBanner = _pageBanner.parentNode.removeChild(_pageBanner);

    // reinsert at the top of viewport, else after primary nav.
    if (renderAtTopOfPage) {
        document.body.insertBefore(_pageBanner, document.body.firstChild);
    } else {
        outerWrapper.insertBefore(_pageBanner, outerWrapper.firstChild);
    }

    // display the banner
    _pageBanner.classList.add('c-banner-is-visible');

    // GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'banner',
        action: 'display',
        name: MozBanner.id,
        non_interaction: true
    });

    // wire up close button
    _pageBanner
        .querySelector('.c-banner-close')
        .addEventListener('click', MozBanner.close, false);
};

MozBanner.init = function (id, renderAtTopOfPage) {
    const cookiesEnabled =
        typeof window.Mozilla.Cookies !== 'undefined' &&
        window.Mozilla.Cookies.enabled();

    _pageBanner = document.getElementById(id);

    /**
     * If the banner does not exist on a page,
     * or there's not a valid banner ID then do nothing.
     */
    if (!_pageBanner || typeof id !== 'string') {
        return false;
    }

    MozBanner.id = id;

    // Show only if cookies enabled & banner not previously dismissed.
    if (cookiesEnabled && !MozBanner.hasCookie(MozBanner.id)) {
        MozBanner.show(renderAtTopOfPage);
    }
};

export default MozBanner;
