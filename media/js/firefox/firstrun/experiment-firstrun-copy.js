/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var moreland = new Mozilla.TrafficCop({
        id: 'experiment-fxfirstrun-copy-042018',
        variations: {
            'v=a': 2, // control
            'v=b': 2,
            'v=c': 2,
            'v=d': 2
        }
    });

    moreland.init();
})(window.Mozilla);
