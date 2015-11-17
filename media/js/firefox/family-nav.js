/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

;(function(Mozilla, $, Waypoint) {
    'use strict';

    Mozilla.FxFamilyNav = (function() {
        var mqDesktop;
        var fxFamillyNavSticky;

        // It's your world, IE
        if (typeof matchMedia !== 'undefined') {
            mqDesktop = matchMedia('(min-width: 760px)');
        }

        // entire fx family nav wrapper
        var $fxFamilyHeader = $('#fxfamilynav-header');

        // little ... button that triggers tertiary display
        var $tertiaryNavTrigger = $('#fxfamilynav-tertiarynav-trigger');

        // wrappers for tertiary nav
        var $tertiaryNavContainer = $('#fxfamilynav-tertiarynav');

        // all ul.tertiarynav elements
        var $tertiaryNavs = $fxFamilyHeader.find('.tertiarynav');

        // initialize the thing
        var _initMq = function() {
            mqDesktop.addListener(function(mq) {
                if (mq.matches) {
                    _enableDesktop();
                } else {
                    _disableDesktop();
                }
            });

            if (mqDesktop.matches) {
                _enableDesktop();
            }
        };

        // wire up all desktop interactions
        var _enableDesktop = function() {
            // toggle tertiary nav visibility
            $tertiaryNavTrigger.on('click', function() {
                $tertiaryNavTrigger.toggleClass('active');
                $tertiaryNavContainer.toggleClass('active');

                // track when opening menu

                if ($tertiaryNavTrigger.hasClass('active')) {
                    window.dataLayer.push({
                        'event': 'family-nav-interaction',
                        'location': 'Side Menu',
                        'browserAction': 'Open Menu'
                    });
                }
            }).addClass('visible');

            // hide/show tertiary nav
            $tertiaryNavContainer.on('mouseover', function() {
                $tertiaryNavContainer.addClass('active');
                $tertiaryNavTrigger.addClass('active');
            }).on('mouseout', function() {
                $tertiaryNavContainer.removeClass('active');
                $tertiaryNavTrigger.removeClass('active');
            });

            // make sure tertiary nav is hidden if mouse leaves nav area
            $fxFamilyHeader.on('mouseleave', function() {
                $tertiaryNavContainer.removeClass('active');
                $tertiaryNavTrigger.removeClass('active');
            });

            // ensure only browsers that support CSS transforms
            // get the sticky nav (matchMedia support overlap is
            // almost exact)
            if (mqDesktop) {
                fxFamillyNavSticky = new Waypoint.Sticky({
                    element: $fxFamilyHeader,
                    offset: -50
                });
            }
        };

        // remove all desktop interactions (mobile clean-up)
        var _disableDesktop = function() {
            $tertiaryNavContainer.removeClass('active');

            $tertiaryNavTrigger.off();
            $tertiaryNavContainer.off();
            $fxFamilyHeader.off();

            if (mqDesktop) {
                fxFamillyNavSticky.destroy();
            }
        };

        // public initialization point
        var _init = function() {
            // all external tertiary nav links open in new tab
            $tertiaryNavs.find('a[rel="external"]').attr('target', '_blank');

            // initialize matchMedia
            if (mqDesktop) {
                _initMq();
            } else {
                // if matchMedia not available, just wire up the desktop stuff
                _enableDesktop();

                // check if IE 8 and replace ... button
                if (/MSIE\s[1-8]\./.test(navigator.userAgent)) {
                    $('.trigger-dots').addClass('fallback');
                }
            }
        };

        $tertiaryNavs.on('click', 'a', function() {
            window.dataLayer.push({
                'event': 'family-nav-interaction',
                'browserAction': $(this).attr('data-ga')
            });
        });

        // public interface
        return {
            init: function() {
                _init();
            }
        };
    })();
})(window.Mozilla, window.jQuery, window.Waypoint);

Mozilla.FxFamilyNav.init();
