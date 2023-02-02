/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

let _gaLoaded = false;

/**
 * Ensure window.dataLayer is always defined,
 * even if GTM might not have loaded.
 */
window.dataLayer = window.dataLayer || [];

function loadGA() {
    /**
     * Google Tag Manager used to load GA4 (gtag.js)
     */
    const GTM_CONTAINER_ID = document
        .getElementsByTagName('html')[0]
        .getAttribute('data-gtm-container-id');

    function gtag() {
        window.dataLayer.push(arguments);
    }

    if (GTM_CONTAINER_ID) {
        const gaScript = document.createElement('script');
        gaScript.async = 'true';
        gaScript.type = 'text/javascript';
        gaScript.src = `https://www.googletagmanager.com/gtag/js?id=${GTM_CONTAINER_ID}`;
        const pageScript = document.getElementsByTagName('script')[0];
        pageScript.parentNode.insertBefore(gaScript, pageScript);

        gtag('js', new Date());
        gtag('config', GTM_CONTAINER_ID);
    }

    /**
     * Google Universal Analytics (analytics.js)
     */
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

    _gaLoaded = true;
}

// Callback when OneTrust banner is either loaded or updated.
// This function *must* remain in global scope.
window.OptanonWrapper = function () {
    const activeGroups = window.OptanonActiveGroups;

    // C0002 is group ID for analytics cookies.
    if (
        typeof activeGroups === 'string' &&
        activeGroups.indexOf('C0002') !== -1 &&
        !_gaLoaded
    ) {
        loadGA();
    }
};
