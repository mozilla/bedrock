/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    function trackVideoInteraction(title, state) {
        window.dataLayer.push({
            event: 'video-interaction',
            videoTitle: title,
            interaction: state
        });
    }

    function initVideoInteractionTracking() {
        var video = document.getElementById('fbcontainer-video');

        if (!video) {
            return;
        }

        video.addEventListener(
            'play',
            function () {
                trackVideoInteraction(
                    this.getAttribute('data-ga-label'),
                    'play'
                );
            },
            false
        );

        video.addEventListener(
            'pause',
            function () {
                var action =
                    this.currentTime === this.duration ? 'complete' : 'pause';
                trackVideoInteraction(
                    this.getAttribute('data-ga-label'),
                    action
                );
            },
            false
        );
    }

    function onLoad() {
        initVideoInteractionTracking();
    }

    window.Mozilla.run(onLoad);
})();
