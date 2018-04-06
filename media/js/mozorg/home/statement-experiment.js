/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';
    
    // example configuration for a redirect experiment
    var cop = new Mozilla.TrafficCop({
        id: 'experiment-home-statement',
        variations: {
            'v=1': 50,
            'v=2': 50
        }
    });

    cop.init();

})(window.Mozilla);
