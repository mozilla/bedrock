/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $speed_graph = $('#speed-graph');

    if (document.body.id === 'firefox-desktop') {
        $speed_graph.closest('.container').waypoint(function() {
            $speed_graph.addClass('animate');
        }, {
            triggerOnce: true,
            offset: 100
        });
    } else {
        setTimeout(function() {
            $speed_graph.addClass('animate');
        }, 1000);
    }
})(window.jQuery);
