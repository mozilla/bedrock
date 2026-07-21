/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import VideoEngagement from './datalayer-videoengagement.es6';

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

window.Mozilla.VideoEngagement = VideoEngagement;

// Init tracking on HTML videos
// YouTube video tracking is handled automatically with GA4 enhanced measurement
const HTMLVideos = document.querySelectorAll('.ga-video-engagement');
for (let i = 0; i < HTMLVideos.length; ++i) {
    const video = HTMLVideos[i];
    video.addEventListener('play', VideoEngagement.handleStart, {
        once: true
    });
    // Floor duration because we don't need precise numbers here
    video.addEventListener('loadedmetadata', (e) => {
        VideoEngagement.duration = Math.floor(e.target.duration);
    });
    // 'timeupdate' will handle both video_progress and video_complete data
    // ('ended' not reliable: if 'loop' is true, it will not fire)
    video.addEventListener('timeupdate', VideoEngagement.throttledProgress);
}
