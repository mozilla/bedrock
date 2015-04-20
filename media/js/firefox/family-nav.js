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

        // top level nav <li> elements (for handling hover)
        var $primaryLis = $('#fxfamilynav-primary > li');

        // just the <a> tags in the top level nav
        var $primaryLinks = $fxFamilyNav.find('.primary-link');

        // reference the currently active primary <li>
        var $activePrimaryLi;

        // little ... button that triggers tertiary display
        var $tertiaryNavTrigger = $('#fxfamilynav-tertiarynav-trigger');

        // wrappers for tertiary nav
        var $tertiaryNavContainer = $('#fxfamilynav-tertiarynav');

        // all ul.subnav elements
        var $subNavs = $fxFamilyNav.find('.subnav');

        // all ul.tertiarynav elements
        var $tertiaryNavs = $fxFamilyHeader.find('.tertiarynav');

        // used to revert subnav after hovering off non-selected primary link
        var currentNavId;

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

        var _setTertiaryNav = function() {
            $tertiaryNavs.each(function() {
                var $this = $(this);

                if ($this.data('parent') === currentNavId) {
                    $this.addClass('active');
                    return false;
                }
            });

            // all external tertiary nav links open in new tab
            $tertiaryNavs.find('a[rel="external"]').attr('target', '_blank');
        };

        // wire up all desktop interactions
        var _enableDesktop = function() {
            // hide '.active' primary <li> when hovering/focusing other sibling <li>'s
            $primaryLis.on('mouseenter', function() {
                // if tabbing to a link, then mousing over another, must blur tabbed to link
                // to prevent text overlap
                $primaryLinks.blur();

                // hide the default active subnav
                $activePrimaryLi.removeClass('active');

                // show the hovered over subnav
                $(this).find('.subnav').addClass('active');
            }).on('mouseleave', function() {
                // hide any focus/hover activated subnavs
                $subNavs.removeClass('active');

                // show the default subnav
                $activePrimaryLi.addClass('active');
            });

            $primaryLinks.on('focus', function() {
                // hide any focus/hover activated subnavs
                $subNavs.removeClass('active');

                // hide the default subnav
                $activePrimaryLi.removeClass('active');

                // show the related subnav
                $(this).siblings('.subnav:first').addClass('active');
            }).on('blur', function() {
                // hide any focus/hover activated subnavs
                $subNavs.removeClass('active');

                // show the default active subnav
                $activePrimaryLi.addClass('active');
            });

            // toggle tertiary nav visibility
            $tertiaryNavTrigger.on('click', function() {
                $tertiaryNavTrigger.toggleClass('active');
                $tertiaryNavContainer.toggleClass('active');

                // track when opening menu
                if ($tertiaryNavTrigger.hasClass('active')) {
                    window.gaTrack(['_trackEvent', 'Fx Family Nav Interactions', 'Side Menu', 'Open Menu']);
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
                $fxFamilyHeader.waypoint('sticky', {
                    offset: -80
                });
            }
        };

        // remove all desktop interactions (mobile clean-up)
        var _disableDesktop = function() {
            $tertiaryNavContainer.removeClass('active');

            $primaryLis.off();
            $primaryLinks.off();
            $tertiaryNavTrigger.off();
            $tertiaryNavContainer.off();
            $fxFamilyHeader.off();

            if (mqDesktop) {
                $fxFamilyHeader.waypoint('unsticky');
            }
        };

        // public initialization point, called from page specific script
        var _init = function(config) {
            // default to desktop
            var primaryId = config.primaryId || 'desktop';

            // default to overview
            var subId = config.subId || '';

            // store selected nav id for use when hovering off other navs
            currentNavId = primaryId;

            // select primary nav (always)
            $('a[data-id="' + primaryId + '"]').addClass('selected').closest('li').addClass('active');
            $activePrimaryLi = $('a[data-id="' + primaryId + '"]').closest('li');
            $activePrimaryLi.addClass('active');

            // if subnav id was sent, select it
            if (subId) {
                // set subsubnav
                if ($.inArray(subId, ['index', 'trust', 'customize', 'fast']) > -1) {
                    $('#desktop-subsubnav').addClass('active');
                }

                $('a[data-id="' + primaryId + '-' + subId + '"]').addClass('selected');
            }

            _setTertiaryNav();

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

            _initGA();
        };

        // analytics
        var _initGA = function() {
            // clicks on top level nav links
            $primaryLinks.on('click', function(e) {
                var $this = $(this);

                if (e.metaKey || e.ctrlKey) {
                    window.gaTrack(['_trackEvent', 'Fx Family Nav Interactions', $this.data('id'), $this.data('id') + ' - top nav link']);
                } else {
                    e.preventDefault();
                    window.gaTrack(['_trackEvent', 'Fx Family Nav Interactions', $this.data('id'), $this.data('id') + ' - top nav link'], function() {
                        window.location = $this.attr('href');
                    });
                }
            });

            // clicks on subnav links
            $subNavs.on('click', 'a', function(e) {
                var $this = $(this);

                var parentName = $this.data('id').split('-');

                var trackName = ($fxFamilyHeader.hasClass('stuck')) ? parentName[0] + ' - Persistent Nav' : parentName[0];

                if (e.metaKey || e.ctrlKey) {
                    window.gaTrack(['_trackEvent', 'Fx Family Nav Interactions', trackName, parentName[1]]);
                } else {
                    e.preventDefault();
                    window.gaTrack(['_trackEvent', 'Fx Family Nav Interactions', trackName, parentName[1]], function() {
                        window.location = $this.attr('href');
                    });
                }
            });

            // clicks on tertiary nav links
            $tertiaryNavs.on('click', 'a', function(e) {
                var $this = $(this);

                if (e.metaKey || e.ctrlKey || $this.attr('rel') === 'external') {
                    window.gaTrack(['_trackEvent', 'Fx Family Nav Interactions', 'Side Menu', $this.data('ga')]);
                } else {
                    e.preventDefault();
                    window.gaTrack(['_trackEvent', 'Fx Family Nav Interactions', 'Side Menu', $this.data('ga')], function() {
                        window.location = $this.attr('href');
                    });
                }
            });
        };

        // public interface
        return {
            // @config (object):
            //      primaryId (string): ID of primary nav link
            //      subId (string): ID of sub nav link, dependent upon primary
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
