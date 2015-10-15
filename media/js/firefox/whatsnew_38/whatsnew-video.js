/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
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
                    // track play event in GTM

                    window.dataLayer.push({
                        'event': 'video-play',
                        'videoTitle': 'When its Personal Campaign Video'
                    });
                }, 500);
            }
        });
    });

    // auto close the modal after video finishes
    $video.on('ended', function() {
        setTimeout(function() {
            Mozilla.Modal.closeModal();
            // track video end event in GTM

            window.dataLayer.push({
                'event': 'video-complete',
                'videoTitle': 'When its Personal Campaign Video'
            });
        }, 1000);
     });

 })(window.jQuery, window.Mozilla);
