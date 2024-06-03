/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import AffiliateAttribution from './affiliate-attribution.es6';
import {
    consentRequired,
    dntEnabled,
    getConsentCookie,
    gpcEnabled
} from '../../base/consent/utils.es6';

const AffiliateConsent = {
    /**
     * Initialize the affiliate flow if the visitor meets the requirements.
     * Else, just add flow params as normal.
     */
    initAffiliateFlow: () => {
        if (AffiliateAttribution.meetsRequirements()) {
            AffiliateAttribution.init().catch((e) => {
                console.error(e); // eslint-disable-line no-console
            });
        } else {
            AffiliateAttribution.addFlowParams();
        }
    },

    /**
     * Add flow params to the subscription link href.
     */
    initFlowParams: () => {
        AffiliateAttribution.addFlowParams();
    },

    /**
     * Handle 'mozConsentStatus' event.
     * @param {Object} e - Event object.
     */
    handleConsent: (e) => {
        const hasConsent = e.detail.analytics;

        if (hasConsent) {
            AffiliateConsent.initAffiliateFlow();
            window.removeEventListener(
                'mozConsentStatus',
                AffiliateConsent.handleConsent,
                false
            );
        }
    },

    /**
     * Initialize the affiliate flow or add flow params based
     * on consent state.
     */
    init: () => {
        // If visitor is in the EU/EAA wait for a consent signal.
        if (consentRequired()) {
            window.addEventListener(
                'mozConsentStatus',
                AffiliateConsent.handleConsent,
                false
            );
        } else {
            /**
             * Else if outside of EU/EAA, do attribution
             * (unless consent cookie rejects analytics).
             */
            const cookie = getConsentCookie();

            if (cookie && !cookie.analytics) {
                return;
            }

            // If GPC/DNT is enabled, just add flow params.
            if (dntEnabled() || gpcEnabled()) {
                AffiliateConsent.initFlowParams();
                return;
            }

            AffiliateConsent.initAffiliateFlow();
        }
    }
};

export default AffiliateConsent;
