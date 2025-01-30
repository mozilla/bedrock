/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FxaLink from './fxa-link.es6.js';
import FxaAttribution from './fxa-attribution.es6.js';
import { consentRequired, getConsentCookie } from './consent/utils.es6.js';

const FxaBundleConsent = {
    /**
     * Initialize attribution based on URL query parameters.
     */
    initAttribution: () => {
        if (typeof window._SearchParams !== 'undefined') {
            const urlParams = new window._SearchParams();
            FxaAttribution.init(urlParams.params);
        }
    },

    /**
     * Handle 'mozConsentStatus' event.
     * @param {Object} e - Event object.
     */
    handleConsent: (e) => {
        if (e.detail.analytics) {
            FxaBundleConsent.initAttribution();
        }

        window.removeEventListener(
            'mozConsentStatus',
            FxaBundleConsent.handleConsent,
            false
        );
    },

    /**
     * Initialize data consent for EU/EAA countries.
     */
    initConsent: () => {
        // If visitor is in the EU/EAA wait for a consent signal.
        if (consentRequired()) {
            window.addEventListener(
                'mozConsentStatus',
                FxaBundleConsent.handleConsent,
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

            FxaBundleConsent.initAttribution();
        }
    },

    /**
     * Initialize FxA bundle.
     */
    init: () => {
        // Handle data consent for EU/EAA countries.
        FxaBundleConsent.initConsent();

        // Configure FxA links for Sync etc.
        if (typeof window._SearchParams !== 'undefined') {
            FxaLink.init();
        }
    }
};

export default FxaBundleConsent;
