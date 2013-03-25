/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    "use strict";

    var options = {
        nextButton: '.next',
        prevButton: '.prev',
        autoPlay: true,
        autoPlayDelay: 3000,
        pauseOnHover: true,
        fadeFrameWhenSkipped: false,
        animateStartingFrameIn: true,
        moveActiveFrameToTop: false,
//        startingFrameID: '6',
    };

    var slideshow = $('#slideshow').sequence(options).data('sequence');

})();
