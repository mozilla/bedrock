/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function recordInteraction(state) {
    window.dataLayer.push({
        event: 'video-interaction',
        videoTitle: 'wnp-141',
        interaction: state
    });
}

function init() {
    const video = document.getElementById('wnp-video');

    video.addEventListener('play', () => recordInteraction('video play'));
    video.addEventListener('pause', () => recordInteraction('video paused'));
}

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

init();
