/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Waypoint) {
    'use strict';

    // Lazyload images
    Mozilla.LazyLoad.init();

    /*
    * Sticky CTA
    */
    var $stickyCTA = $(document.querySelectorAll('.c-sticky-cta'));
    var hasCookies = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();
    $stickyCTA.attr('aria-hidden', 'true');

    // init dismiss button
    function initStickyCTA() {
        // add and remove aria-hidden
        var primaryTop = new Waypoint({
            element: document.querySelectorAll('.c-primary-cta'),
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

        // hide sticky at top to prevent revealing through overscroll
        var $stickyWrapper = $stickyCTA.find('.c-sticky-cta-wrapper');
        $stickyWrapper.hide();
        var mozContent = new Waypoint({
            element: document.querySelectorAll('.mozilla-content'),
            handler: function(direction) {
                if(direction === 'down') {
                    // reveal sticky
                    $stickyWrapper.show();
                } else {
                    // hide sticky
                    $stickyWrapper.hide();
                }
            },
            offset: 100
        });

        // add button
        var $dismissButton = $('<button type="button" class="sticky-dismiss">').text('Dismiss this prompt.');
        $dismissButton.appendTo($stickyWrapper);

        // find all the buttons
        var dismissButtons = $('.sticky-dismiss');
        // listen for the click
        dismissButtons.on('click', function() {
            // destroy waypoints
            primaryTop.destroy();
            mozContent.destroy();

            // dismiss the sticky banner
            dismissStickyCTA();
        });
    }

    // handle dismiss
    function dismissStickyCTA() {
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
