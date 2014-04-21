/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

 var FirefoxDesktop = window.FirefoxDesktop || {};

(function($) {
    var $intro_stage = $('#intro .stage');
    var $designed_stage = $('#designed .stage');

    var $intro_animation = $('#intro .animation-wrapper');
    var $designed_animation = $('#designed .animation-wrapper');

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

    // customize icons section
    var $customizer_list = $('#customizer-list');

    // theme thumbnails
    var $themes_thumbs = $('#themes-thumbs');

    // theme preview image
    var $theme_demo = $('#theme-demo');

    // store current customizer
    var current_customizer = 'themes';
    var previous_customizer = '';

    // handle clicking on themes/add-ons/awesome bar icons
    $('.show-customizer').on('click', function(e) {
        e.preventDefault();

        var $this = $(this);

        // make sure action should be taken
        if ($this.attr('href').replace('#', '') !== current_customizer) {
            previous_customizer = current_customizer;
            current_customizer = $this.attr('href').replace('#', '');

            // select correct customizer icon
            $customizer_list.find('a').removeClass('selected');
            $customizer_list.find('a[href="#' + current_customizer + '"]').addClass('selected');

            // apply correct class to icon list for arrow placement
            $customizer_list.removeClass(previous_customizer).addClass(current_customizer);

            var $curr = $('.customizer.active');

            var $next = $($this.attr('href'));

            $curr.fadeOut('fast', function() {
                $curr.removeClass('active');
            });

            // display specified customizer
            $next.fadeIn('fast').addClass('active');
        }
    });

    // handle clicks on theme thumbnails
    $themes_thumbs.on('click', 'a', function(e) {
        e.preventDefault();

        var $this = $(this);

        // de-select all
        $themes_thumbs.find('a').removeClass('selected');

        // select clicked
        $this.addClass('selected');

        // figure out new image src
        var new_src = $theme_demo.attr('src').replace(/(.*)theme-.*\.png/gi, "$1" + $this.attr('id') + '.png');

        // update image with new src
        $theme_demo.attr('src', new_src);
    });
})(window.jQuery);
