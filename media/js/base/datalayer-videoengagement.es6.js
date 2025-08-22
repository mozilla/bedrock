/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

// Match "Video Engagement" events from GA4:
// https://support.google.com/analytics/answer/9216061
const VideoEngagement = {};

// Set when video starts
VideoEngagement.title;
VideoEngagement.url;
// Set when metadata fully loads
VideoEngagement.duration = null;
// Match GA4 thresholds
VideoEngagement.progressThresholds = [10, 25, 50, 75];

VideoEngagement.sendEvent = (videoObject) => {
    window.dataLayer.push({
        visible: true,
        video_duration: VideoEngagement.duration,
        video_title: VideoEngagement.title,
        video_url: VideoEngagement.url,
        video_provider: 'self-hosted',
        video_current_time: videoObject.currentTime,
        video_percent: videoObject.percent,
        event: videoObject.event
    });
};

// https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/play_event
// NOTE: this event is configured to only fire once, does not need listener removed
VideoEngagement.handleStart = (e) => {
    VideoEngagement.url = e.target.currentSrc;
    VideoEngagement.title = e.target.dataset.gaTitle || e.target.title;

    VideoEngagement.sendEvent({
        event: 'video_start',
        currentTime: 0,
        percent: 0
    });
};

// Rounded because we don't need precise numbers
VideoEngagement.getPercentageComplete = (currentTime) => {
    return Math.round((currentTime / VideoEngagement.duration) * 100);
};

VideoEngagement.getPassedThresholds = (percentageComplete) => {
    return VideoEngagement.progressThresholds.filter(
        (threshold) => percentageComplete >= threshold
    );
};

// https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/timeupdate_event
VideoEngagement.handleProgress = (e) => {
    const currentTime = Math.round(e.target.currentTime);
    const percentageComplete =
        VideoEngagement.getPercentageComplete(currentTime);

    // Check if video has ended
    if (percentageComplete === 100) {
        // Send complete event
        VideoEngagement.sendEvent({
            event: 'video_complete',
            currentTime,
            percent: 100
        });

        // Stop sending events
        e.target.removeEventListener(
            'timeupdate',
            VideoEngagement.handleProgress
        );
    } else {
        // Check if we have a progress event to send
        const passedThresholds =
            VideoEngagement.getPassedThresholds(percentageComplete);
        if (passedThresholds.length > 0) {
            const lastThreshold = e.target.hasAttribute('data-ga-threshold')
                ? parseInt(e.target.getAttribute('data-ga-threshold'), 10)
                : 0;
            const currentThreshold =
                passedThresholds[passedThresholds.length - 1];
            // Send progress event if we've passed a new threshold
            if (currentThreshold > lastThreshold) {
                VideoEngagement.sendEvent({
                    event: 'video_progress',
                    currentTime,
                    percent: currentThreshold
                });
                // Store record of sent threshold data for this element
                e.target.setAttribute('data-ga-threshold', currentThreshold);
            }
        }
    }
};

export default VideoEngagement;
