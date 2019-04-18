/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'experiment-about-page-performance',
        variations: {
            'v=a': 2,
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

    cop.init();
})();
