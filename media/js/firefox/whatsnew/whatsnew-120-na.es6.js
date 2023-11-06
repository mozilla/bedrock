/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../base/experiment-utils.es6.js';
import MzpModal from '@mozilla-protocol/core/protocol/js/modal';

const href = window.location.href;
const videoLink = document.querySelector('.js-video-play');
const src = 'https://www.youtube.com/iframe_api';
const qrButton = document.querySelector('.qr-code-btn');
const modalContent = document.querySelector('.mzp-u-modal-content');

const initTrafficCop = () => {
    if (href.indexOf('v=') !== -1) {
        if (href.indexOf('v=1') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp120-video',
                'data-ex-name': 'wnp-120-experiment-na'
            });
        } else if (href.indexOf('v=2') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'wnp120-no-video',
                'data-ex-name': 'wnp-120-experiment-na'
            });
        }
    } else if (TrafficCop) {
        const murtaugh = new TrafficCop({
            id: 'wnp-120-expiriment-na',
            cookieExpires: 0,
            variations: {
                'v=1': 50, // Fakespot video
                'v=2': 50 // no video
            }
        });
        murtaugh.init();
    }
};

if (isApprovedToRun()) {
    initTrafficCop();
}

if (href.indexOf('v=1') !== -1) {
    init();
}

// YouTube API hook has to be in global scope
window.onYouTubeIframeAPIReady = () => {
    // Play the video only once the API is ready.
    Mozilla.pipVideoPlay();
};

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
    const videoId = videoLink.getAttribute('data-id');
    const title = videoLink.getAttribute('data-video-title');

    // return early if youtube API fails to load or is blocked.
    if (typeof window.YT === 'undefined') {
        return;
    }

    new window.YT.Player(videoLink, {
        width: 500,
        height: 281,
        videoId: videoId,
        playerVars: {
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
    videoLink.setAttribute('role', 'button');

    videoLink.addEventListener(
        'click',
        function (e) {
            e.preventDefault();
            initVideoPlayer();
        },
        false
    );
}

Mozilla.pipVideoPlay = playVideo;

// click handler for opening Modal with QR Code

function handleQrCodeModal(e) {
    e.preventDefault();
    MzpModal.createModal(e.target, modalContent, {
        closeText: 'Close Modal'
    });
}

qrButton.addEventListener('click', handleQrCodeModal, false);
