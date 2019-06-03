/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'experiment-about-page-performance',
        variations: {
            'v=a': 5,
            'v=b': 5,
            'v=c': 5,
            'v=d': 5,
            'v=e': 5,
            'v=f': 5,
            'v=g': 5,
            'v=h': 5,
            'v=i': 5,
            'v=j': 5
        }
    });

    cop.init();
})();
