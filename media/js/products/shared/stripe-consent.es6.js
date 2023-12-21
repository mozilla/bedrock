/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    consentRequired,
    getConsentCookie
} from '../../base/consent/utils.es6';

const StripeConsent = {
    /**
     * Load Stripe Radar 3rd party script.
     */
    loadStripeJS: () => {
        const newScriptTag = document.createElement('script');
        const target = document.getElementsByTagName('script')[0];
        newScriptTag.src = 'https://js.stripe.com/v3/';
        target.parentNode.insertBefore(newScriptTag, target);
    },

    /**
     * Handle 'mozConsentStatus' event.
     * @param {Object} e - Event object.
     */
    handleConsent: (e) => {
        const hasConsent = e.detail.analytics;

        if (hasConsent) {
            StripeConsent.loadStripeJS();

            window.removeEventListener(
                'mozConsentStatus',
                StripeConsent.handleConsent,
                false
            );
        }
    },

    /**
     * Load Stripe JS based on consent state.
     * @returns {void}
     */
    init: () => {
        // If visitor is in the EU/EAA wait for a consent signal.
        if (consentRequired()) {
            window.addEventListener(
                'mozConsentStatus',
                StripeConsent.handleConsent,
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

            StripeConsent.loadStripeJS();
        }
    }
};

export default StripeConsent;
