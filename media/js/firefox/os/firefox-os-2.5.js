/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    function trackClick(e) {
        e.preventDefault();
        var id = $(e.target).data('id');
        ftGoalTag14004(id);
    }

    function ftGoalTag14004(id){
        var ftRand = Math.random() + '';
        var num = ftRand * 1000000000000000000;
        var ftGoalTagPix14004 = new Image();

        ftGoalTagPix14004.src = 'https://servedby.flashtalking.com/spot/8/6247;52161;4669/?spotName=' + id + '&cachebuster=' + num;

        setTimeout(ftLoaded14004, 400);
    }

    function ftLoaded14004() {
        window.location.href = 'https://d2yw7jilxa8093.cloudfront.net/B2GDroid-mozilla-central-nightly-latest.apk';
    }

    if (!window._dntEnabled()) {
        $('.cta-button').on('click', trackClick);
    }

})(jQuery);
