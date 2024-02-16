/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope
window.onYouTubeIframeAPIReady = function () {
    'use strict';

    // Play the video only once the API is ready.
    Mozilla.pipVideoPlay();
};

(function () {
    'use strict';
    var locale =
        document.getElementsByTagName('html')[0].getAttribute('lang') ||
        'en-US';
    var videoLink = document.querySelector('.js-video-play');
    var src = 'https://www.youtube.com/iframe_api';

    function loadScript() {
        var tag = document.createElement('script');
        tag.src = src;
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }

    function isScriptLoaded() {
        return document.querySelector('script[src="' + src + '"]')
            ? true
            : false;
    }

    function playVideo() {
        var videoId = videoLink.getAttribute('data-id');
        var title = videoLink.getAttribute('data-video-title');

        // return early if youtube API fails to load or is blocked.
        if (typeof window.YT === 'undefined') {
            return;
        }

        var start = locale === 'en' ? 169 : 0;
        new window.YT.Player(videoLink, {
            width: 500,
            height: 281,
            videoId: videoId,
            playerVars: {
                start: start,
                modestbranding: 1, // hide YouTube logo.
                rel: 0 // do not show related videos on end.
            },
            events: {
                onReady: onPlayerReady,
                onStateChange: onPlayerStateChange
            }
        });

        function onPlayerReady(event) {
            event.target.playVideo();
        }

        function onPlayerStateChange(event) {
            var state;

            switch (event.data) {
                case window.YT.PlayerState.PLAYING:
                    state = 'video play';
                    break;
                case window.YT.PlayerState.PAUSED:
                    state = 'video paused';
                    break;
                case window.YT.PlayerState.ENDED:
                    state = 'video complete';
                    break;
            }

            if (state) {
                window.dataLayer.push({
                    event: 'video-interaction',
                    videoTitle: title,
                    interaction: state
                });
            }
        }
    }

    function initVideoPlayer() {
        // check to see if you youtube API is loaded before trying to play the video.
        if (!isScriptLoaded()) {
            loadScript();
        } else {
            playVideo();
        }
    }

    function init() {
        videoLink.setAttribute('role', 'button');

        videoLink.addEventListener('click', function (e) {
            e.preventDefault();
            initVideoPlayer();
        });
    }

    Mozilla.pipVideoPlay = playVideo;

    init();
})();
