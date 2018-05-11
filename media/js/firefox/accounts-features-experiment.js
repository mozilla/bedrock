/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'experiment_accounts_features_headlines',
        variations: {
            'v=a': 50,
            'v=b': 50
        }
    });

    cop.init();
})(window.Mozilla);
