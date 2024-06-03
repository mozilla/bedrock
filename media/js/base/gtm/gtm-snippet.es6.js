/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    consentRequired,
    dntEnabled,
    getConsentCookie,
    gpcEnabled,
    isFirefoxDownloadThanks
} from '../consent/utils.es6';

const GTM_CONTAINER_ID = document
    .getElementsByTagName('html')[0]
    .getAttribute('data-gtm-container-id');

const GTMSnippet = {};

/**
 * Load the GTM snippet. Expects `GTM_CONTAINER_ID` to be
 * defined in the HTML tag via a data attribute.
 */
GTMSnippet.loadSnippet = () => {
    if (GTM_CONTAINER_ID) {
        // prettier-ignore
        (function(w,d,s,l,i,j,f,dl,k,q){
            w[l]=w[l]||[];w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});f=d.getElementsByTagName(s)[0];
            k=i.length;q='//www.googletagmanager.com/gtm.js?id=@&l='+(l||'dataLayer');
            while(k--){j=d.createElement(s);j.async=!0;j.src=q.replace('@',i[k]);f.parentNode.insertBefore(j,f);}
        }(window,document,'script','dataLayer',[GTM_CONTAINER_ID]));
    }
};

/**
 * Determine if the current page is /firefox/download/thanks/.
 * @returns {Boolean}
 */
GTMSnippet.isFirefoxDownloadThanks = () => {
    return isFirefoxDownloadThanks(window.location.href);
};

/**
 * Event handler for `mozConsentStatus` event.
 * @param {Object} e - Event object
 */
GTMSnippet.handleConsent = (e) => {
    const hasConsent = e.detail.analytics;

    if (hasConsent) {
        GTMSnippet.loadSnippet();
        window.removeEventListener(
            'mozConsentStatus',
            GTMSnippet.handleConsent,
            false
        );
    }
};

/**
 * Logic for when to load the GTM snippet. We try and do this as soon as possible
 * since the script runs in the <head>. For visitors in the EU who require explicit
 * opt-in, we wait for a `mozConsentStatus` signal handled in `base/consent/init.es6.js`.
 */
GTMSnippet.init = () => {
    /**
     * If either Global Privacy Control (GPC) or Do Not Track (DNT) are enabled
     * then we do not load Google Tag Manager.
     */
    if (gpcEnabled()) {
        return;
    }

    if (dntEnabled()) {
        return;
    }

    // If visitor is in the EU/EAA wait for a consent signal.
    if (consentRequired()) {
        /**
         * If we're on /thanks/ and already have a consent cookie that
         * accepts analytics then load GTM. This is important because
         * a consent signal does not fire on /thanks/ in EU/EAA due to
         * the allow-list, but we still want to record downloads from
         * campaign pages that are allowed.
         */
        const cookie = getConsentCookie();

        if (
            GTMSnippet.isFirefoxDownloadThanks(window.location.href) &&
            cookie &&
            cookie.analytics
        ) {
            GTMSnippet.loadSnippet();
        } else {
            window.addEventListener(
                'mozConsentStatus',
                GTMSnippet.handleConsent,
                false
            );
        }
    } else {
        /**
         * Else if outside of EU/EAA, load analytics by default
         * (unless consent cookie rejects analytics).
         */
        const cookie = getConsentCookie();

        if (cookie && !cookie.analytics) {
            return;
        }

        GTMSnippet.loadSnippet();
    }
};

export default GTMSnippet;
