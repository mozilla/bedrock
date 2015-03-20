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
        if (event.metaKey || event.ctrlKey) {
            // Open link in new tab
            gaTrack(gaArgs);
        } else {
            event.preventDefault();
            gaTrack(gaArgs, function() { window.location = href; });
        }
    };

    // Setup GA tracking for misc links
    $('.feature .more').on('click', function(e) {
        trackClick([
            '_trackEvent',
            '/firefox/developer/ Interactions',
            'learn more link clicks',
            $(this).text()
        ], $(this).attr('href'), e);
    });

    // GA tracking for download buttons
    $('.intro .download-link').on('click', function(e) {
        trackClick([
            '_trackEvent',
            '/firefox/developer/ Interactions',
            'primary CTA - download click',
            'Firefox Developer Edition',
        ], $(this).attr('href'), e);
    });

    $('.dev-footer .download-link').on('click', function(e) {
        trackClick([
            '_trackEvent',
            '/firefox/developer/ Interactions',
            'secondary CTA - bottom download click',
            'Firefox Developer Edition',
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
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    'event': 'video-interaction',
                    'interaction': 'play',
                    'videoTitle': videoTitle
                });
            }

            function onPlayerStateChange(event) {
                if (event.data == YT.PlayerState.ENDED) {
                    window.dataLayer = window.dataLayer || [];
                    window.dataLayer.push({
                        'event': 'video-interaction',
                        'interaction': 'finish',
                        'videoTitle': videoTitle
                    });
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
