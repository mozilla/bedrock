/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    if (window.site.platform === 'ios' || window.site.platform === 'android') {
        var cop = new Mozilla.TrafficCop({
            id: 'experiment-about-page-performance-mobile',
            variations: {
                'v=a': 10,
                'v=b': 10,
                'v=c': 10,
                'v=d': 10,
                'v=e': 10,
                'v=f': 10,
                'v=g': 10,
                'v=h': 10,
                'v=i': 10,
                'v=j': 10
            }
        });

        cop.init();
    }

})();
