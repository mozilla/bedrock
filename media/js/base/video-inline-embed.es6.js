/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope
window.onYouTubeIframeAPIReady = function () {
    // Play the video only once the API is ready.
    Mozilla.YouTubeInlineEmbed();
};

const src = 'https://www.youtube.com/iframe_api';
let videoLink;
let videoId;
let videoStart;
let title;

function loadScript() {
    const tag = document.createElement('script');
    tag.src = src;
    const firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}

function isScriptLoaded() {
    return document.querySelector('script[src="' + src + '"]') ? true : false;
}

function playVideo() {
    // return early if youtube API fails to load or is blocked.
    if (typeof window.YT === 'undefined') {
        return;
    }

    new window.YT.Player(videoLink, {
        width: 640,
        height: 360,
        videoId: videoId,
        playerVars: {
            start: videoStart,
            modestbranding: 1, // hide YouTube logo.
            rel: 0, // do not show related videos on end.
            cc_load_policy: 1 // show captions.
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
        let state;

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
    const videos = document.querySelectorAll('.js-video-play');

    for (let i = 0; i < videos.length; i++) {
        videos[i].setAttribute('role', 'button');
        videos[i].addEventListener('click', (e) => {
            e.preventDefault();
            videoLink = e.currentTarget;
            videoId = videoLink.getAttribute('data-video-id');
            videoStart = parseInt(
                videoLink.getAttribute('data-video-start'),
                10
            );
            title = videoLink.getAttribute('data-video-title');
            initVideoPlayer();
        });
    }
}

Mozilla.YouTubeInlineEmbed = playVideo;

init();
