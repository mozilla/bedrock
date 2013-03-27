/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    "use strict";

    // default user action to auto
    var action = 'auto';

    // declare slideshow options
    // @requires: sequencejs
    var options = {
        nextButton: '.next',
        prevButton: '.prev',
        autoPlay: true,
        autoPlayDelay: 7000,
        pauseOnHover: true,
        pauseIcon: '.pause-icon',
        pauseButton: true,
        fadeFrameWhenSkipped: false,
        animateStartingFrameIn: true,
        moveActiveFrameToTop: false,
    };
    
    // set up the slideshow
    // @requires: sequencejs
    var slideshow = $('#slideshow').sequence(options).data('sequence');

    var track = function() {
        // must use nextFrame here - currentFrame (oddly) isn't updated yet.
        console.log('tracking ' + slideshow.nextFrame[0].id + ' with action ' + action);

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
})(jQuery);
