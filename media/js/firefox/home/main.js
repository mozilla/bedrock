/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla, Waypoint) {
    'use strict';

    // Basic feature detect for JS support.
    function supportsBaselineJS() {
        return 'querySelector' in document &&
               'querySelectorAll' in document &&
               'addEventListener' in window &&
               typeof HTMLMediaElement !== 'undefined';
    }

    function trackVideoInteraction(title, state) {
        window.dataLayer.push({
            'event': 'video-interaction',
            'videoTitle': title,
            'interaction': state
        });
    }

    function initVideoInteractionTracking() {
        var videos = document.querySelectorAll('video');

        for (var i = 0; i < videos.length; i++) {
            videos[i].addEventListener('play', function() {
                trackVideoInteraction(this.getAttribute('data-ga-label'), 'play');
            }, false);

            videos[i].addEventListener('pause', function() {
                var action = this.currentTime === this.duration ? 'complete' : 'pause';
                trackVideoInteraction(this.getAttribute('data-ga-label'), action);
            }, false);
        }
    }

    // Init video poster helper and bind video interaction events for JS tracking.
    function initFasterVideo() {
        var videoPoster = new Mozilla.VideoPosterHelper('.key-features-section .key-feature-media.video');
        videoPoster.init();

        // Auto pause the video when scrolled out of view.
        new Waypoint({
            element: document.getElementById('faster-video'),
            handler: function(direction) {
                if (direction === 'down') {
                    try {
                        if (!this.element.paused) {
                            this.element.pause();
                        }
                    } catch(e) {
                        // Fail silently.
                    }
                }
            },
            offset: '-50%'
        });
    }

    // Bind one time scroll tracking events for main page sections.
    function initScrollTracking() {
        var sections = document.querySelectorAll('[data-scroll-tracking]');

        for (var i = 0; i < sections.length; i++) {
            new Waypoint({
                element: sections[i],
                handler: function(direction) {
                    if (direction === 'down') {
                        window.dataLayer.push({
                            'eAction': 'scroll',
                            'eLabel': this.element.getAttribute('data-scroll-tracking'),
                            'event': 'non-interaction'
                        });
                        this.destroy(); // only fire tracking events once
                    }
                },
                offset: '100%'
            });
        }
    }

    if (supportsBaselineJS()) {
        initFasterVideo();
        initScrollTracking();
        initVideoInteractionTracking();
    }

})(window.Mozilla, window.Waypoint);
