/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

const TrackScroll = {};

let thresholds = [25, 50, 75, 90];

TrackScroll.getDepth = () => {
    const scrollHeight = document.documentElement.scrollHeight;
    const innerHeight = window.innerHeight;
    const scrollY = window.scrollY;
    const scrollPosition = innerHeight + scrollY;
    const depth = (100 * scrollPosition) / scrollHeight;
    return depth;
};

TrackScroll.sendEvent = (threshold) => {
    window.dataLayer.push({
        event: 'scroll',
        percent_scrolled: String(threshold)
    });
};

TrackScroll.scrollListener = () => {
    const currentDepth = TrackScroll.getDepth();

    // get a list of thresholds we've passed
    const matchingThresholds = thresholds.filter(
        (threshold) => currentDepth >= threshold
    );

    // remove thresholds we've passed from list of ones we're looking for
    thresholds = thresholds.filter((threshold) => currentDepth < threshold);

    // send the event for thresholds we passed
    matchingThresholds.forEach((threshold) => {
        TrackScroll.sendEvent(threshold);
    });

    // remove the event listener if we've scrolled past all thresholds
    if (thresholds.length === 0) {
        removeEventListener('scroll', TrackScroll.scrollListener);
    }
};

export default TrackScroll;
