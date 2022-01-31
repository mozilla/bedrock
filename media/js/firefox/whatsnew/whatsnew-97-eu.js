/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope, ugh.
window.onYouTubeIframeAPIReady = function () {
    'use strict';

    // Play the video only once the API is ready.
    Mozilla.wnpVideoPlay();
};

(function () {
    'use strict';

    var videoLink = document.querySelector('.js-video-play');
    var videoContainer = document.querySelector(
        '.mzp-c-modal-overlay-contents .video-play'
    );
    var videoId = videoContainer.getAttribute('data-id');
    var videoLang = videoContainer.getAttribute('data-lang');
    var src = 'https://www.youtube.com/iframe_api';
    var player;

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
        // if youtube API fails or is blocked, try redirecting to youtube.com
        if (typeof window.YT === 'undefined') {
            window.location.href = 'https://www.youtube.com/watch?v=' + videoId;
        }

        player = new window.YT.Player(videoContainer, {
            width: 640,
            height: 360,
            videoId: videoId,
            playerVars: {
                modestbranding: 1, // hide YouTube logo.
                rel: 0, // do not show related videos on end.
                cc_load_policy: 1, // turn on captions
                cc_lang_pref: videoLang // specify caption language
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
                    videoTitle: 'Mozilla: The Big Picture',
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

    function destroyVideoPlayer() {
        if (player) {
            player.destroy();
        }
    }

    function openVideoModal(e) {
        e.preventDefault();

        var content = document.querySelector('.mzp-c-modal-overlay-contents');

        Mzp.Modal.createModal(e.target, content, {
            title: null,
            className: 'mzp-has-media',
            onCreate: initVideoPlayer,
            onDestroy: destroyVideoPlayer
        });
    }

    function init() {
        videoLink.addEventListener('click', openVideoModal, false);
    }

    Mozilla.wnpVideoPlay = playVideo;

    init();
})();
