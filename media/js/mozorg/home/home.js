/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Waypoint) {
    'use strict';

    var mozClient = window.Mozilla.Client;
    var impactInnovationWaypoint;
    var $slideshow = $('#home-slideshow');

    function handleWaypoint(target, callback) {
        return function(direction) {
            window.dataLayer.push({
                'event': 'scroll-section',
                'section': target
            });

            if (typeof callback === 'function') {
                callback(direction);
            }
        };
    }

    // Intro slideshow
    function startSlideshow() {
        if ($slideshow.length) {
            $slideshow.cycle({
                fx: 'fade',
                log: false,
                slides: '> .slide',
                speed: 1000,
                startingSlide: 1, // start on group photo
                timeout: 5000
            });
        }
    }

    function enableWaypoints() {
        impactInnovationWaypoint = new Waypoint({
            element: '#impact-innovate-wrapper',
            handler: handleWaypoint('impact-innovation'),
            offset: '40%'
        });
    }

    // show mobile download buttons if on mobile platform and not fx
    if (mozClient.isMobile && !mozClient.isFirefox) {
        $('#fxmobile-download-buttons').addClass('visible');
        $('#fx-download-link').addClass('hidden');

        if (window.site.platform === 'android') {
            $('.android-systems-link').removeClass('hidden');
        }
    }

    $(function() {
        var mqIsTablet;

        // test for matchMedia
        if ('matchMedia' in window) {
            mqIsTablet = matchMedia('(min-width: 760px)');
        }

        if (mqIsTablet) {
            if (mqIsTablet.matches) {
                enableWaypoints();
                startSlideshow();
            }

            mqIsTablet.addListener(function(mq) {
                if (mq.matches) {
                    enableWaypoints();
                    startSlideshow();
                } else {
                    if ($slideshow.length) {
                        $slideshow.cycle('destroy');
                    }

                    impactInnovationWaypoint.destroy();
                }
            });
        // if browser doesn't support matchMedia, assume it's a wide enough
        // screen and start slideshow
        } else {
            startSlideshow();
        }
    });
})(window.jQuery, window.Waypoint);
