/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var dozerman = new Mozilla.TrafficCop({
        id: 'experiment-firefox-whatsnew-54-de',
        variations: {
            'v=a': 50, // send to device widget/control
            'v=b': 50 // QR code
        }
    });

    dozerman.init();
})(window.Mozilla);
