/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'experiment_firefox_desktop_brand',
        variations: {
            'v=a': 2,  // control
            'v=b': 2,  // new brand
            'v=c': 2,  // new brand, no quantum
            'v=d': 2,  // new brand, browser in headline
            'v=e': 2   // new brand, product image
        }
    });

    cop.init();
})(window.Mozilla);
