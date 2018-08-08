/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'experiment-download-scene2-email-082018',
        variations: {
            'v=a': 50,
            'v=b': 50,
        }
    });

    cop.init();
})(window.Mozilla);
