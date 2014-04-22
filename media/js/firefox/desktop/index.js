/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

 var FirefoxDesktop = window.FirefoxDesktop || {};

(function($) {
    $('#animateit').click(function(e) {
        e.preventDefault();

        $('#customize .animation-wrapper').toggleClass('animate');
    });

    var $customize_stage = $('#customize .stage');
    var $customize_animation = $('#intro .animation-wrapper');

    // animations only run on full desktop sized viewport
    if (FirefoxDesktop.isDesktopViewport) {
        // initiate animation just after page load.
        setTimeout(function() {
            $intro_animation.addClass('animate');
            $designed_animation.addClass('animate');
        }, 750);

        $('#flexible-replay').on('click', function(e) {
            e.preventDefault();

            // Fade out stages with opacity transition.
            $intro_stage.addClass('resetting');
            $designed_stage.addClass('resetting');

            // After opacity transition completes, reset animations by removing
            // 'animate' class, the restore opacity by removing the 'resetting'
            // class.
            setTimeout(function() {
                $intro_animation.removeClass('animate');
                $intro_stage.removeClass('resetting');

                $designed_animation.removeClass('animate');
                $designed_stage.removeClass('resetting');

                // After opacity has been restored, trigger the animations
                // again by adding the 'animate' class.
                setTimeout(function() {
                    $intro_animation.addClass('animate');
                    $designed_animation.addClass('animate');
                }, 200);
            }, 200);
        });
    }
})(window.jQuery);
