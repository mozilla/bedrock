/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FxaProductButton from './fxa-product-button.es6.js';
import { consentRequired, getConsentCookie } from './consent/utils.es6';

const FxaProductButtonConsent = {
    /**
     * Initialize FxA metrics flow request.
     */
    initMetricsFlow: () => {
        if (FxaProductButton.isSupported()) {
            FxaProductButton.init().catch(() => {
                // do nothing
            });
        }
    },

    /**
     * Handle 'mozConsentStatus' event.
     * @param {Object} e - Consent event.
     */
    handleConsent: (e) => {
        if (e.detail.analytics) {
            FxaProductButtonConsent.initMetricsFlow();
            window.removeEventListener(
                'mozConsentStatus',
                FxaProductButtonConsent.handleConsent,
                false
            );
        }
    },

    /**
     * Initialize the FxA product button with consent status.
     */
    init: () => {
        // If visitor is in the EU/EAA wait for a consent signal.
        if (consentRequired()) {
            window.addEventListener(
                'mozConsentStatus',
                FxaProductButtonConsent.handleConsent,
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

            FxaProductButtonConsent.initMetricsFlow();
        }
    }
};

export default FxaProductButtonConsent;
