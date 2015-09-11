/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla, Waypoint) {
    'use strict';

    var $html = $('html');
    var $nav = $('#nav');

    var stickyNav = new Waypoint.Sticky({
        element: $nav,
        handler: function(direction){
            if(direction == 'down'){
                $nav.addClass('fixedNav');
            } else{
                $nav.removeClass('fixedNav');
            }

        }
    });

    if (window.isFirefox() || window.isFirefoxiOS()) {
        // iOS
        if ($html.hasClass('ios')) {
            // all iOS users have private browsing
            $html.addClass('firefox-up-to-date');

        // Android or desktop
        } else {
            // desktop & Android version numbers match
            if (window.getFirefoxMasterVersion() >= 42)  {
                // try private browsing button is available
                $html.addClass('firefox-up-to-date');

                if ($html.hasClass('android')) {
                    // update SUMO link
                } else {
                    // initialize UITour
                }
            } else {
                $html.addClass('firefox-old');
            }
        }
    } else {
        $html.addClass('non-firefox');
    }

})(window.jQuery, window.Mozilla, window.Waypoint);
