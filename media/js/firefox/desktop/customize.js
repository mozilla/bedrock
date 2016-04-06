/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Mozilla) {
    'use strict';

    var isDesktopViewport = $(window).width() >= 1000;
    var isSmallViewport = $(window).width() < 760;

    var $introStage = $('#intro .stage');
    var $designedStage = $('#designed .stage');

    var $introAnimation = $('#intro .animation-wrapper');
    var $designedAnimation = $('#designed .animation-wrapper');

    // animations only run on full desktop sized viewport
    if (isDesktopViewport) {
        // initiate animation just after page load.
        setTimeout(function() {
            $introAnimation.addClass('animate');
            $designedAnimation.addClass('animate');
        }, 750);

        $('#flexible-replay').on('click', function(e) {
            e.preventDefault();

            // Fade out stages with opacity transition.
            $introStage.addClass('resetting');
            $designedStage.addClass('resetting');

            // After opacity transition completes, reset animations by removing
            // 'animate' class, then restore opacity by removing the 'resetting'
            // class.
            setTimeout(function() {
                $introAnimation.removeClass('animate');
                $introStage.removeClass('resetting');

                $designedAnimation.removeClass('animate');
                $designedStage.removeClass('resetting');

                // After opacity has been restored, trigger the animations
                // again by adding the 'animate' class.
                setTimeout(function() {
                    $introAnimation.addClass('animate');
                    $designedAnimation.addClass('animate');
                }, 200);
            }, 200);

        });
    }

    if (!isSmallViewport) {
        // fire sync animation when scrolled to
        $('#sync').waypoint(function() {
            Mozilla.syncAnimation();
            this.destroy(); // only execute waypoint once
        }, {
            offset: 50
        });
    }

    // customize icons section
    var $customizerList = $('#customizer-list');

    // theme thumbnails
    var $themesThumbs = $('#themes-thumbs');

    // theme preview image
    var $themeDemo = $('#theme-demo');

    // store current customizer
    var currentCustomizer = 'themes';
    var previousCustomizer = '';

    // handle clicking on themes/add-ons/awesome bar icons
    $('.show-customizer').on('click', function(e) {
        e.preventDefault();

        var $this = $(this);

        // make sure action should be taken
        if ($this.attr('href').replace('#', '') !== currentCustomizer) {
            previousCustomizer = currentCustomizer;
            currentCustomizer = $this.attr('href').replace('#', '');

            // select correct customizer icon
            $customizerList.find('a').removeClass('selected');
            $customizerList.find('a[href="#' + currentCustomizer + '"]').addClass('selected');

            // apply correct class to icon list for arrow placement
            $customizerList.removeClass(previousCustomizer).addClass(currentCustomizer);

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
    $themesThumbs.on('click', 'button', function(e) {
        e.preventDefault();

        var $this = $(this);

        // de-select all
        $themesThumbs.find('button').removeClass('selected');

        // select clicked
        $this.addClass('selected');

        // figure out new image src
        var newSrc = $themeDemo.attr('src').replace(/(.*)theme-.*\.png/gi, '$1' + $this.prop('id') + '.png');

        // update image with new src
        $themeDemo.attr('src', newSrc);

    });
})(window.jQuery, window.Mozilla);
