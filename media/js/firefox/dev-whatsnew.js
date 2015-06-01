/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// YouTube API hook has to be in global scope

// Videos are not yet ready for the whatsnew features (Performance Tools
// and What We Fixed). These videos are *probably* coming shortly after
// 6/2, so leaving this file here for easy implementation.

function onYouTubeIframeAPIReady() {
    'use strict';

    Mozilla.firstRunOnYouTubeIframeAPIReady();
}

;(function($, Mozilla) {
    'use strict';

    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    function onYouTubeIframeAPIReady() {

        // show video modal when user clicks a video play link
        $('a.video-play').attr('role', 'button').click(function(e) {
            e.preventDefault();

            var $this = $(this);
            var $videoContainer = $this.nextAll('.responsive-video-container');
            var $video = $this.nextAll('.responsive-video-container').children().first();

            // grab the nearby h2 tag as the modal window title
            var videoTitle = $this.siblings('h2').text();

            var player = new YT.Player($video.get(0), {
                height: '390',
                width: '640',
                videoId: $video.data('video-id'),
                events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });

            function onPlayerReady(event) {
                event.target.playVideo();

                window.dataLayer.push({
                    'event': 'video-interaction',
                    'interaction': 'play',
                    'videoTitle': videoTitle
                });
            }

            function onPlayerStateChange(event) {
                if (event.data === YT.PlayerState.ENDED) {
                    window.dataLayer.push({
                        'event': 'video-interaction',
                        'interaction': 'finish',
                        'videoTitle': videoTitle
                    });
                }
            }

            Mozilla.Modal.createModal(this, $videoContainer, {
                title: videoTitle,
                onDestroy: function() {
                    player.destroy();
                }
            });
        });

    }

    Mozilla.firstRunOnYouTubeIframeAPIReady = onYouTubeIframeAPIReady;

})(window.jQuery, window.Mozilla);
