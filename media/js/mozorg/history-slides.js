/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function(w, $) {
    "use strict";

    // default user action to auto
    var action = 'auto';
    var $window = $(window);
    var $body = $('body');
    var $slideshow = $('#slideshow');
    var wideMode = false;
    var hasMediaQueries = (typeof matchMedia !== 'undefined');

    // declare slideshow options
    var options = {
        nextButton: '.next',
        prevButton: '.prev',
        autoPlay: true,
        autoPlayDelay: 8500,
        pauseOnHover: true,
        moveActiveFrameToTop: false,
        fadeFrameWhenSkipped: false,
        animateStartingFrameIn: true,
        reverseAnimationsWhenNavigatingBackwards: true,
        preventDelayWhenReversingAnimations: true,
        swipeEvents: {
            left: "next",
            right: "prev",
            up: false,
            down: false
        }
    };

    // set up the slideshow
    // @requires: sequencejs
    var slideshow = $slideshow.sequence(options).data('sequence');


    // If the browser supports media queries, check the width onload and onresize.
    // If not, just lock it in permanent wideMode.
    if (hasMediaQueries) {
        checkWidth();
        $window.on('resize', function() {
            clearTimeout(this.resizeTimeout);
            this.resizeTimeout = setTimeout(checkWidth, 200);
        });
    } else {
        wideMode = true;
        $body.addClass('wide');
        $slideshow.addClass('on');
    }

    function checkWidth() {
        if (window.matchMedia('screen and (min-width: 1000px)').matches) {
            wideMode = true;
            $body.addClass('wide');
            $slideshow.addClass('on');
            slideshow.startAutoPlay();
        } else {
            wideMode = false;
            $body.removeClass('wide');
            $slideshow.removeClass('on');
            slideshow.stopAutoPlay();
        }
    }


    // Track slide views
    var track = function() {
        // must use nextFrame here - currentFrame (oddly) isn't updated yet.
        gaTrack(['_trackEvent', 'mozilla15 SlideShow', action, slideshow.nextFrame[0].id]);

        // reset action to autoplay
        action = 'auto';
    };

    // track animations when next frame comes in
    slideshow.afterNextFrameAnimatesIn = function() {
        track();
    };

    $('.next, .prev').on('click', function(e) {
        e.preventDefault();
        action = 'click';
    });

    $(document).on('keydown', function(e) {
        var key = e.keyCode;

        if (key === 39 || key === 37) {
            action = 'keydown';
        }
    });

})(window, jQuery);
