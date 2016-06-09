/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Waypoint) {
    'use strict';

    var $navPage = $('#nav-page');

    // waypoints
    var actionWaypoint;
    var innovationWaypoint;
    var firefoxWaypoint;
    var suppressScrollTracking = false;
    var clickTargetSection;

    // intro slideshow
    var $slideshow = $('#home-slideshow');
    var mqIsTablet;

    // encryption video
    var encryptionVideoContainer = new Mozilla.VideoPosterHelper('#action');
    var $video = $('#encryption-video');

    // innovation section - aframe 3d demo
    var $aframeIframe;
    var $aframeShield; // sits over iframe to prevent scroll capture

    // test for matchMedia
    if ('matchMedia' in window) {
        mqIsTablet = matchMedia('(min-width: 760px)');
    }


    // Intro slideshow
    function startSlideshow() {
        $slideshow.cycle({
            fx: 'fade',
            log: false,
            slides: '> .slide',
            speed: 1000,
            startingSlide: 1, // start on group photo
            timeout: 5000
        });
    }


    // Encryption video
    // use poster value from <video>
    $('#encryption-video-container .moz-video-button').css({
        'background-image': 'url(' + $video.attr('poster') + ')'
    });

    encryptionVideoContainer.init();

    // track play and complete on video
    $video.on('play', function() {
        window.dataLayer.push({
            'event': 'video-interaction',
            'interaction': 'video - play',
            'videoTitle': 'home-encryption'
        });
    }).on('ended', function() {
        window.dataLayer.push({
            'event': 'video-interaction',
            'interaction': 'video - complete',
            'videoTitle': 'home-encryption'
        });
    });

    // Innovation section - aframe
    function isAframeSupported() {
        var canvas = document.createElement('canvas');
        var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        var glSupported = !!(gl && gl instanceof WebGLRenderingContext);
        var isIE11 = !!(navigator.userAgent.match(/Trident\/7\./));

        // IE 11 supports WebGL, but aframe still fails to load
        return glSupported && !isIE11;
    }

    if (isAframeSupported()) {
        $aframeIframe = $('<iframe>').attr({
            frameborder: 0,
            id: 'aframe-iframe',
            src: 'https://aframe.io/aframe/examples/animation-aframe-logo/?ui=false'
        });

        $aframeShield = $('<div>').attr('id', 'aframe-iframe-shield');

        $aframeIframe.on('load', function() {
            $(this).addClass('loaded');
        });

        // put the iframe under the shield
        $('#aframe-wrapper').append($aframeShield).append($aframeIframe);
    }

    function enableWaypoints() {
        // fire the waypoints for each section, passing classes for the current and previous sections
        actionWaypoint = new Waypoint({
            element: '#action',
            handler: navState('action', 'intro'),
            offset: '30%'
        });

        innovationWaypoint = new Waypoint({
            element: '#innovation',
            handler: navState('innovation', 'action'),
            offset: '30%'
        });

        firefoxWaypoint = new Waypoint({
            element: '#firefox',
            handler: navState('firefox', 'innovation'),
            offset: '30%'
        });
    }

    // Change the navbar current item to match the section waypoint
    function navState(current, previous) {
        return function(direction) {
            var $navPrimary;
            var gtmSection;

            // if user clicks a primary nav item, only perform logic below if
            // the clicked nav item matches the item currently being scrolled
            // into view. this prevents scroll tracking on items in-between the
            // currently visible item and the destination item.
            if (!suppressScrollTracking || (clickTargetSection === current || clickTargetSection === previous)) {
                // un-highlight all nav items
                $navPage.find('#nav-page-primary li').removeClass();

                // determine which nav item we will act upon based on scroll
                // direction
                if (direction === 'down') {
                    $navPrimary = $('#nav-primary-' + current);
                } else {
                    $navPrimary = $('#nav-primary-' + previous);
                }

                // will be undefined when scrolling up to #intro
                gtmSection = $navPrimary.find('a').data('link-name');

                if (gtmSection) {
                    // highlight the appropriate nav item
                    $navPrimary.addClass('current');

                    // remove ' anchor' text from data-link-name for scrolling event
                    gtmSection = gtmSection.replace(/ anchor/, '');

                    // track scrolling to sections
                    window.dataLayer.push({
                        'event': 'scroll-section',
                        'section': gtmSection
                    });
                }

                suppressScrollTracking = false;
                clickTargetSection = undefined;
            }
        };
    }

    // Scroll smoothly to the linked section
    $('#masthead').on('click', '#nav-page-primary a[href^="#"], .masthead-logo a[href^="#"]', function(e) {
        e.preventDefault();

        var $this = $(this);

        $this.blur();
        // Extract the target element's ID from the link's href.
        var $elem = $($this.attr('href').replace(/.*?(#.*)/g, '$1'));
        var offset = $elem.offset().top;

        // don't track scrolling to in-between sections
        suppressScrollTracking = true;
        clickTargetSection = $elem.prop('id');

        Mozilla.smoothScroll({
            top: offset
        });
    });

    // start up slideshow and waypoints for wide screens
    if (mqIsTablet) {
        if (mqIsTablet.matches) {
            startSlideshow();
            enableWaypoints();
        }

        mqIsTablet.addListener(function(mq) {
            if (mq.matches) {
                startSlideshow();
                enableWaypoints();
            } else {
                $slideshow.cycle('destroy');

                actionWaypoint.destroy();
                innovationWaypoint.destroy();
                firefoxWaypoint.destroy();
            }
        });
    // if browser doesn't support matchMedia, assume it's a wide enough screen
    // and start slideshow
    } else {
        startSlideshow();
    }
})(window.jQuery, window.Waypoint);
