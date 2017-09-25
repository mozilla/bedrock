/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla, Waypoint) {
    'use strict';

    var client = Mozilla.Client;
    var $slideShow = $('.feature-carousel');
    var $newsletterModal = $('.newsletter-modal');
    var stickyFooterWaypoint;
    var videoCarouselWaypoint;
    var otherFeaturesWaypoint;

    function cutsTheMustard() {
        return 'querySelector' in document &&
               'querySelectorAll' in document &&
               'addEventListener' in window &&
               typeof window.matchMedia !== 'undefined' &&
               typeof HTMLMediaElement !== 'undefined';
    }

    // Init newsletter modal signup CTA's.
    function initNewsletterSignUp() {
        var signUpLinks = document.querySelectorAll('.button.sign-up');

        for (var i = 0; i < signUpLinks.length; i++) {
            signUpLinks[i].setAttribute('role', 'button');
            signUpLinks[i].addEventListener('click', function(e) {
                e.preventDefault();
                Mozilla.Modal.createModal(this, $newsletterModal);
            }, false);
        }
    }

    // Init feature video carousel.
    function initVideoCarousel() {

        $slideShow.cycle({
            fx: 'scrollHorz',
            log: false,
            slides: '> li',
            speed: 620,
            prev: '.feature-carousel-previous',
            next: '.feature-carousel-next',
        });

        $slideShow.cycle('pause');

        /**
         * We only auto-play videos inline in the carousel for desktop users, since many mobile platforms
         * restrict auto play without direct user interaction, and also disallow inline video.
         */
        if (client.isDesktop) {

            var videos = document.querySelectorAll('.feature-carousel video');

            // remove standard controls and set each video to loop.
            for (var i = 0; i < videos.length; i++) {
                videos[i].removeAttribute('controls');
                videos[i].setAttribute('loop', '');
            }

            // triggered just prior to a transition to a new slide.
            $slideShow.on('cycle-before', function(event, optionHash, outgoingSlideEl, incomingSlideEl, forwardFlag) {
                var outgoingVideo = $(outgoingSlideEl).find('video')[0];
                var incomingVideo = $(incomingSlideEl).find('video')[0];
                var direction = forwardFlag ? 'Right' : 'Left';

                // pause the outgoing video.
                if (outgoingVideo && !outgoingVideo.paused) {
                    outgoingVideo.pause();
                }

                // reset the incoming video to the first frame.
                if (incomingVideo && incomingVideo.paused) {
                    // if a video is slow to load metadata may not yet be available, so fail gracefully.
                    try {
                        incomingVideo.currentTime = 0;
                    } catch(e) {
                        // empty
                    }
                }

                window.dataLayer.push({
                    'event': 'in-page-interaction',
                    'eAction': 'Button Click',
                    'eLabel': 'Carousel ' + direction
                });
            });

            // triggered after the slideshow has completed transitioning to the next slide.
            $slideShow.on('cycle-after', function(event, optionHash, outgoingSlideEl, incomingSlideEl) {
                var video = $(incomingSlideEl).find('video')[0];

                // play the incoming video.
                if (video && video.paused) {
                    playVideo(video);
                }
            });
        }
    }

    // Destroy feature video carousel.
    function destroyVideoCarousel() {
        var videos;
        var activeVideo = document.querySelector('.cycle-slide-active video');

        if (activeVideo && client.isDesktop) {
            activeVideo.pause();

            videos = document.querySelectorAll('.feature-carousel video');

            // reinstate videos to use standard controls.
            for (var i = 0; i < videos.length; i++) {
                videos[i].setAttribute('controls', '');
                videos[i].removeAttribute('loop');
            }
        }

        $slideShow.cycle('destroy');
    }

    // Scroll waypoints to automatically start / pause the video carousel as user scrolls in / out of section.
    function initVideoWaypoints() {

        videoCarouselWaypoint = new Waypoint({
            element: document.querySelector('.feature-carousel-container'),
            offset: '50%',
            handler: function(direction) {
                var video = document.querySelector('.cycle-slide-active video');

                if (video && client.isDesktop) {
                    if (direction === 'down') {
                        playVideo(video);
                    } else {
                        video.pause();
                    }
                }
            }
        });

        otherFeaturesWaypoint = new Waypoint({
            element: document.querySelector('.other-features'),
            offset: 0,
            handler: function(direction) {
                var video = document.querySelector('.cycle-slide-active video');

                if (video && client.isDesktop) {
                    if (direction === 'down') {
                        playVideo(video);
                    } else {
                        video.play();
                    }
                }
            }
        });
    }

    function playVideo(video) {
        if (video.readyState && video.readyState > 0) {
            video.play();
        }
    }

    // Scroll waypoints for GA tracking.
    function initScrollTracking() {
        var sections = document.querySelectorAll('[data-scroll-tracking]');

        for (var i = 0; i < sections.length; i++) {
            new Waypoint({
                element: sections[i],
                handler: function(direction) {
                    if (direction === 'down') {
                        window.dataLayer.push({
                            event: 'scroll-section',
                            interaction: 'scroll',
                            section: this.element.getAttribute('data-scroll-tracking')
                        });
                    }
                },
                offset: '100%'
            });
        }
    }

    // Only init video carousel for wide viewports on desktop browsers.
    function initMediaQueries() {
        var desktopWidth;

        desktopWidth = matchMedia('(min-width: 1000px)');

        if (desktopWidth.matches) {
            initVideoCarousel();
            initVideoWaypoints();
            initStickyFooter();
        }

        desktopWidth.addListener(function(mq) {
            if (mq.matches) {
                initVideoCarousel();
                initVideoWaypoints();
                initStickyFooter();
            } else {
                destroyVideoCarousel();
                destroyWaypoints();
            }
        });
    }

    // Init sticky footer CTA as user scrolls past key features section.
    function initStickyFooter() {
        stickyFooterWaypoint = new Waypoint.Sticky({
            element: document.querySelector('.sticky-footer'),
            offset: 'bottom-in-view'
        });
    }

    // Destroy all waypoints used for UI interactions.
    function destroyWaypoints() {
        if (stickyFooterWaypoint) {
            stickyFooterWaypoint.destroy();
        }

        if (videoCarouselWaypoint) {
            videoCarouselWaypoint.destroy();
        }

        if (otherFeaturesWaypoint) {
            otherFeaturesWaypoint.destroy();
        }
    }

    // Basic feature detect for 1st class JS features.
    if (cutsTheMustard()) {
        document.querySelector('main').className = 'supports-videos';
        initMediaQueries();
        initScrollTracking();
        initNewsletterSignUp();
    }

})(window.Mozilla, window.Waypoint);
