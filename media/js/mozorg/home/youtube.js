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
    Mozilla.homePageVideoPlay();
};

(function () {
    'use strict';

    var src = 'https://www.youtube.com/iframe_api';
    var player;

    function getNextEl(el) {
        el = el.nextSibling;
        while (el) {
            if (el.nodeType === 1) {
                return el;
            }
            el = el.nextSibling;
        }
        return null;
    }

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
        var title = document.querySelector(
            '.mzp-c-modal-inner > header > h2'
        ).innerText;
        var videoLink = document.querySelector(
            '.mzp-c-modal-inner .video-play'
        );
        var videoId = videoLink.getAttribute('data-id');

        // if youtube API fails or is blocked, try redirecting to youtube.com
        if (typeof window.YT === 'undefined') {
            window.location.href = 'https://www.youtube.com/watch?v=' + videoId;
        }

        player = new window.YT.Player(videoLink, {
            width: 640,
            height: 360,
            videoId: videoId,
            playerVars: {
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

    function destroyVideoPlayer() {
        if (player) {
            player.destroy();
        }
    }

    function openVideoModal(e) {
        e.preventDefault();

        var card = e.currentTarget;
        var title = card.querySelector('.mzp-c-card-title').innerText;
        var sibling = getNextEl(card);
        var content = sibling.querySelector('.mzp-c-card-video-content');

        window.MzpModal.createModal(card, content, {
            title: title,
            className: 'mzp-has-media',
            onCreate: initVideoPlayer,
            onDestroy: destroyVideoPlayer
        });
    }

    function init() {
        var videoCards = document.querySelectorAll(
            '.mzp-c-card.has-video-embed .mzp-c-card-block-link'
        );

        for (var i = 0; i < videoCards.length; i++) {
            videoCards[i].addEventListener('click', openVideoModal, false);
        }
    }

    Mozilla.homePageVideoPlay = playVideo;

    init();
})();
