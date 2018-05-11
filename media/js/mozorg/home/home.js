/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Waypoint) {
    'use strict';

    /*
     * Video Tracking
     */

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

    /*
     * Sticky CTA
     */


    var stickyCTA = document.getElementById('download-firefox-sticky-cta');
    $(stickyCTA).attr('aria-hidden', 'true');

    // add and remove aria-hidden
    var primaryTop = new Waypoint({
        element: document.getElementById('download-firefox-primary-cta'),
        handler: function(direction) {
            if(direction === 'down') {
                // becomes percivable as the user scrolls down
                $(stickyCTA).removeAttr('aria-hidden');
            } else {
                // hidden again as they scroll up
                $(stickyCTA).attr('aria-hidden', 'true');
            }
        }
    });

    // init dismiss button
    function initDismissStickyCTA() {
        // add button
        var $dismissButton = $('<button>').addClass('sticky-dismiss').text('Dismiss download prompt.');
        var $stickyWrapper = $(stickyCTA).find('.primary-wrapper');
        $dismissButton.appendTo($stickyWrapper);
        // listen for click
        $dismissButton.on('click', function(){
            // dismiss
            dismissStickyCTA();
        });
    }

    // handle dismiss
    function dismissStickyCTA() {
        // destroy waypoint
        primaryTop.destroy();
        // remove element
        $(stickyCTA).remove();
        // set cookie, if cookies are supported
        if (typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled()) {
            var d = new Date();
            d.setTime(d.getTime() + (30 * 24 * 60 * 60 * 1000)); // 30 days
            Mozilla.Cookies.setItem('sticky-home-cta-dismissed', 'true', d, '/');
        }
    }

    // check if previously dismissed
    // Check that cookies are enabled before seeing if one already exists.
    if (typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled()) {
        if (Mozilla.Cookies.getItem('sticky-home-cta-dismissed')) {
            // previously dismissed
            dismissStickyCTA();
        } else {
            // init the button
            initDismissStickyCTA();
        }
    }

})(window.Waypoint);
