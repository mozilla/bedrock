/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

;(function(Mozilla, $) {
    'use strict';

    Mozilla.FxFamilyNav = (function() {
        var mqDesktop;

        // It's your world, IE
        if (typeof matchMedia !== 'undefined') {
            mqDesktop = matchMedia('(min-width: 760px)');
        }

        // entire fx family nav wrapper
        var $fxFamilyHeader = $('#fxfamilynav-header');

        // just the <nav> - primary, sub, and tertiary navs
        var $fxFamilyNav = $('#fxfamilynav');

        // just the <a> tags in the top level nav
        var $primaryLinks = $fxFamilyNav.find('.primary-link');

        // little ... button that triggers tertiary display
        var $tertiaryNavTrigger = $('#fxfamilynav-tertiarynav-trigger');

        // wrappers for sub/tertiary navs
        var $subNavContainer = $('#fxfamilynav-subnav');
        var $tertiaryNavContainer = $('#fxfamilynav-tertiarynav');

        // all ul.subnav elements
        var $subNavs = $fxFamilyNav.find('.subnav');

        // all ul.tertiarynav elements
        var $tertiaryNavs = $fxFamilyNav.find('.tertiarynav');

        // used to revert subnav after hovering off non-selected primary link
        var currentNavId;
        var currentSubNavId;

        // CTA wrapper
        var $ctaWrapper = $('#fxfamilynav-cta-wrapper');

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

        // shows related subnav when hovering over primary nav link
        var _displaySubNav = function(subNavId) {
            // remember to revert subnav on mouseout
            currentSubNavId = subNavId;

            $subNavContainer.animate({ opacity: 0 }, 200, function() {
                // hide all subnavs
                $subNavs.removeClass('active');

                // show the correct subnav
                $subNavContainer.find('.subnav[data-parent="' + subNavId + '"]').addClass('active');

                // re-display subnav container
                $subNavContainer.animate({ opacity: 1 }, 200);
            });
        };

        var _setTertiaryNav = function() {
            $tertiaryNavs.each(function() {
                var $this = $(this);

                if ($this.data('parent') === currentNavId) {
                    $this.addClass('active');
                    return false;
                }
            });
        };

        // wire up all desktop interactions
        var _enableDesktop = function() {
            $subNavContainer.removeClass('hidden');

            $primaryLinks.on('mouseover focus', function() {
                var $this = $(this);
                var thisId = $this.data('id');

                // if not hovering over currently active primary nav link, change subnav
                if (currentSubNavId !== thisId) {
                    _displaySubNav(thisId);
                }
            });

            // revert subnav to default when mouseleaving nav area
            $fxFamilyNav.on('mouseleave blur', function() {
                if (currentSubNavId !== currentNavId) {
                    _displaySubNav(currentNavId);
                }
            });

            // toggle tertiary nav visibility
            $tertiaryNavTrigger.on('click', function() {
                $tertiaryNavTrigger.toggleClass('active');
                $tertiaryNavContainer.toggleClass('active');
            }).addClass('visible');

            $tertiaryNavContainer.on('mouseover', function() {
                $tertiaryNavContainer.addClass('active');
                $tertiaryNavTrigger.addClass('active');
            }).on('mouseout', function() {
                $tertiaryNavContainer.removeClass('active');
                $tertiaryNavTrigger.removeClass('active');
            });

            $fxFamilyHeader.on('mouseleave', function() {
                $tertiaryNavContainer.removeClass('active');
                $tertiaryNavTrigger.removeClass('active');
            });

            $fxFamilyHeader.waypoint('sticky', {
                offset: -120
            });
        };

        // remove all desktop interactions (mobile clean-up)
        var _disableDesktop = function() {
            $subNavContainer.addClass('hidden');
            $tertiaryNavContainer.removeClass('active');

            $primaryLinks.off();
            $fxFamilyNav.off();
            $tertiaryNavTrigger.off();
            $tertiaryNavContainer.off();
            $fxFamilyHeader.off();

            $fxFamilyHeader.waypoint('unsticky');
        };

        // public initialization point, called from page specific script
        var _init = function(config) {
            // default to desktop
            var primaryId = config.primaryId || 'desktop';

            // default to overview
            var subId = config.subId || 'overview';

            // does page provide a CTA for sticky nav?
            var ctaId = config.ctaId || null;

            // store selected nav id for use when hovering off other navs
            currentNavId = currentSubNavId = primaryId;

            // select primary nav (always)
            $primaryLinks.each(function() {
                var $this = $(this);

                if ($this.data('id') === primaryId) {
                    $this.addClass('selected');
                    return false;
                }
            });

            // if subnav id was sent, select it
            if (subId) {
                $('a[data-id="' + primaryId + '-' + subId + '"]').addClass('selected');
            }

            // set the associated sub & tertiary navs
            _displaySubNav(primaryId);
            _setTertiaryNav();

            if (ctaId) {
                _setCTA(ctaId);
            }

            // initialize matchMedia
            if (mqDesktop) {
                _initMq();
            } else {
                // if matchMedia not available, just wire up the desktop stuff
                _enableDesktop();
            }
        };

        // pulls element with ctaId into container within nav
        // retains all event listeners
        var _setCTA = function(ctaId) {
            $ctaWrapper.append($('#' + ctaId));
        };

        // public interface
        return {
            // @config (object):
            //      primaryId (string): ID of primary nav link
            //      subId (string): ID of sub nav link, dependent upon primary
            //      ctaId (string): ID of CTA on implementing page to be pulled into sticky nav
            //                      element will be moved entirely (not duplicated)
            //
            //      Available nav IDs:
            //      desktop
            //          - index
            //          - trust
            //          - customize
            //          - fast
            //      android
            //          - index
            //      os
            //          - index
            //          - devices
            //          - partners
            //          - mwc
            init: function(config) {
                _init(config);
            }
        };
    })();
})(window.Mozilla, window.jQuery);
