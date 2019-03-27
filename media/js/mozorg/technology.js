/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global YT */
/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope
function onYouTubeIframeAPIReady() {
    'use strict';

    Mozilla.technologyOnYouTubeIframeAPIReady();
}

(function($) {
    'use strict';

    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';

    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    function onYouTubeIframeAPIReady() {
        // show video modal when user clicks play button
        $('.hero-rust-video a.video-play').attr('role', 'button').click(function(e) {
            e.preventDefault();

            var $videoContainer = $('#video-container');
            var video = $videoContainer.find('.video')[0];
            var videoTitle = $(this).data('videoTitle');

            var player = new YT.Player(video, {
                height: '390',
                width: '640',
                videoId: '8EPsnf_ZYU0',
                events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });

            function onPlayerReady(event) {
                event.target.playVideo();
            }

            function onPlayerStateChange(event) {
                var state;

                switch(event.data) {
                case YT.PlayerState.PLAYING:
                    state = 'video play';
                    break;
                case YT.PlayerState.PAUSED:
                    state = 'video paused';
                    break;
                case YT.PlayerState.ENDED:
                    state = 'video complete';
                    break;
                }

                if (state) {
                    window.dataLayer.push({
                        'event': 'video-interaction',
                        'videoTitle': videoTitle,
                        'interaction': state
                    });
                }
            }

            Mozilla.Modal.createModal(this, $videoContainer, {
                onDestroy: function() {
                    player.destroy();
                }
            });
        });
    }

    Mozilla.technologyOnYouTubeIframeAPIReady = onYouTubeIframeAPIReady;

})(window.jQuery);
