/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    BrowserClient,
    browserApiErrorsIntegration,
    dedupeIntegration,
    defaultStackParser,
    getCurrentScope,
    globalHandlersIntegration,
    httpContextIntegration,
    makeFetchTransport
} from '@sentry/browser';

import {
    consentRequired,
    dntEnabled,
    getConsentCookie,
    gpcEnabled
} from './consent/utils.es6';

const SentryConsent = {
    /**
     * Enable tree shaking of unused Sentry JS integrations.
     * https://docs.sentry.io/platforms/javascript/configuration/tree-shaking/
     */
    initClient: () => {
        // Get Data Source Name (DSN)
        const sentryDsn = document
            .getElementsByTagName('html')[0]
            .getAttribute('data-sentry-dsn');

        const client = new BrowserClient({
            dsn: sentryDsn,
            sampleRate: 0.1,
            transport: makeFetchTransport,
            stackParser: defaultStackParser,
            integrations: [
                dedupeIntegration(),
                globalHandlersIntegration(),
                httpContextIntegration,
                browserApiErrorsIntegration()
            ]
        });

        getCurrentScope().setClient(client);
        client.init();
    },

    /**
     * Handle 'mozConsentStatus' event.
     * @param {Object} e - Event object.
     */
    handleConsent: (e) => {
        const hasConsent = e.detail.analytics;

        if (hasConsent) {
            SentryConsent.initClient();
            window.removeEventListener(
                'mozConsentStatus',
                SentryConsent.handleEvent,
                false
            );
        }
    },

    /**
     * Initialize data consent for EU/EAA countries.
     */
    init: () => {
        /**
         * If either Global Privacy Control (GPC) or Do Not Track (DNT) are enabled
         * then we do not load Sentry.
         */
        if (gpcEnabled()) {
            return;
        }

        if (dntEnabled()) {
            return;
        }

        // If visitor is in the EU/EAA wait for a consent signal.
        if (consentRequired()) {
            window.addEventListener(
                'mozConsentStatus',
                SentryConsent.handleConsent,
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

            SentryConsent.initClient();
        }
    }
};

export default SentryConsent;
