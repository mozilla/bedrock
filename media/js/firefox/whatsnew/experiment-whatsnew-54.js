/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var santangelo = new Mozilla.TrafficCop({
        id: 'experiment_whatsnew_55',
        variations: {
            'v=a': 33,  // double-control
            'v=b': 33,  // QR code, no app store badges
            'v=c': 33   // QR code, app store badges moved up
        }
    });

    santangelo.init();
})(window.Mozilla);
