/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    $('.cta-button').on('click', function(e) {
        if (!window._dntEnabled()) {
            e.preventDefault();
            ftGoalTag14004();
        }
    });

    function ftGoalTag14004(){
        var ftRand = Math.random() + '';
        var num = ftRand * 1000000000000000000;
        var ftGoalTagPix14004 = new Image();

        ftGoalTagPix14004.src = 'https://servedby.flashtalking.com/spot/2713;14004;1723/?spotName=submit_button&cachebuster=' + num;

        setTimeout(ftLoaded14004, 300);
    }

    function ftLoaded14004() { 
        window.location.href = 'https://d2yw7jilxa8093.cloudfront.net/B2GDroid-mozilla-central-nightly-latest.apk';
    } 

})(jQuery);
