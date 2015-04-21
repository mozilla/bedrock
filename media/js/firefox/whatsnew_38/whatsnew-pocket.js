/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function(){
    'use strict';

    var $pageContent = $('#outer-wrapper');
    var $modalContent = $('#modal-content');
    var $videoEmbed = $modalContent.find('.video-embed');
    var videoTitle = $modalContent.find('h2').text();
    var $video = $('#whatsnew-video');
    var $videoThumbnail = $modalContent.find('.video-thumbnail');

    // opens the campaign video in mozid modal
    function initVideoModal() {
        Mozilla.Modal.createModal($pageContent[0], $videoEmbed, {
            title: videoTitle
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

        // hide thumbnail and play video on click
        $videoThumbnail.on('click', function (e) {
            e.preventDefault();
            $videoThumbnail.addClass('hidden');
            setTimeout(function() {
                $video[0].play();
            }, 150);
        });
    }

    // show video modal on page load only for those locales who have it
    if ($modalContent.length === 1) {
        initVideoModal();
    }
});
