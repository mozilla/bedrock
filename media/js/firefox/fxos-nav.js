/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function(Mozilla, $, Waypoint) {
    'use strict';

    Mozilla.FxOsNav = (function() {
        var mqDesktop;
        var fxOsNavSticky;

        // It's your world, IE
        if (typeof matchMedia !== 'undefined') {
            mqDesktop = matchMedia('(min-width: 760px)');
        }

        // entire fxos nav wrapper
        var $fxOsHeader = $('#fxosnav-header');

        // little ... button that triggers adjunct nav display
        var $adjunctNavTrigger = $('#fxosnav-adjunctnav-trigger');

        // wrappers for adjunct nav
        var $adjunctNavContainer = $('#fxosnav-adjunctnav');

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
            // toggle adjunct nav visibility
            $adjunctNavTrigger.on('click', function() {
                $adjunctNavTrigger.toggleClass('active');
                $adjunctNavContainer.toggleClass('active');

                // track when opening menu

                if ($adjunctNavTrigger.hasClass('active')) {
                    window.dataLayer.push({
                        'event': 'open-side-menu'
                    });
                }
            }).addClass('visible');

            // hide/show adjunct nav
            $adjunctNavContainer.on('mouseover', function() {
                $adjunctNavContainer.addClass('active');
                $adjunctNavTrigger.addClass('active');
            }).on('mouseout', function() {
                $adjunctNavContainer.removeClass('active');
                $adjunctNavTrigger.removeClass('active');
            });

            // make sure adjunct nav is hidden if mouse leaves nav area
            $fxOsHeader.on('mouseleave', function() {
                $adjunctNavContainer.removeClass('active');
                $adjunctNavTrigger.removeClass('active');
            });

            // ensure only browsers that support CSS transforms
            // get the sticky nav (matchMedia support overlap is
            // almost exact)
            if (mqDesktop) {
                fxOsNavSticky = new Waypoint.Sticky({
                    element: $fxOsHeader,
                    offset: -50
                });
            }
        };

        // remove all desktop interactions (mobile clean-up)
        var _disableDesktop = function() {
            $adjunctNavContainer.removeClass('active');

            $adjunctNavTrigger.off();
            $adjunctNavContainer.off();
            $fxOsHeader.off();

            if (mqDesktop) {
                fxOsNavSticky.destroy();
            }
        };

        // public initialization point
        var _init = function() {
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

        // public interface
        return {
            init: function() {
                _init();
            }
        };
    })();
})(window.Mozilla, window.jQuery, window.Waypoint);

Mozilla.FxOsNav.init();
