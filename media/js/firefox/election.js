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

(function() {
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

})();
