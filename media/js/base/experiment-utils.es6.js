/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { gpcEnabled, dntEnabled } from './consent/utils.es6';

const knownExcludedParams = [
    'automation=true', // Automated functional tests
    'entrypoint_experiment=', // Mozilla accounts experiments
    'entrypoint_variation=',
    'experiment=', // Stub attribution experiments
    'variation=',
    'utm_medium=cpc', // Ad campaign tests
    'utm_source=firefox-browser', // Firefox in-product tests
    'reason=manual-update' // https://github.com/mozilla/bedrock/issues/11071
];

/**
 * Check given URL against a list of well-know experimental query parameters.
 * Issue #10559
 * @param {String} params - query params, defaults to window.location.search.
 * @param {String} ua - user agent, defaults to navigator.userAgent.
 * @returns {Boolean} - return false if match is found or if GPC / DNT are enabled.
 */
function isApprovedToRun(params, ua) {
    let queryString =
        typeof params === 'string' ? params : window.location.search || null;
    const userAgent = typeof ua === 'string' ? ua : navigator.userAgent || null;

    // Exclude Googlebot from experiment redirects issue #15773.
    if (userAgent && userAgent.indexOf('Googlebot') !== -1) {
        return false;
    }

    if (gpcEnabled()) {
        return false;
    }

    if (dntEnabled()) {
        return false;
    }

    if (queryString) {
        queryString = decodeURIComponent(queryString);

        return knownExcludedParams.every((param) => {
            return queryString.indexOf(param) === -1;
        });
    }

    return true;
}

export { isApprovedToRun };
