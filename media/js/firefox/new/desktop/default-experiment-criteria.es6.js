/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    hasConsentCookie,
    getConsentCookie
} from '../../../base/consent/utils.es6';

const experimentCookieID = 'download-as-default';

const utmParams = [
    'utm_source=',
    'utm_medium=',
    'utm_campaign=',
    'utm_term=',
    'utm_content='
];

function meetsExperimentCriteria(platform, params) {
    // Experiment specific feature detection.
    if (
        typeof window.URL !== 'function' ||
        typeof window.URLSearchParams !== 'function' ||
        !window.history.replaceState
    ) {
        return false;
    }

    // Experiment should only trigger for Windows.
    if (platform !== 'windows') {
        return false;
    }

    // Don't enter into experiment if cookies are disabled.
    if (!Mozilla.Cookies.enabled()) {
        return false;
    }

    // Don't enter into experiment if visitor has previously rejected analytics.
    if (hasConsentCookie()) {
        const cookie = getConsentCookie();

        if (!cookie.analytics) {
            return false;
        }
    }

    /**
     * Don't enter into experiment if there are any existing UTM parameters in
     * the page URL. We do not want to clobber those and overwrite existing
     * campaign data.
     */
    if (params) {
        const queryString = decodeURIComponent(params);
        return utmParams.every((param) => {
            return queryString.indexOf(param) === -1;
        });
    }

    // Don't enter into experiment if we already have an attribution cookie.
    if (
        (Mozilla.Cookies.hasItem('moz-stub-attribution-code') ||
            Mozilla.Cookies.hasItem('moz-stub-attribution-sig')) &&
        !Mozilla.Cookies.hasItem(experimentCookieID)
    ) {
        return false;
    }

    return true;
}

export { meetsExperimentCriteria, experimentCookieID };
