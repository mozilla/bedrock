/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var carver = new Mozilla.TrafficCop({
        id: 'experiment-firefox-whatsnew-54-ja-zhcn',
        variations: {
            'v=c': 50, // control/no primary CTA
            'v=d': 50 // QR code
        }
    });

    carver.init();
})(window.Mozilla);
