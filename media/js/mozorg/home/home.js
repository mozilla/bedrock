/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

 /* global YT */
 /* eslint no-unused-vars: [2, { "varsIgnorePattern": "onYouTubeIframeAPIReady" }] */

// YouTube API hook has to be in global scope
function onYouTubeIframeAPIReady() {
    'use strict';

    Mozilla.initHomePageVideos();
}

(function($, Waypoint) {
    'use strict';

    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    function getNextEl(el) {
        el = el.nextSibling;
        while (el) {
            if (el.nodeType === 1) {
                return el;
            }
            el = el.nextSibling;
        }
        return null;
    }

    function initHomePageVideos() {
        var videoCards = document.querySelectorAll('.mzp-c-card.has-video-embed .mzp-c-card-block-link');

        function playVideo(event) {
            var card = event.currentTarget;
            var title = card.querySelector('.mzp-c-card-title').innerText;
            var sibling = getNextEl(event.currentTarget);
            var content = sibling.querySelector('.mzp-c-card-video-content');

            var videoLink = content.querySelector('.video-play');
            var videoId = videoLink.getAttribute('data-id');

            var player = new YT.Player(videoLink, {
                width: 640,
                height: 360,
                videoId: videoId,
                playerVars: {
                    modestbranding: 1, // hide YouTube logo.
                    rel: 0, // do not show related videos on end.
                },
                events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });

            function onPlayerReady(event) {
                event.target.playVideo();
            }

            function onPlayerStateChange(event) {
                var state;

                switch(event.data) {
                case YT.PlayerState.PLAYING:
                    state = 'video play';
                    break;
                case YT.PlayerState.PAUSED:
                    state = 'video paused';
                    break;
                case YT.PlayerState.ENDED:
                    state = 'video complete';
                    break;
                }

                if (state) {
                    window.dataLayer.push({
                        'event': 'video-interaction',
                        'videoTitle': title,
                        'interaction': state
                    });
                }
            }

            if (content) {
                event.preventDefault();

                Mzp.Modal.createModal(this, content, {
                    title: title,
                    className: 'mzp-has-media',
                    onDestroy: function() {
                        player.destroy();
                    }
                });
            }
        }

        // open and play videos in a modal on click.
        for (var i = 0; i < videoCards.length; i++) {
            videoCards[i].addEventListener('click', playVideo, false);
        }
    }

    // Lazyload images
    Mozilla.LazyLoad.init();

    // Video card interactions.
    Mozilla.initHomePageVideos = initHomePageVideos;

    /*
    * Sticky CTA
    */

    var $stickyCTA = $(document.getElementById('download-firefox-sticky-cta'));
    var hasCookies = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();
    $stickyCTA.attr('aria-hidden', 'true');

    // init dismiss button
    function initStickyCTA() {
    // add and remove aria-hidden
        var primaryTop = new Waypoint({
            element: document.getElementById('download-firefox-primary-cta'),
            handler: function(direction) {
                if(direction === 'down') {
                // becomes percivable as the user scrolls down
                    $stickyCTA.removeAttr('aria-hidden');
                } else {
                // hidden again as they scroll up
                    $stickyCTA.attr('aria-hidden', 'true');
                }
            }
        });

        // add button
        var $dismissButton = $('<button>').addClass('sticky-dismiss').text('Dismiss download prompt.');
        var $stickyWrapper = $stickyCTA.find('.primary-wrapper');
        $dismissButton.appendTo($stickyWrapper);
        // listen for click
        $dismissButton.one('click', function(){
        // dismiss
            dismissStickyCTA(primaryTop);
        });
    }

    // handle dismiss
    function dismissStickyCTA(stickyWayPoint) {
        // destroy waypoint
        stickyWayPoint.destroy();
        // remove element
        $stickyCTA.remove();
        // set cookie, if cookies are supported
        if (hasCookies) {
            var d = new Date();
            d.setTime(d.getTime() + (30 * 24 * 60 * 60 * 1000)); // 30 days
            Mozilla.Cookies.setItem('sticky-home-cta-dismissed', 'true', d, '/');
        }
    }

    // Check if previously dismissed
    if (hasCookies) {
        if (!Mozilla.Cookies.getItem('sticky-home-cta-dismissed')) {
            // init the button
            initStickyCTA();
        } else {
            $stickyCTA.remove();
        }
    } else {
        $stickyCTA.remove();
    }

})(window.jQuery, window.Waypoint);
