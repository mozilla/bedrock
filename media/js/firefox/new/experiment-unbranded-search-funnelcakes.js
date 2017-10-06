/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    // initialize experiment - performs env check and does geo-lookup
    Mozilla.TCFCGeoExp.init({
        countryCode: 'us',
        experimentConfig: {
            id: 'experiment_unbranded_search_funnelcake',
            variations: {
                'f=130': 10,
                'f=131': 10,
                'f=132': 10
            }
        }
    });
})(window.Mozilla);
