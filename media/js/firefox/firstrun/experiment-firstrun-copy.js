/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'experiment_firstrun_copy',
        variations: {
            'v=a': 5,  // double-control
            'v=b': 5   // copy test
        }
    });

    cop.init();
})(window.Mozilla);
