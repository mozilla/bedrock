/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var isDesktopViewport = $(window).width() >= 1000;

    var $feel_animation;
    var loopAnimation;

    if (isDesktopViewport) {
        $feel_animation = $('#feel-animation');

        loopAnimation = function() {
            setInterval(function() {
                $feel_animation.removeClass('animate');

                setTimeout(function() {
                    $feel_animation.addClass('animate');
                }, 100);
            }, 8800);
        };

        $('#feel').waypoint(function() {
            $feel_animation.addClass('animate');
            loopAnimation();
        }, {
            triggerOnce: true,
            offset: 50
        });
    }
})(window.jQuery);
