/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// YouTube API hook has to be in global scope
function onYouTubeIframeAPIReady() {
    Mozilla.firstRunOnYouTubeIframeAPIReady();
}

;(function($) {
    'use strict';

    var tag = document.createElement('script');

    tag.src = 'https://www.youtube.com/iframe_api';
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


    var trackClick = function (gaArgs, href, event) {
        event.preventDefault();
        gaTrack(gaArgs, function() {
            window.location = href;
        });
    };

    // Setup GA tracking for misc links
    $('.feature .more').on('click', function(e) {
        trackClick([
            '_trackEvent',
            'Developer landing page Interactions',
            'learn more link clicks',
            $(this).text()
        ], $(this).attr('href'), e);
    });

    function onYouTubeIframeAPIReady() {

        // show video modal when user clicks a video play link
        $('a.video-play').attr('role', 'button').click(function(e) {
            e.preventDefault();

            var $this = $(this);
            var $videoContainer = $this.nextAll('.responsive-video-container');
            var $video = $this.nextAll('.responsive-video-container').children().first();

            // grab the nearby h2 tag as the modal window title
            var videoTitle = $this.siblings('h2').text();

            function onPlayerReady(event) {
                // Don't trigger video play on iOS or Android since mobile
                // Safari/Chrome don't allow a JS-triggered video
                if (window.site.platform !== 'ios' && window.site.platform !== 'android') {
                    event.target.playVideo();
                }
                gaTrack(
                    ['_trackEvent',
                     'Developer landing page Interactions',
                     'play',
                     videoTitle + ' video']
                );
            }

            function onPlayerStateChange(event) {
                if (event.data == YT.PlayerState.ENDED) {
                    gaTrack(
                        ['_trackEvent',
                         'Developer landing page Interactions',
                         'finish',
                         videoTitle + ' video']
                    );
                }
            }

            var player;

            Mozilla.Modal.createModal(this,
                $videoContainer, {
                title: videoTitle,
                onCreate: function() {
                    player = new YT.Player($video.get(0), {
                        height: '390',
                        width: '640',
                        videoId: $video.data('video-id'),
                        events: {
                            'onReady': onPlayerReady,
                            'onStateChange': onPlayerStateChange
                        }
                    });
                },
                onDestroy: function() {
                    player.destroy();
                }
            });
        });

    }

    Mozilla.firstRunOnYouTubeIframeAPIReady = onYouTubeIframeAPIReady;

})(window.jQuery, window.Mozilla);
