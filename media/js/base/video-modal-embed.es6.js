/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope, ugh.
window.onYouTubeIframeAPIReady = function () {
    // Play the video only once the API is ready.
    Mozilla.YouTubeModalEmbed();
};

const src = 'https://www.youtube.com/iframe_api';
let player;

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
    const tag = document.createElement('script');
    tag.src = src;
    const firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}

function isScriptLoaded() {
    return document.querySelector('script[src="' + src + '"]') ? true : false;
}

function playVideo() {
    const videoLink = document.querySelector(
        '.mzp-c-modal-inner .video-player-frame'
    );
    const videoId = videoLink.getAttribute('data-video-id');
    const videoStart = parseInt(videoLink.getAttribute('data-video-start'), 10);

    // if youtube API fails or is blocked, try redirecting to youtube.com
    if (typeof window.YT === 'undefined') {
        window.location.href = 'https://www.youtube.com/watch?v=' + videoId;
    }

    player = new window.YT.Player(videoLink, {
        width: 1280,
        height: 720,
        videoId: videoId,
        playerVars: {
            start: videoStart,
            modestbranding: 1, // hide YouTube logo.
            rel: 0, // do not show related videos on end.
            cc_load_policy: 1 // show captions.
        },
        events: {
            onReady: onPlayerReady
        }
    });

    function onPlayerReady(event) {
        event.target.playVideo();
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

    const video = e.currentTarget;
    const sibling = getNextEl(video);
    const content = sibling.querySelector('.js-video-content');
    const title = content
        .querySelector('.video-player-frame')
        .getAttribute('data-video-title');

    window.MzpModal.createModal(video, content, {
        title: title,
        className: 'mzp-has-media',
        onCreate: initVideoPlayer,
        onDestroy: destroyVideoPlayer
    });
}

function init() {
    const videos = document.querySelectorAll(
        '.js-video-play, .mzp-c-card.has-video-embed .mzp-c-card-block-link'
    );

    for (let i = 0; i < videos.length; i++) {
        videos[i].setAttribute('role', 'button');
        videos[i].addEventListener('click', openVideoModal, false);
    }
}

Mozilla.YouTubeModalEmbed = playVideo;

init();
