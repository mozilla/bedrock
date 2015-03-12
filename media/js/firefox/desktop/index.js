/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Mozilla) {
    'use strict';

    var isDesktopViewport = $(window).width() >= 1000;

    var $customize_stage = $('#customize .stage');
    var $customize_animation = $('#customize .animation-wrapper');

    // animations only run on full desktop sized viewport
    if (isDesktopViewport) {
        $('#customize').waypoint(function() {
            $customize_animation.addClass('animate');
        }, {
            triggerOnce: true,
            offset: 50
        });

        $('#flexible-replay').on('click', function(e) {
            e.preventDefault();

            // Fade out stage with opacity transition.
            $customize_stage.addClass('resetting');

            // After opacity transition completes, reset animation by removing
            // 'animate' class, then restore opacity by removing the 'resetting'
            // class.
            setTimeout(function() {
                $customize_animation.removeClass('animate');
                $customize_stage.removeClass('resetting');

                // After opacity has been restored, trigger the animation
                // again by adding the 'animate' class.
                setTimeout(function() {
                    $customize_animation.addClass('animate');
                }, 200);
            }, 200);

            // GA tracking
            gaTrack(['_trackEvent', 'firefox/desktop/ Interactions', 'replay link']);
        });
    }

    Mozilla.FxFamilyNav.init({ primaryId: 'desktop', subId: 'index' });
})(window.jQuery, window.Mozilla);
