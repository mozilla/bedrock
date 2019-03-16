/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'experiment_firefox_desktop_brand',
        variations: {
            'v=a': 93,  // control
            'v=b': 7   // new brand
        }
    });

    cop.init();
})(window.Mozilla);
