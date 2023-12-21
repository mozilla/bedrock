/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    consentRequired,
    dntEnabled,
    getConsentCookie,
    gpcEnabled
} from '../consent/utils.es6';

const StubAttributionConsent = {
    /**
     * Handle 'mozConsentStatus' event.
     * @param {Object} e - Event object.
     */
    handleConsent: (e) => {
        const hasConsent = e.detail.analytics;

        if (hasConsent) {
            window.Mozilla.StubAttribution.init();
            window.removeEventListener(
                'mozConsentStatus',
                StubAttributionConsent.handleConsent,
                false
            );
        }
    },

    /**
     * Initialize stub attribution based on consent status.
     */
    init: () => {
        /**
         * If either Global Privacy Control (GPC) or Do Not Track (DNT) are enabled
         * then do not do attribution.
         */
        if (gpcEnabled()) {
            return;
        }

        if (dntEnabled()) {
            return;
        }

        // If visitor is in the EU/EAA.
        if (consentRequired()) {
            /**
             * If we're on /thanks/ and already have a consent cookie that
             * accepts analytics then start attribution. This is important
             * because a consent signal does not fire on /thanks/ in EU/EAA
             * due to the allow-list, but we still want to record attribution
             * from campaign pages that are allowed.
             */
            const cookie = getConsentCookie();

            if (
                window.Mozilla.StubAttribution.isFirefoxDownloadThanks() &&
                cookie &&
                cookie.analytics
            ) {
                window.Mozilla.StubAttribution.init();
            } else {
                /**
                 * If we don't have a consent cookie, then wait for a signal.
                 */
                window.addEventListener(
                    'mozConsentStatus',
                    StubAttributionConsent.handleConsent,
                    false
                );
            }
        } else {
            /**
             * Else we do attribution by default, unless the visitor has a consent
             * cookie that rejects analytics.
             */
            const cookie = getConsentCookie();

            if (cookie && !cookie.analytics) {
                return;
            }

            window.Mozilla.StubAttribution.init();
        }
    }
};

export default StubAttributionConsent;
