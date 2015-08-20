/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $speedGraph = $('#speed-graph');

    if (document.body.id === 'firefox-desktop') {
        $speedGraph.closest('.container').waypoint(function() {
            $speedGraph.addClass('animate');
            this.destroy(); // execute waypoint once
        }, {
            offset: 100
        });
    } else {
        setTimeout(function() {
            $speedGraph.addClass('animate');
        }, 1000);
    }
})(window.jQuery);
