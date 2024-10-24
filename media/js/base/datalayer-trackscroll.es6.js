/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

const TrackScroll = {};

// track when page has been scrolled these percentages:
let thresholds = [25, 50, 75, 90];
// variables to support both throttle and debounce
const pushDelay = 200;
let lastPush = 0;
let pushTimer;
let listening = true;

// get what percentage of the page has been scrolled
TrackScroll.getDepth = () => {
    const scrollHeight = document.documentElement.scrollHeight;
    const innerHeight = window.innerHeight;
    const scrollY = window.scrollY;
    const scrollPosition = innerHeight + scrollY;
    const depth = (100 * scrollPosition) / scrollHeight;
    return depth;
};

// log the event to the dataLayer
TrackScroll.sendEvent = (threshold) => {
    window.dataLayer.push({
        event: 'scroll',
        percent_scrolled: String(threshold)
    });
};

// removes the event listener after we're done
TrackScroll.removeListener = () => {
    if (listening) {
        window.removeEventListener('scroll', TrackScroll.scrollListener, false);
        listening = false;
    }
};

// delayed call to scrollHandler, will keep getting delayed if it keeps getting called (aka this is a debouced call)
TrackScroll.delayedScrollHandler = () => {
    clearTimeout(pushTimer);
    pushTimer = setTimeout(function () {
        TrackScroll.scrollHandler();
    }, pushDelay);
};

TrackScroll.scrollHandler = () => {
    // check the browser supports filter before doing anything else
    if (typeof Array.prototype.filter === 'function') {
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
            TrackScroll.removeListener();
        }
    } else {
        // if it's too old to support logging, remove the listener
        TrackScroll.removeListener();
    }
};

TrackScroll.scrollListener = () => {
    const now = new Date();

    // if it's been a while since the last one, log it
    if (now - lastPush >= pushDelay) {
        TrackScroll.scrollHandler();
        lastPush = new Date();
    }

    // cue up one last check after scrolling stops
    TrackScroll.delayedScrollHandler();
};

export default TrackScroll;
