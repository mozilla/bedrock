/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import Glean from '@mozilla/glean/web';
import GleanMetrics from '@mozilla/glean/metrics';
import { pageEvent } from './page.es6';
import {
    consentRequired,
    getConsentCookie,
    isFirefoxDownloadThanks
} from '../base/consent/utils.es6';

const Utils = {
    /**
     * Takes a URL string and filters out any sensitive information,
     * such as newsletter tokens, before returning the URL.
     * See issue https://github.com/mozilla/bedrock/issues/13583
     * @param {String} URL
     * @returns {String} filtered URL
     */
    filterURL: (str) => {
        try {
            const url = new URL(str);
            const newsletterPaths = [
                '/newsletter/existing/',
                '/newsletter/country/'
            ];

            newsletterPaths.forEach((path) => {
                // Find the index of the newsletter pathname
                const index = url.pathname.indexOf(path);

                // Remove everything after the pathname (which is the token)
                if (index !== -1) {
                    const newPathname = url.pathname.substring(
                        0,
                        index + path.length
                    );
                    url.pathname = newPathname;
                }
            });

            return url.toString();
        } catch (e) {
            return str;
        }
    },

    /**
     * Determine if page URL is /firefox/download/thanks/.
     */
    isFirefoxDownloadThanks: () => {
        return isFirefoxDownloadThanks(window.location.href);
    },

    /**
     * Initialize Glean for sending pings.
     * @param {*} telemetryEnabled
     */
    initGlean: (telemetryEnabled) => {
        const pageUrl = window.location.href;
        const endpoint = 'https://www.mozilla.org';
        const channel = pageUrl.startsWith(endpoint) ? 'prod' : 'non-prod';

        /**
         * Ensure telemetry coming from automated testing is tagged
         * https://mozilla.github.io/glean/book/reference/debug/sourceTags.html
         */
        if (pageUrl.includes('automation=true')) {
            Glean.setSourceTags(['automation']);
        }

        Glean.initialize('bedrock', telemetryEnabled, {
            channel: channel,
            serverEndpoint: endpoint,
            enableAutoElementClickEvents: true
        });
    },

    /**
     * Record page load event and add custom metrics.
     */
    initPageLoadEvent: () => {
        /**
         * Manually call Glean's default page_load event. Here
         * we override `url` and `referrer` since we need to
         * apply some custom logic to these values before they
         * are sent.
         */
        GleanMetrics.pageLoad({
            url: Utils.filterURL(window.location.href),
            referrer: Utils.filterURL(document.referrer)
        });
    },

    initHelpers: () => {
        if (typeof window.Mozilla === 'undefined') {
            window.Mozilla = {};
        }

        /**
         * Creates global helpers on the window.Mozilla.Glean
         * namespace, so that external JS bundles can trigger
         * custom interaction events.
         */
        window.Mozilla.Glean = {
            /**
             * Note: pageEvent is not currently used in the codebase,
             * but will be useful for future implementations once we
             * align it more closely to follow the now standardized
             * Glean click event metrics.
             */
            pageEvent: (obj) => {
                try {
                    pageEvent(obj);
                } catch (e) {
                    // do nothing
                }
            },
            clickEvent: (obj) => {
                try {
                    GleanMetrics.recordElementClick(obj);
                } catch (e) {
                    // do nothing
                }
            }
        };
    },

    /**
     * Initialize Glean and fire page load event only if telemetry
     * is enabled.
     * @param {Boolean} telemetryEnabled
     */
    configureGlean: (telemetryEnabled) => {
        Utils.initGlean(telemetryEnabled);

        if (telemetryEnabled) {
            Utils.initPageLoadEvent();

            // Initialize global clickEvent helpers
            Utils.initHelpers();
        }
    },

    /**
     * Handle 'mozConsentStatus' event.
     * @param {Object} e - Event object.
     */
    handleConsent: (e) => {
        Utils.configureGlean(e.detail.analytics);
        window.removeEventListener(
            'mozConsentStatus',
            Utils.handleConsent,
            false
        );
    },

    /**
     * Configure Glean depending on data consent requirements.
     */
    bootstrapGlean: () => {
        // If visitor is in the EU/EAA wait for a consent signal.
        if (consentRequired()) {
            /**
             * If we're on /thanks/ and already have a consent cookie that
             * accepts analytics then load Glean. This is important because
             * a consent signal does not fire on /thanks/ in EU/EAA due to
             * the allow-list, but we still want to record downloads from
             * campaign pages that are allowed.
             */
            const cookie = getConsentCookie();

            if (
                Utils.isFirefoxDownloadThanks(window.location.href) &&
                cookie &&
                cookie.analytics
            ) {
                Utils.configureGlean(cookie.analytics);
            } else {
                window.addEventListener(
                    'mozConsentStatus',
                    Utils.handleConsent,
                    false
                );
            }
        } else {
            /**
             * Else if outside of EU/EAA, load analytics by default
             * (unless consent cookie rejects analytics).
             */
            const cookie = getConsentCookie();
            const consent = cookie ? cookie.analytics : true;
            Utils.configureGlean(consent);
        }
    }
};

export default Utils;
