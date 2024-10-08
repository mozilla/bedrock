/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Copied from Protocol, to be back-ported along with nav updates.

(function () {
    'use strict';

    var MzpNavigation = {};
    var _navElem;
    var _navItemsLists;
    var _options = {
        onNavOpen: null,
        onNavClose: null
    };
    var _ticking = false;
    var _lastKnownScrollPosition = 0;
    var _animationFrameID = null;
    var _stickyScrollOffset = 300;
    var _wideBreakpoint = '768px';
    var _tallBreakpoint = '600px';
    var _mqLargeNav;
    var _viewport = document.getElementsByTagName('html')[0];

    /**
     * Does the viewport meet the minimum width and height
     * requirements for sticky behavior?
     * @returns {Boolean}
     */
    MzpNavigation.isLargeViewport = function () {
        return _mqLargeNav.matches;
    };

    /**
     * Feature detect for sticky navigation
     * @returns {Boolean}
     */
    MzpNavigation.supportsSticky = function () {
        if (typeof window.MzpSupports !== 'undefined') {
            return (
                window.MzpSupports.matchMedia &&
                window.MzpSupports.classList &&
                window.MzpSupports.requestAnimationFrame &&
                window.MzpSupports.cssFeatureQueries &&
                CSS.supports('position', 'sticky')
            );
        } else {
            return false;
        }
    };

    /**
     * Scroll event listener. No computationally expensive
     * operations such as DOM modifications should happen
     * here. Instead we throttle using `requestAnimationFrame`.
     */
    MzpNavigation.onScroll = function () {
        if (!_ticking) {
            _animationFrameID = window.requestAnimationFrame(
                MzpNavigation.checkScrollPosition
            );
            _ticking = true;
        }
    };

    /**
     * Create sticky state for the navigation.
     */
    MzpNavigation.createSticky = function () {
        _viewport.classList.add('mzp-has-sticky-navigation');
        _animationFrameID = window.requestAnimationFrame(
            MzpNavigation.checkScrollPosition
        );
        window.addEventListener('scroll', MzpNavigation.onScroll, false);
    };

    /**
     * Destroy sticky state for the navigation.
     */
    MzpNavigation.destroySticky = function () {
        _viewport.classList.remove('mzp-has-sticky-navigation');
        _navElem.classList.remove('mzp-is-scrolling');
        _navElem.classList.remove('mzp-is-hidden');
        _lastKnownScrollPosition = 0;

        if (_animationFrameID) {
            window.cancelAnimationFrame(_animationFrameID);
        }
        window.removeEventListener('scroll', MzpNavigation.onScroll, false);
    };

    /**
     * Initialize sticky state for the navigation.
     * Uses `matchMedia` to determine if conditions
     * for sticky navigation are satisfied.
     */
    MzpNavigation.initSticky = function () {
        _mqLargeNav = matchMedia(
            '(min-width: ' +
                _wideBreakpoint +
                ') and (min-height: ' +
                _tallBreakpoint +
                ')'
        );

        function makeStickyNav(mq) {
            if (mq.matches) {
                MzpNavigation.createSticky();
            } else {
                MzpNavigation.destroySticky();
            }
        }

        if (window.matchMedia('all').addEventListener) {
            _mqLargeNav.addEventListener('change', makeStickyNav, false);
        } else if (window.matchMedia('all').addListener) {
            _mqLargeNav.addListener(makeStickyNav);
        }

        if (MzpNavigation.isLargeViewport()) {
            MzpNavigation.createSticky();
        }
    };

    /**
     * Implements sticky navigation behavior as
     * user scrolls up and down the viewport.
     */
    MzpNavigation.checkScrollPosition = function () {
        // add styling for when scrolling the viewport
        if (window.scrollY > 0) {
            _navElem.classList.add('mzp-is-scrolling');
        } else {
            _navElem.classList.remove('mzp-is-scrolling');
        }

        // scrolling down
        if (window.scrollY > _lastKnownScrollPosition) {
            // hide the sticky nav shortly after scrolling down the viewport.
            if (window.scrollY > _stickyScrollOffset) {
                // if there's a menu currently open, close it.
                if (typeof window.MzpMenu !== 'undefined') {
                    window.MzpMenu.close();
                }

                _navElem.classList.add('mzp-is-hidden');
            }
        }
        // scrolling up
        else {
            _navElem.classList.remove('mzp-is-hidden');
        }

        _lastKnownScrollPosition = window.scrollY;
        _ticking = false;
    };

    /**
     * Event handler for navigation menu button `click` events.
     */
    MzpNavigation.onClick = function (e) {
        var thisNavItemList = e.target.parentNode.querySelector(
            '.m24-c-navigation-items'
        );

        e.preventDefault();

        // Update button state
        e.target.classList.toggle('mzp-is-active');

        // Update menu state
        thisNavItemList.classList.toggle('mzp-is-open');

        // Update aria-expended state on menu.
        var expanded = thisNavItemList.classList.contains('mzp-is-open')
            ? true
            : false;
        thisNavItemList.setAttribute('aria-expanded', expanded);

        if (expanded) {
            if (typeof _options.onNavOpen === 'function') {
                _options.onNavOpen(thisNavItemList);
            }
        } else {
            if (typeof _options.onNavClose === 'function') {
                _options.onNavClose(thisNavItemList);
            }
        }
    };

    /**
     * Set initial ARIA navigation states.
     */
    MzpNavigation.setAria = function () {
        for (var i = 0; i < _navItemsLists.length; i++) {
            _navItemsLists[i].setAttribute('aria-expanded', false);
        }
    };

    /**
     * Bind navigation event handlers.
     */
    MzpNavigation.bindEvents = function () {
        _navItemsLists = document.querySelectorAll('.m24-c-navigation-items');
        if (_navItemsLists.length > 0) {
            var navButtons = document.querySelectorAll(
                '.m24-c-navigation-menu-button'
            );
            for (var i = 0; i < navButtons.length; i++) {
                navButtons[i].addEventListener(
                    'click',
                    MzpNavigation.onClick,
                    false
                );
            }
            MzpNavigation.setAria();
        }
    };

    /**
     * Initialize menu.
     * @param {Object} options - configurable options.
     */
    MzpNavigation.init = function (options) {
        if (typeof options === 'object') {
            for (var i in options) {
                if (options.hasOwnProperty.call(i)) {
                    _options[i] = options[i];
                }
            }
        }

        MzpNavigation.bindEvents();

        /**
         * Init (optional) sticky navigation.
         * If there are multiple navigation organisms on a single page,
         * assume only the first (and hence top-most) instance can and
         * will be sticky.
         *
         * Do not init sticky navigation if user prefers reduced motion
         */

        _navElem = document.querySelector('.m24-navigation-refresh');
        var _navIsSticky =
            _navElem &&
            _navElem.classList.contains('m24-mzp-is-sticky') &&
            MzpNavigation.supportsSticky();

        if (_navIsSticky && matchMedia('(prefers-reduced-motion)').matches) {
            _navElem.classList.remove('m24-mzp-is-sticky');
        } else if (_navIsSticky) {
            MzpNavigation.initSticky();
        }
    };

    window.MzpNavigation = MzpNavigation;
})(window.Mzp);
