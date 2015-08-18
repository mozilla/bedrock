/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var isDesktopViewport = $(window).width() >= 1000;

    var $feelAnimation;
    var loopAnimation;

    if (isDesktopViewport) {
        $feelAnimation = $('#feel-animation');

        loopAnimation = function() {
            setInterval(function() {
                $feelAnimation.removeClass('animate');

                setTimeout(function() {
                    $feelAnimation.addClass('animate');
                }, 100);
            }, 8800);
        };

        $('#feel').waypoint(function() {
            $feelAnimation.addClass('animate');
            loopAnimation();
            this.destroy(); // execute waypoint once
        }, {
            offset: 50
        });
    }
})(window.jQuery);
