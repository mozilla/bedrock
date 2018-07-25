/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Waypoint) {
    'use strict';

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
        var videoCards = document.querySelectorAll('.mzp-c-card.has-video-embed .mzp-c-card-block-link');

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
        var card = e.currentTarget;
        var title = card.querySelector('.mzp-c-card-title').innerText;
        var sibling = getNextEl(e.currentTarget);
        var content = sibling.querySelector('.mzp-c-card-video-content');

        if (content) {
            e.preventDefault();
            var video = content.querySelector('video');

            Mozilla.Modal.createModal(this, content, {
                title: title,
                className: 'mzp-has-media',
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

})(window.Waypoint);
