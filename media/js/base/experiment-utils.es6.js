/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

const knownExperimentalParams = [
    'automation=true', // Automated functional tests
    'entrypoint_experiment=', // Firefox Accounts experiments
    'entrypoint_variation=',
    'experiment=', // Stub attribution experiments
    'variation=',
    'utm_medium=cpc', // Ad campaign tests
    'utm_source=firefox-browser' // Firefox in-product tests
];

/**
 * Check given URL against a list of well-know experemental query parameters.
 * Issue #10559
 * @param {String} params - query params, defaults to window.location.search.
 * @returns {Boolean} - return false if match is found.
 */
function isApprovedToRun(params) {
    let queryString =
        typeof params === 'string' ? params : window.location.search || null;

    if (queryString) {
        queryString = decodeURIComponent(queryString);

        return knownExperimentalParams.every((param) => {
            return queryString.indexOf(param) === -1;
        });
    }

    return true;
}

module.exports = {
    isApprovedToRun
};
