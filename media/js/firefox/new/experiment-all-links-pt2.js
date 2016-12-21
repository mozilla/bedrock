/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'exp_fx_new_scene1_all_links_pt2',
        variations: {
            'v=1': 3,  // modal
            'v=2': 3,  // in-page content
            'v=3': 3   // double control
        }
    });

    cop.init();
})(window.Mozilla);
