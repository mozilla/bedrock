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
let listening = true;

function debounce(func, delay) {
    let timer;
    return function () {
        clearTimeout(timer);
        timer = setTimeout(() => {
            func.apply(this, arguments);
        }, delay);
    };
}

// get what percentage of the page has been scrolled
TrackScroll.getDepth = (scrollHeight, innerHeight, scrollY) => {
    return (scrollY / (scrollHeight - innerHeight)) * 100;
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

TrackScroll.scrollHandler = () => {
    // check the browser supports filter before doing anything else
    if (typeof Array.prototype.filter === 'function') {
        const scrollHeight = document.documentElement.scrollHeight;
        const innerHeight = window.innerHeight;
        const scrollY = window.scrollY;
        const currentDepth = TrackScroll.getDepth(
            scrollHeight,
            innerHeight,
            scrollY
        );

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

TrackScroll.onScroll = debounce(TrackScroll.scrollHandler, 100);

export default TrackScroll;
