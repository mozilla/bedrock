/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { trapKeyboardFocus } from './m24-keyboard-focus-trap.es6';

const MzpNavigation = {};
let _navElem;
let _navItemsLists;
let _navMenuButtons;
const _options = {
    onNavOpen: null,
    onNavClose: null
};
let _ticking = false;
let _lastKnownScrollPosition = 0;
let _animationFrameID = null;
const _stickyScrollOffset = 300;
const _wideBreakpoint = '768px';
const _tallBreakpoint = '600px';
let _mqLargeNav;
const _viewport = document.getElementsByTagName('html')[0];
let _navigationKeyboardFocusTrapCleanUp = null;

// MzpNavigation focusable element class list
const _defaultFocusList =
    '.m24-c-navigation-logo-link, .m24-c-navigation-menu-button, .m24-c-menu-title';
let _focusList = _defaultFocusList;

/**
 * set class list for focusable elements
 * @param {String} list - class list to determine focusable elements.
 */
MzpNavigation.setFocusList = (list) => {
    _focusList = list;
};

/**
 * reset class list for focusable elements as the default one
 */
MzpNavigation.resetFocusListFunction = () => {
    _focusList = _defaultFocusList;
};

/**
 * Does the viewport meet the minimum width and height
 * requirements for sticky behavior?
 * @returns {Boolean}
 */
MzpNavigation.isLargeViewport = () => {
    return _mqLargeNav.matches;
};

/**
 * Feature detect for sticky navigation
 * @returns {Boolean}
 */
MzpNavigation.supportsSticky = () => {
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
MzpNavigation.onScroll = () => {
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
MzpNavigation.createSticky = () => {
    _viewport.classList.add('mzp-has-sticky-navigation');
    _animationFrameID = window.requestAnimationFrame(
        MzpNavigation.checkScrollPosition
    );
    window.addEventListener('scroll', MzpNavigation.onScroll, false);
};

/**
 * Destroy sticky state for the navigation.
 */
MzpNavigation.destroySticky = () => {
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
MzpNavigation.initSticky = () => {
    _mqLargeNav = matchMedia(
        `(min-width: ${_wideBreakpoint}) and (min-height: ${_tallBreakpoint})`
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
MzpNavigation.checkScrollPosition = () => {
    // add styling for when scrolling the viewport and nav is already sticking
    if (window.scrollY > 0 && _navElem.getBoundingClientRect().top < 1) {
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
MzpNavigation.onClick = (e) => {
    const thisNavItemList = e.target.parentNode.querySelector(
        '.m24-c-navigation-items'
    );

    e.preventDefault();

    // Update button state
    e.target.classList.toggle('mzp-is-active');

    // Update menu state
    thisNavItemList.classList.toggle('mzp-is-open');

    // Update aria-expended state on menu.
    const expanded = thisNavItemList.classList.contains('mzp-is-open')
        ? true
        : false;
    e.target.setAttribute('aria-expanded', expanded);

    if (expanded) {
        if (typeof _options.onNavOpen === 'function') {
            _options.onNavOpen(thisNavItemList);
        }

        // trap keyboard navigation focus for MzpNavigation
        _navigationKeyboardFocusTrapCleanUp = trapKeyboardFocus(
            () => !MzpNavigation.isLargeViewport(),
            document.querySelector('.m24-navigation-refresh'),
            () => _focusList
        );
    } else {
        if (typeof _options.onNavClose === 'function') {
            _options.onNavClose(thisNavItemList);
        }

        if (_navigationKeyboardFocusTrapCleanUp !== null) {
            _navigationKeyboardFocusTrapCleanUp();
            _navigationKeyboardFocusTrapCleanUp = null;
        }
    }
};

/**
 * use Intersection Observer API to keep track of when the mobile
 * nav menu is displayed to handle aria roles better
 */
MzpNavigation.menuButtonVisible = (callback) => {
    // check if Intersection observer is supported
    if (
        typeof window.MzpSupports !== 'undefined' &&
        window.MzpSupports.intersectionObserver
    ) {
        const observer = new IntersectionObserver(
            (entries) => {
                for (let index = 0; index < entries.length; index++) {
                    const entry = entries[index];
                    callback(entry.intersectionRatio > 0, entry.target);
                }
            },
            { root: document.documentElement }
        );
        for (let index = 0; index < _navMenuButtons.length; index++) {
            const button = _navMenuButtons[index];
            observer.observe(button);
        }
    }
};

/**
 * Set initial ARIA navigation states.
 */
MzpNavigation.setAria = () => {
    if (
        typeof window.MzpSupports !== 'undefined' &&
        window.MzpSupports.intersectionObserver
    ) {
        MzpNavigation.menuButtonVisible((isVisible, menuButton) => {
            if (isVisible) {
                // if the menu button is visible -  set the 'aria-expanded' role based on whether the menu is open or not
                const isActive =
                    !!menuButton.classList.contains('mzp-is-active');
                menuButton.setAttribute('aria-expanded', isActive);
            } else {
                // if the menu is not visible - remove the aria role, since elements
                // with `display: none` are not read to screen readers
                menuButton.removeAttribute('aria-expanded');
            }
        });
    } else {
        for (let index = 0; index < _navMenuButtons.length; index++) {
            const menuButton = _navMenuButtons[index];
            const isActive =
                menuButton.classList.contains('mzp-is-active') &&
                getComputedStyle(menuButton).display !== 'none';
            menuButton.setAttribute('aria-expanded', isActive);
        }
    }
};

/**
 * Bind navigation event handlers.
 */
MzpNavigation.bindEvents = () => {
    _navItemsLists = document.querySelectorAll('.m24-c-navigation-items');
    if (_navItemsLists.length > 0) {
        _navMenuButtons = document.querySelectorAll(
            '.m24-c-navigation-menu-button'
        );
        for (let index = 0; index < _navMenuButtons.length; index++) {
            const menuButton = _navMenuButtons[index];
            menuButton.addEventListener('click', MzpNavigation.onClick, false);
        }
        MzpNavigation.setAria();
    }
};

/**
 * Initialize menu.
 * @param {Object} options - configurable options.
 */
MzpNavigation.init = (options) => {
    if (typeof options === 'object') {
        for (const i in options) {
            if (Object.prototype.hasOwnProperty.call(options, i)) {
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

    _navElem = document.querySelector('.enable-main-nav-sticky');
    const _navIsSticky =
        _navElem &&
        _navElem.classList.contains('m24-mzp-is-sticky') &&
        MzpNavigation.supportsSticky();

    if (_navIsSticky && matchMedia('(prefers-reduced-motion)').matches) {
        _navElem.classList.remove('m24-mzp-is-sticky');
    } else if (_navIsSticky) {
        MzpNavigation.initSticky();
    }
};

export default MzpNavigation;
