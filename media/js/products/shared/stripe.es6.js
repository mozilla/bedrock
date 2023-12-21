/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function handleEvent(e) {
    const hasConsent = e.detail.analytics;

    if (hasConsent) {
        // init Stripe Radar (3rd party script).
        const newScriptTag = document.createElement('script');
        const target = document.getElementsByTagName('script')[0];
        newScriptTag.src = 'https://js.stripe.com/v3/';
        target.parentNode.insertBefore(newScriptTag, target);

        window.removeEventListener('mozConsentStatus', handleEvent, false);
    }
}

window.addEventListener('mozConsentStatus', handleEvent, false);
