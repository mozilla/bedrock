/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'experiment-home-fx-copy',
        variations: {
            'v=a': 25,
            'v=b': 25,
            'v=c': 25,
            'v=d': 25 // double control group
        }
    });

    cop.init();
})(window.Mozilla);
