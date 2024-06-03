/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FxaForm from './fxa-form.es6.js';
import { consentRequired, getConsentCookie } from './consent/utils.es6';

const FxaFormConsent = {
    /**
     * Initialize the form with consent status.
     * @param {Boolean} consent - Whether attribution is allowed.
     */
    initForm: (consent) => {
        const skipAttribution = !consent ? true : false;
        if (FxaForm.isSupported()) {
            FxaForm.init(skipAttribution).catch(() => {
                // do nothing
            });
        }
    },

    /**
     * Handle 'mozConsentStatus' event.
     * @param {Object} e - Event object.
     */
    handleConsent: (e) => {
        FxaFormConsent.initForm(e.detail.analytics);
        window.removeEventListener(
            'mozConsentStatus',
            FxaFormConsent.handleConsent,
            false
        );
    },

    /**
     * Initialize the essential form functionality before waiting for consent.
     */
    initEssential: () => {
        // Configure Sync for Firefox desktop browsers.
        FxaForm.configureSync();
    },

    /**
     * Initialize the form with consent status.
     */
    init: () => {
        FxaFormConsent.initEssential();

        // If visitor is in the EU/EAA wait for a consent signal.
        if (consentRequired()) {
            window.addEventListener(
                'mozConsentStatus',
                FxaFormConsent.handleConsent,
                false
            );
        } else {
            /**
             * Else if outside of EU/EAA, do attribution
             * (unless consent cookie rejects analytics).
             */
            const cookie = getConsentCookie();

            if (cookie) {
                FxaFormConsent.initForm(cookie.analytics);
            } else {
                FxaFormConsent.initForm(true);
            }
        }
    }
};

export default FxaFormConsent;
