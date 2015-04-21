/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function(){
    'use strict';

    var $videoContent = $('#video-content');
    var $videoEmbed = $videoContent.find('.video-embed');
    var $video = $('#whatsnew-video');

    // show video modal on thumbnail click
    $('.video-thumbnail').on('click', function (e) {
        e.preventDefault();

        Mozilla.Modal.createModal(this, $videoEmbed, {
            onCreate: function() {
                setTimeout(function() {
                    $video[0].play();
                }, 500);
            }
        });
    });

    // auto close the modal after video finishes
    $video.on('pause', function() {
        // 'pause' event fires just before 'ended', so
        // using 'ended' results in extra pause tracking.
        if ($video[0].currentTime === $video[0].duration) {
            setTimeout(function() {
                Mozilla.Modal.closeModal();
            }, 500);
        }
     });
});
