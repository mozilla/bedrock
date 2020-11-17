/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Copied from Protocol, to be backported along with nav updates.

(function(Mzp) {
    'use strict';

    var Navigation = {};
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
     * requirements for sticky behaviour?
     * @returns {Boolean}
     */
    Navigation.isLargeViewport = function() {
        return _mqLargeNav.matches;
    };

    /**
     * Feature detect for sticky navigation
     * @returns {Boolean}
     */
    Navigation.supportsSticky = function() {
        if (typeof Mzp.Supports !== 'undefined') {
            return Mzp.Supports.matchMedia &&
                   Mzp.Supports.classList &&
                   Mzp.Supports.requestAnimationFrame &&
                   Mzp.Supports.cssFeatureQueries &&
                   CSS.supports('position', 'sticky');
        } else {
            return false;
        }
    };

    /**
     * Scroll event listener. No computationally expensive
     * operations such as DOM modifications should happen
     * here. Instead we throttle using `requestAnimationFrame`.
     */
    Navigation.onScroll = function() {
        if (!_ticking) {
            _animationFrameID = window.requestAnimationFrame(Navigation.checkScrollPosition);
            _ticking = true;
        }
    };

    /**
     * Create sticky state for the navigation.
     */
    Navigation.createSticky = function() {
        _viewport.classList.add('mzp-has-sticky-navigation');
        _animationFrameID = window.requestAnimationFrame(Navigation.checkScrollPosition);
        window.addEventListener('scroll', Navigation.onScroll, false);
    };

    /**
     * Destroy sticky state for the navigation.
     */
    Navigation.destroySticky = function() {
        _viewport.classList.remove('mzp-has-sticky-navigation');
        _navElem.classList.remove('mzp-is-scrolling');
        _navElem.classList.remove('mzp-is-hidden');
        _lastKnownScrollPosition = 0;

        if (_animationFrameID) {
            window.cancelAnimationFrame(_animationFrameID);
        }
        window.removeEventListener('scroll', Navigation.onScroll, false);
    };

    /**
     * Initialize sticky state for the navigation.
     * Uses `matchMedia` to determine if conditions
     * for sticky navigation are satisfied.
     */
    Navigation.initSticky = function() {
        _mqLargeNav = matchMedia('(min-width: ' + _wideBreakpoint + ') and (min-height: ' + _tallBreakpoint + ')');

        _mqLargeNav.addListener(function(mq) {
            if (mq.matches) {
                Navigation.createSticky();
            } else {
                Navigation.destroySticky();
            }
        });

        if (Navigation.isLargeViewport()) {
            Navigation.createSticky();
        }
    };

    /**
     * Implements sticky navigation behaviour as
     * user scrolls up and down the viewport.
     */
    Navigation.checkScrollPosition = function() {
        // add tyling for when scrolling the viewport
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
                if (typeof Mzp.Menu !== 'undefined') {
                    Mzp.Menu.close();
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
    Navigation.onClick = function(e) {
        var thisNavItemList = e.target.parentNode.querySelector('.c-navigation-items');

        e.preventDefault();

        // Update button state
        e.target.classList.toggle('mzp-is-active');

        // Update menu state
        thisNavItemList.classList.toggle('mzp-is-open');

        // Update aria-expended state on menu.
        var expanded = thisNavItemList.classList.contains('mzp-is-open') ? true : false;
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
    Navigation.setAria = function() {
        for (var i = 0; i < _navItemsLists.length; i++) {
            _navItemsLists[i].setAttribute('aria-expanded', false);
        }
    };

    /**
     * Bind navigation event handlers.
     */
    Navigation.bindEvents = function() {
        _navItemsLists = document.querySelectorAll('.c-navigation-items');
        if (_navItemsLists.length > 0) {
            var navButtons = document.querySelectorAll('.c-navigation-menu-button');
            for (var i = 0; i < navButtons.length; i++) {
                navButtons[i].addEventListener('click', Navigation.onClick, false);
            }
            Navigation.setAria();
        }
    };

    /**
     * Initialise menu.
     * @param {Object} options - configurable options.
     */
    Navigation.init = function(options) {
        if (typeof options === 'object') {
            for (var i in options) {
                if (options.hasOwnProperty.call(i)) {
                    _options[i] = options[i];
                }
            }
        }

        Navigation.bindEvents();

        /**
         * Init (optional) sticky navigation.
         * If there are multiple navigation organisms on a single page,
         * assume only the first (and hence top-most) instance can and
         * will be sticky.
         */
        _navElem = document.querySelector('.c-navigation');

        if (_navElem && _navElem.classList.contains('mzp-is-sticky')) {
            if (Navigation.supportsSticky()) {
                Navigation.initSticky();
            }
        }
    };

    window.Mzp.Navigation = Navigation;

})(window.Mzp);
