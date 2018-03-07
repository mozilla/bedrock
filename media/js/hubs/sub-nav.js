/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/*
Depends on:

js/libs/jquery.waypoints.min.js
js/libs/jquery.waypoints-sticky.min.js
*/

(function($, Waypoint) {
    'use strict';

    var mqShowNav;
    var subNavSticky;
    var $subNavElem = $('.moz-sub-nav');

    function enableDesktop() {
        if (mqShowNav) {
            subNavSticky = new Waypoint.Sticky({
                element: $subNavElem,
                offset: 0
            });
        }
    }

    // It's your world, IE
    if ($subNavElem.length && typeof matchMedia !== 'undefined') {
        mqShowNav = matchMedia('(min-width: 760px)');

        mqShowNav.addListener(function(mq) {
            if (mq.matches) {
                enableDesktop();
            } else {
                subNavSticky.destroy();
            }
        });

        if (mqShowNav.matches) {
            enableDesktop();
        }
    }

})(window.jQuery, window.Waypoint);
