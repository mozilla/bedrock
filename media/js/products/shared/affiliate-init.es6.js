/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import AffiliateAttribution from './affiliate-attribution.es6';

function initAttributionFlow(e) {
    const hasConsent = e.detail.analytics;

    if (hasConsent) {
        if (AffiliateAttribution.meetsRequirements()) {
            AffiliateAttribution.init().catch((e) => {
                console.error(e); // eslint-disable-line no-console
            });
        } else {
            // Just add flow params as normal.
            AffiliateAttribution.addFlowParams();
        }

        window.removeEventListener(
            'mozConsentStatus',
            initAttributionFlow,
            false
        );
    }
}

window.addEventListener('mozConsentStatus', initAttributionFlow, false);
