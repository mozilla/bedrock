/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    function trackVideoInteraction(title, state) {
        window.dataLayer.push({
            'event': 'video-interaction',
            'videoTitle': title,
            'interaction': state
        });
    }

    function initVideoInteractionTracking() {
        var video = document.getElementById('pip-video');

        video.addEventListener('play', function() {
            trackVideoInteraction(this.getAttribute('data-video-title'), 'video play');
        }, false);

        video.addEventListener('pause', function() {
            var action = this.currentTime === this.duration ? 'video complete' : 'video paused';
            trackVideoInteraction(this.getAttribute('data-video-title'), action);
        }, false);
    }

    function onLoad() {
        var videoPoster = new Mozilla.VideoPosterHelper('.pip-video');
        videoPoster.init();
        initVideoInteractionTracking();
    }

    window.Mozilla.run(onLoad);

})();
