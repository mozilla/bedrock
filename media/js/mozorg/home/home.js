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

    function initVideoEvents() {
        var videos = document.querySelectorAll('video');
        var videoCards = document.querySelectorAll('.card.has-video .card-block-link');

        // open and play videos in a modal on click.
        for (var i = 0; i < videoCards.length; i++) {
            videoCards[i].addEventListener('click', playVideo, false);
        }

        // track video interaction events for GA.
        for (var j = 0; j < videos.length; j++) {
            videos[j].addEventListener('play', function() {
                trackVideoInteraction(this.getAttribute('data-ga-label'), 'play');
            }, false);

            videos[j].addEventListener('pause', function() {
                var action = this.currentTime === this.duration ? 'complete' : 'pause';
                trackVideoInteraction(this.getAttribute('data-ga-label'), action);
            }, false);
        }
    }

    function playVideo(e) {
        var $card = $(this);
        var $content = $card.next().find('.card-video-content');
        var title = $card.find('.card-title').text();

        if ($content.length) {
            e.preventDefault();
            var video = $content.find('video')[0];

            Mozilla.Modal.createModal(this, $content, {
                title: title,
                onCreate: function() {
                    try {
                        video.load();
                        video.play();
                    } catch(err) {
                        // fail silently
                    }
                },
                onDestroy: function() {
                    video.pause();
                }
            });
        }
    }

    // Lazyload images
    Mozilla.LazyLoad.init();

    // Video card interactions.
    initVideoEvents();
})();
