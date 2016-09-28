/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'home_link_style_test',
        variations: {
            'v=a': 25,
            'v=b': 25
        }
    });

    cop.init();
})(window.Mozilla);
