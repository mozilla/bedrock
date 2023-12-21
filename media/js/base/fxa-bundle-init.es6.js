/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FxaLink from './fxa-link.es6.js';
import FxaAttribution from './fxa-attribution.es6.js';
import FxaCoupon from './fxa-coupon.es6.js';

let urlParams;

if (typeof window._SearchParams !== 'undefined') {
    urlParams = new window._SearchParams();
}

function handleEvent(e) {
    const hasConsent = e.detail.analytics;

    if (hasConsent) {
        // Track external URL parameter referrals for Mozilla account links.
        FxaAttribution.init(urlParams.params);

        window.removeEventListener('mozConsentStatus', handleEvent, false);
    }
}

// Pass coupon URLs through to FxA subscription links.
FxaCoupon.init();

if (urlParams) {
    window.addEventListener('mozConsentStatus', handleEvent, false);

    // Configure Mozilla account links for Sync on desktop.
    FxaLink.init();
}
