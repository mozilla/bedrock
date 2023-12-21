/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import Glean from '@mozilla/glean/web';
import GleanMetrics from '@mozilla/glean/metrics';
import { recordCustomPageMetrics } from './page.es6';
import {
    consentRequired,
    getConsentCookie,
    isFirefoxDownloadThanks
} from '../base/consent/utils.es6';

const Utils = {
    filterNewsletterURL: (str) => {
        try {
            const url = new URL(str);

            // Ensure we don't include tokens in newsletter page load event pings
            // Issue https://github.com/mozilla/bedrock/issues/13583
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

    getUrl: (str) => {
        const url = typeof str === 'string' ? str : window.location.href;
        return Utils.filterNewsletterURL(url);
    },

    getPathFromUrl: (str) => {
        let pathName =
            typeof str === 'string' ? str : document.location.pathname;
        pathName = pathName.replace(/^(\/\w{2}-\w{2}\/|\/\w{2,3}\/)/, '/');
        const newsletterPaths = [
            '/newsletter/existing/',
            '/newsletter/country/'
        ];

        // Ensure we don't include tokens in newsletter page pings
        // Issue https://github.com/mozilla/bedrock/issues/13583
        newsletterPaths.forEach((path) => {
            if (pathName.includes(path)) {
                pathName = path;
            }
        });

        return pathName;
    },

    getLocaleFromUrl: (str) => {
        const pathName =
            typeof str === 'string' ? str : document.location.pathname;
        const locale = pathName.match(/^\/(\w{2}-\w{2}|\w{2,3})\//);
        // If there's no locale in the path then assume language is `en-US`;
        return locale && locale.length > 0 ? locale[1] : 'en-US';
    },

    getQueryParamsFromUrl: (str) => {
        const query = typeof str === 'string' ? str : window.location.search;

        if (typeof window._SearchParams !== 'undefined') {
            return new window._SearchParams(query);
        }

        return false;
    },

    getReferrer: (str) => {
        const referrer = typeof str === 'string' ? str : document.referrer;
        const url = Utils.filterNewsletterURL(referrer);

        return url;
    },

    getHttpStatus: () => {
        const pageId = document
            .getElementsByTagName('html')[0]
            .getAttribute('data-http-status');
        return pageId && pageId === '404' ? '404' : '200';
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
            serverEndpoint: endpoint
        });
    },

    /**
     * Record page load event and add custom metrics.
     */
    initPageLoadEvent: () => {
        recordCustomPageMetrics();

        /**
         * Manually call Glean's default page_load event. Here
         * we override `url` and `referrer` since we need to
         * apply some custom logic to these values before they
         * are sent.
         */
        GleanMetrics.pageLoad({
            url: Utils.getUrl(),
            referrer: Utils.getReferrer()
        });
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
