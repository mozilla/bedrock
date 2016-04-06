/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $mapContainer = $('#map-container');

    window.scrollMwcMap = function() {
        setTimeout(function() {
            $mapContainer.animate({
                scrollLeft: '300px'
            }, 250, function() {
                setTimeout(function() {
                    $mapContainer.animate({
                        scrollLeft: '0px'
                    }, 250);
                }, 350);
            });
        }, 500);
    };
})(window.jQuery);
