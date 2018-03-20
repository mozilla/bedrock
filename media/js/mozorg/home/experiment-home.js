/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


/* Experiment: https://bugzilla.mozilla.org/show_bug.cgi?id=1443566
 * URL: https://www.mozilla.org/en-US/
 * Audience: en-US
 * Traffic: 60% audience, 30/30 split*/

(function() {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'experiment_home_2018',
        variations: {
            'v=a': 30, // 30% redirected to home page redesign
            'v=b': 30   // 30% redirected to control
        }
    });
    cop.init();

})(window.Mozilla);
