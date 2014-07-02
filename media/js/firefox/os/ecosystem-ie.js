/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var $videos = $('video');

    // GA tracking on videos
    $videos.on('play', function() {
        gaTrack(['_trackEvent', '/os/ecosytem/ Interactions', $(this).attr('id'), 'Play']);
    }).on('pause', function() {
        // is video over?
        // 'pause' event fires just before 'ended', so
        // using 'ended' results in extra pause tracking.
        var action = (this.currentTime === this.duration) ? 'Complete' : 'Pause';

        gaTrack(['_trackEvent', '/os/ecosytem/ Interactions', $(this).attr('id'), action]);
    });
})(window.jQuery);
