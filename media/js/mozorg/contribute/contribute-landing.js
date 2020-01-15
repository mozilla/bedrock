/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(){
    'use strict';

    function onVideoEnd() {
        window.dataLayer.push({
            event: 'contribute-video-ended'
        });
    }

    function playVideo(e) {
        e.preventDefault();

        var link = e.target;
        var video = document.getElementById('htmlPlayer');

        Mzp.Modal.createModal(link, video, {
            title: '',
            onCreate: function() {
                video.play();

                window.dataLayer.push({
                    'event': 'contribute-landing-interactions',
                    'browserAction': 'Video Interactions',
                    'location': 'Video text link'
                });
            },
            onDestroy: function() {
                video.pause();
                video.removeEventListener('ended', onVideoEnd, false);
            }
        });

        // Track when the video ends
        video.addEventListener('ended', onVideoEnd, false);
    }

    function onLoad() {
        // Play videos in a modal
        document.querySelector('.js-contribute-video').addEventListener('click', playVideo, false);
    }

    Mozilla.run(onLoad);

})();
