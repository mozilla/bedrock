/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global YT */
/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope
function onYouTubeIframeAPIReady() {
    'use strict';

    Mozilla.initVideo();
}

(function(Mozilla) {
    'use strict';

    // Video
    var videoLink = document.querySelector('.js-video-play');

    if (videoLink) {
        var tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }

    function onYouTubeIframeAPIReady() {

        // lazy load video when visitor clicks the placeholder.
        var videoId = videoLink.getAttribute('data-id');

        videoLink.setAttribute('role', 'button');

        videoLink.addEventListener('click', function(e) {
            e.preventDefault();

            new YT.Player(videoLink, {
                height: '281',
                width: '500',
                videoId: videoId,
                playerVars: {
                    modestbranding: 1, // hide YouTube logo.
                    rel: 0, // do not show related videos on end.
                },
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
                        'videoTitle': 'Red Panda Cubs - Firefox + Woodland Park Zoo',
                        'interaction': state
                    });
                }
            }
        });
    }

    Mozilla.initVideo = onYouTubeIframeAPIReady;

})(window.Mozilla);
