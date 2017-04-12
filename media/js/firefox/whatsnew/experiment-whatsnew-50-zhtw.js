/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var greggs = new Mozilla.TrafficCop({
        id: 'experiment-firefox-whatsnew-50-zhtw',
        variations: {
            'v=a': 50, // send to device widget
            'v=b': 50 // QR code
        }
    });

    greggs.init();
})(window.Mozilla);
