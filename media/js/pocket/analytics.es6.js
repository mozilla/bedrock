/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Ensure window.dataLayer is always defined, even if GTM might not have loaded.
window.dataLayer = window.dataLayer || [];

const PocketAnalytics = {
    loaded: false,

    loadGA: () => {
        // Google Tag Manager used to load GA4 (gtag.js)
        const GTM_CONTAINER_ID = document
            .getElementsByTagName('html')[0]
            .getAttribute('data-gtm-container-id');

        window.gtag = function () {
            window.dataLayer.push(arguments);
        };

        if (GTM_CONTAINER_ID) {
            const gaScript = document.createElement('script');
            gaScript.async = 'true';
            gaScript.type = 'text/javascript';
            gaScript.src = `https://www.googletagmanager.com/gtag/js?id=${GTM_CONTAINER_ID}`;
            const pageScript = document.getElementsByTagName('script')[0];
            pageScript.parentNode.insertBefore(gaScript, pageScript);

            window.gtag('js', new Date());
            window.gtag('config', GTM_CONTAINER_ID);
        }

        // Google Universal Analytics (analytics.js)
        const GOOGLE_ANALYTICS_ID = document
            .getElementsByTagName('html')[0]
            .getAttribute('data-google-analytics-id');

        if (GOOGLE_ANALYTICS_ID) {
            (function (i, s, o, g, r, a, m) {
                i['GoogleAnalyticsObject'] = r;
                (i[r] =
                    i[r] ||
                    function () {
                        (i[r].q = i[r].q || []).push(arguments);
                    }),
                    (i[r].l = 1 * new Date());
                (a = s.createElement(o)), (m = s.getElementsByTagName(o)[0]);
                a.async = 1;
                a.src = g;
                m.parentNode.insertBefore(a, m);
            })(
                window,
                document,
                'script',
                'https://www.google-analytics.com/analytics.js',
                'ga'
            );

            try {
                window.ga('create', GOOGLE_ANALYTICS_ID, 'auto');
                window.ga('require', 'displayfeatures');
                window.ga('send', 'pageview');
            } catch (e) {
                //do nothing
            }
        }
    },

    // SnowPlow Analytics.
    loadSnowPlow: (config) => {
        const SNOWPLOW_APP_ID = document
            .getElementsByTagName('html')[0]
            .getAttribute('data-snowplow-app-id');

        const SNOWPLOW_SCRIPT_SRC = document
            .getElementsByTagName('html')[0]
            .getAttribute('data-snowplow-script-src');

        const SNOWPLOW_CONNECT_URL = document
            .getElementsByTagName('html')[0]
            .getAttribute('data-snowplow-connect-url');

        if (!SNOWPLOW_APP_ID || !SNOWPLOW_SCRIPT_SRC || !SNOWPLOW_CONNECT_URL) {
            return;
        }

        function getUserData() {
            const data = {
                hashed_user_id: Mozilla.Cookies.getItem('a95b4b6'), // set only when logged-in through the Pocket app.
                hashed_guid: Mozilla.Cookies.getItem('sess_guid') // set only when visiting non-marketing pages.
            };
            Object.keys(data).forEach((key) => {
                if (data[key] === null) {
                    delete data[key];
                }
            });
            if (Object.keys(data).length) {
                return data;
            } else {
                return null;
            }
        }
        // https://docs.snowplowanalytics.com/docs/collecting-data/collecting-from-own-applications/javascript-trackers/javascript-tracker/javascript-tracker-v3/tracker-setup/loading/
        (function (p, l, o, w, i, n, g) {
            if (!p[i]) {
                p.GlobalSnowplowNamespace = p.GlobalSnowplowNamespace || [];
                p.GlobalSnowplowNamespace.push(i);
                p[i] = function () {
                    (p[i].q = p[i].q || []).push(arguments);
                };
                p[i].q = p[i].q || [];
                n = l.createElement(o);
                g = l.getElementsByTagName(o)[0];
                n.async = 1;
                n.src = w;
                g.parentNode.insertBefore(n, g);
            }
        })(window, document, 'script', SNOWPLOW_SCRIPT_SRC, 'snowplow');

        // https://docs.snowplowanalytics.com/docs/collecting-data/collecting-from-own-applications/javascript-trackers/javascript-tracker/javascript-tracker-v3/tracker-setup/initialization-options/
        window.snowplow('newTracker', 'sp', SNOWPLOW_CONNECT_URL, {
            appId: SNOWPLOW_APP_ID,
            platform: 'web',
            eventMethod: config.eventMethod,
            respectDoNotTrack: false,
            stateStorageStrategy: config.stateStorageStrategy,
            contexts: {
                webPage: true,
                performanceTiming: true
            },
            anonymousTracking: config.anonymousTracking
        });

        const data = getUserData();
        if (data) {
            window.snowplow('addGlobalContexts', {
                context: [
                    {
                        schema: `iglu:com.pocket/user/jsonschema/1-0-0`,
                        data
                    }
                ]
            });
        }
        window.snowplow('enableActivityTracking', {
            // integers are in seconds
            minimumVisitLength: 10,
            heartbeatDelay: 10
        });
        window.snowplow('enableLinkClickTracking');
        window.snowplow('enableFormTracking');
        window.snowplow('trackPageView');
    },

    loadAnalyticsScripts: (cookieConsent) => {
        // Configure snowplow based on cookie consent.
        const config = {
            eventMethod: cookieConsent ? 'beacon' : 'post',
            stateStorageStrategy: cookieConsent
                ? 'cookieAndLocalStorage'
                : 'none',
            anonymousTracking: cookieConsent
                ? false
                : { withServerAnonymisation: true }
        };

        try {
            PocketAnalytics.loadSnowPlow(config);

            // Only load GA if user consents to analytics cookies.
            if (cookieConsent) {
                PocketAnalytics.loadGA();
            }
        } catch (e) {
            // do nothing
        }

        PocketAnalytics.loaded = true;
    },

    reloadPage: () => {
        window.location.reload();
    }
};

window.PocketAnalytics = PocketAnalytics;

// Callback when OneTrust banner is either loaded or updated.
// This function *must* remain in global scope.
window.OptanonWrapper = function () {
    const activeGroups = window.OptanonActiveGroups;

    // C0002 is group ID for analytics cookies.
    const cookieConsent =
        typeof activeGroups === 'string' &&
        activeGroups.indexOf('C0002') !== -1;

    if (!PocketAnalytics.loaded) {
        PocketAnalytics.loadAnalyticsScripts(cookieConsent);
        return;
    } else if (!cookieConsent) {
        // Clear user data for existing snowplow session
        if (typeof window.snowplow === 'function') {
            window.snowplow('clearUserData', true, true);
        }

        // Reload the page to remove existing scripts.
        PocketAnalytics.reloadPage();
    }
};
