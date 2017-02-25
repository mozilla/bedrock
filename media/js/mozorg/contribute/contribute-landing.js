/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    // Play videos in a modal
    $('a.video-play').attr('role', 'button').on('click', function(e) {
        e.preventDefault();

        var $this = $(this);
        var videoelem = $('#' + $this.attr('data-element-id'));

        Mozilla.Modal.createModal(this, videoelem, {
            title: '',
            onCreate: function() {
                playVideo();
            },
            onDestroy: function() {
                pauseVideo();
            }
        });

        // Track video plays
        var linktype = $this.data('linktype');
        window.dataLayer.push({
            'event': 'contribute-landing-interactions',
            'browserAction': 'Video Interactions',
            'location': linktype
        });
    });

    // Give the modal a chance to open before playing
    var playVideo = function() {
        var $video = $('#modal video:first');
        if ($video.length > 0) {
            setTimeout(function() {
                $video[0].play();
            }, 400);
            // Track when the video ends
            $video.on('ended', function() {
                window.dataLayer.push({
                    event: 'contribute-video-ended'
                });
            });
        }
    };

    // Pause the video when the modal is closed (Bug 1341242)
    var pauseVideo = function() {
        document.getElementById('htmlPlayer').pause();
    };

    // Track user scrolling through each section on the landing page
    $('#landing .section').waypoint(function(direction) {
        if (direction === 'down') {
            var sectionclass = $(this).prop('class');

            window.dataLayer.push({
                'event': 'scroll-section',
                'section': sectionclass
            });
        }
    }, { offset: '100%' });

})(window.jQuery);
