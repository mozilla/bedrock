/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global YT */
/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope
function onYouTubeIframeAPIReady() {
    'use strict';

    // Play the video only once the API is ready.
    if (Mozilla.pipVideoPlay.videoId) {
        Mozilla.pipVideoPlay(Mozilla.pipVideoPlay.playerId, Mozilla.pipVideoPlay.videoId, Mozilla.pipVideoPlay.videoTitle);
    }
}

(function() {
    'use strict';

    var src = 'https://www.youtube.com/iframe_api';

    function loadScript() {
        var tag = document.createElement('script');
        tag.src = src;
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }

    function isScriptLoaded() {
        return document.querySelector('script[src="' + src + '"]') ? true : false;
    }

    function playVideo(playerId, videoId, videoTitle) {
        new YT.Player(playerId, {
            width: 640,
            height: 360,
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
            event.target.playVideo(playerId, videoId, videoTitle);
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
    }

    function initVideoPlayer(playerId, videoId, videoTitle) {
        // check to see if you youtube API is loaded before trying to play the video.
        if (!isScriptLoaded()) {
            loadScript();
        } else {
            playVideo(playerId, videoId, videoTitle);
        }
    }


    function init() {
        var videoLinks = document.querySelectorAll('.js-video-play');
        var tryButton = document.getElementById('try-button');

        tryButton.addEventListener('click', function(e) {
            Mozilla.pipVideoPlay.playerId = 'player1';
            Mozilla.pipVideoPlay.videoId = tryButton.getAttribute('data-id');
            Mozilla.pipVideoPlay.videoTitle = tryButton.getAttribute('data-video-title');
            e.preventDefault();
            initVideoPlayer(Mozilla.pipVideoPlay.playerId, Mozilla.pipVideoPlay.videoId, Mozilla.pipVideoPlay.videoTitle);
        });

        for (var i = 0; i < videoLinks.length; i++) {
            videoLinks[i].setAttribute('role', 'button');
            videoLinks[i].addEventListener('click', function(e) {
                Mozilla.pipVideoPlay.playerId = this.getAttribute('id');
                Mozilla.pipVideoPlay.videoId = this.getAttribute('data-id');
                Mozilla.pipVideoPlay.videoTitle = this.getAttribute('data-video-title');
                e.preventDefault();
                initVideoPlayer(Mozilla.pipVideoPlay.playerId, Mozilla.pipVideoPlay.videoId, Mozilla.pipVideoPlay.videoTitle);
            });
        }
    }

    Mozilla.pipVideoPlay = playVideo;
    Mozilla.pipVideoPlay.playerId;
    Mozilla.pipVideoPlay.videoId;
    Mozilla.pipVideoPlay.videoTitle;

    init();
})();
