/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var rabbit = new Mozilla.TrafficCop({
        id: 'experiment_firefox_firstrun_fxa',
        variations: {
            'v=a': 2, // control
            'v=b': 2,
            'v=c': 2,
            'v=d': 2,
            'v=e': 2,
            'v=f': 2,
            'v=g': 2,
            'v=h': 2,
            'v=i': 2,
            'v=j': 2
        }
    });

    rabbit.init();
})(window.Mozilla);
