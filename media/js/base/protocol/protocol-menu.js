/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Copied from Protocol, to be backported along with nav updates.

(function(Mzp) {
    'use strict';

    var Menu = {};
    var _menuOpen = false;
    var _hoverTimeout;
    var _hoverTimeoutDelay = 150;
    var _mqWideNav;
    var _wideBreakpoint = '768px';

    var _options = {
        onMenuOpen: null,
        onMenuClose: null,
        onMenuButtonClose: null
    };

    /**
     * Opens a menu panel.
     * @param {Object} el - DOM element (`.mzp-c-menu-category.mzp-js-expandable`)
     * @param {Boolean} animate - show animation when menu panel opens.
     */
    Menu.open = function(el, animate) {
        if (animate) {
            el.classList.add('mzp-is-animated');
        }

        el.classList.add('mzp-is-selected');

        _menuOpen = true; // For checking menu state on keyup.

        el.querySelector('.c-menu-title').setAttribute('aria-expanded', true);

        if (typeof _options.onMenuOpen === 'function') {
            _options.onMenuOpen(el);
        }
    };

    /**
     * Closes all currently open menu panels.
     * Note: on small screens more than one menu can be open at the same time.
     */
    Menu.close = function() {
        var current = document.querySelectorAll('.c-menu-category.mzp-is-selected');

        for (var i = 0; i < current.length; i++) {
            // The following classes must be removed in the correct order
            // to work around a bug in bedrock's classList polyfill for IE9.
            // https://github.com/mozilla/bedrock/issues/6221 :/
            current[i].classList.remove('mzp-is-selected');
            current[i].classList.remove('mzp-is-animated');

            current[i].querySelector('.c-menu-title').setAttribute('aria-expanded', false);
        }

        _menuOpen = false; // For checking menu state on keyup.

        if (typeof _options.onMenuClose === 'function' && current.length > 0) {
            _options.onMenuClose();
        }

        return current.length > 0;
    };

    Menu.onDocumentKeyUp = function(e) {
        if (e.keyCode === 27 && _menuOpen) {
            Menu.close();
        }
    };

    /**
     * Menu panel close button `click` event handler.
     * @param {Object} e - Event object.
     */
    Menu.onCloseButtonClick = function(e) {
        e.preventDefault();

        if (typeof _options.onMenuButtonClose === 'function') {
            _options.onMenuButtonClose();
        }

        Menu.close();
    };

    /**
     * Toggles the open/closed state of a menu panel.
     * @param {Object} el - DOM element (`.mzp-c-menu-category.mzp-js-expandable`)
     */
    Menu.toggle = function(el) {
        var state = el.classList.contains('mzp-is-selected') ? true : false;

        if (!state) {
            Menu.open(el);
        } else {
            // The following classes must be removed in the correct order
            // to work around a bug in bedrock's classList polyfill for IE9.
            // https://github.com/mozilla/bedrock/issues/6221 :/
            el.classList.remove('mzp-is-selected');
            el.classList.remove('mzp-is-animated');
            el.querySelector('.c-menu-title').setAttribute('aria-expanded', false);

            if (typeof _options.onMenuClose === 'function') {
                _options.onMenuClose();
            }
        }
    };

    /**
     * Menu `mouseenter` event handler.
     * Opens the menu only when hover intent is shown.
     * Animates only if a menu panel is not already open.
     * @param {Object} e - Event object.
     */
    Menu.onMouseEnter = function(e) {
        clearTimeout(_hoverTimeout);

        _hoverTimeout = setTimeout(function() {
            var current = Menu.close();
            var animate = current ? false: true;

            Menu.open(e.target, animate);
        }, _hoverTimeoutDelay);
    };

    /**
     * Menu `mouseleave` event handler.
     * Closes the menu only when hover intent is shown.
     */
    Menu.onMouseLeave = function() {
        clearTimeout(_hoverTimeout);

        _hoverTimeout = setTimeout(function() {
            Menu.close();
        }, _hoverTimeoutDelay);
    };

    /**
     * Menu `focusout` event handler.
     * Closes the menu when focus moves to an alement outside of the currently open panel.
     */
    Menu.onFocusOut = function() {
        var self = this;

        /**
         * After an element loses focus, `document.activeElement` will always be `body` before
         * moving to the next element. A `setTimeout` of `0` circumvents this issue as it
         * re-queues the JavaScript to run at the end of the current excecution.
         */
        setTimeout(function() {
            // If the menu is open and the newly focused element is not a child, then call close().
            if (!self.contains(document.activeElement) && self.classList.contains('mzp-is-selected')) {
                Menu.close();
            }
        }, 0);
    };

    /**
     * Menu link `click` event handler for wide viewports.
     * Closes any currently open menu panels before opening the selected one.
     * @param {Object} e - Event object.
     */
    Menu.onClickWide = function(e) {
        e.preventDefault();
        Menu.close();
        Menu.open(e.target.parentNode);
    };

    /**
     * Menu link `click` event handler for small viewports.
     * Toggles the currently selected menu open open/close state.
     * @param {Object} e - Event object.
     */
    Menu.onClickSmall = function(e) {
        e.preventDefault();
        Menu.toggle(e.target.parentNode);
    };

    /**
     * Convenience function for checking `matchMedia` state.
     * @return {Boolean}
     */
    Menu.isWideViewport = function() {
        return _mqWideNav.matches;
    };

    /**
     * Toggle desktop/mobile navigation using `matchMedia` event handler.
     */
    Menu.handleState = function() {
        _mqWideNav = matchMedia('(min-width: ' + _wideBreakpoint + ')');

        _mqWideNav.addListener(function(mq) {
            Menu.close();

            if (mq.matches) {
                Menu.unbindEventsSmall();
                Menu.bindEventsWide();
            } else {
                Menu.unbindEventsWide();
                Menu.bindEventsSmall();
            }
        });

        if (Menu.isWideViewport()) {
            Menu.bindEventsWide();
        } else {
            Menu.bindEventsSmall();
        }
    };

    /**
     * Bind events for wide viewports.
     */
    Menu.bindEventsWide = function() {
        var items = document.querySelectorAll('.c-menu-category.mzp-js-expandable');
        var link;
        var close;

        for (var i = 0; i < items.length; i++) {
            items[i].addEventListener('mouseenter', Menu.onMouseEnter, false);
            items[i].addEventListener('mouseleave', Menu.onMouseLeave, false);
            items[i].addEventListener('focusout', Menu.onFocusOut, false);

            link = items[i].querySelector('.c-menu-title');
            link.addEventListener('click', Menu.onClickWide, false);

            close = items[i].querySelector('.c-menu-button-close');
            close.addEventListener('click', Menu.onCloseButtonClick, false);
        }

        // close with escape key
        document.addEventListener('keyup', Menu.onDocumentKeyUp, false);
    };

    /**
     * Unbind events for wide viewports.
     */
    Menu.unbindEventsWide = function() {
        var items = document.querySelectorAll('.c-menu-category.mzp-js-expandable');
        var link;
        var close;

        for (var i = 0; i < items.length; i++) {
            items[i].removeEventListener('mouseenter', Menu.onMouseEnter, false);
            items[i].removeEventListener('mouseleave', Menu.onMouseLeave, false);
            items[i].removeEventListener('focusout', Menu.onFocusOut, false);

            link = items[i].querySelector('.c-menu-title');
            link.removeEventListener('click', Menu.onClickWide, false);

            close = items[i].querySelector('.c-menu-button-close');
            close.removeEventListener('click', Menu.onCloseButtonClick, false);
        }

        document.removeEventListener('keyup', Menu.onDocumentKeyUp, false);
    };

    /**
     * Bind events for small viewports.
     */
    Menu.bindEventsSmall = function() {
        var items = document.querySelectorAll('.c-menu-category.mzp-js-expandable .c-menu-title');

        for (var i = 0; i < items.length; i++) {
            items[i].addEventListener('click', Menu.onClickSmall, false);
        }
    };

    /**
     * Unbind events for small viewports.
     */
    Menu.unbindEventsSmall = function() {
        var items = document.querySelectorAll('.c-menu-category.mzp-js-expandable .c-menu-title');

        for (var i = 0; i < items.length; i++) {
            items[i].removeEventListener('click', Menu.onClickSmall, false);
        }
    };

    /**
     * Set initial ARIA menu panel states.
     */
    Menu.setAria = function() {
        var items = document.querySelectorAll('.c-menu-category.mzp-js-expandable .c-menu-title');

        for (var i = 0; i < items.length; i++) {
            items[i].setAttribute('aria-expanded', false);
        }
    };

    /**
     * Enhances the menu for 1st class JS support.
     */
    Menu.enhanceJS = function() {
        var menu = document.querySelectorAll('.c-menu');

        for (var i = 0; i < menu.length; i++) {
            menu[i].classList.remove('mzp-is-basic');
            menu[i].classList.add('mzp-is-enhanced');
        }
    };

    /**
     * Basic feature detect for 1st class menu JS support.
     */
    Menu.isSupported = function() {
        if (typeof Mzp.Supports !== 'undefined') {
            return Mzp.Supports.matchMedia && Mzp.Supports.classList;
        } else {
            return false;
        }
    };

    /**
     * Initialise menu.
     * @param {Object} options - configurable options.
     */
    Menu.init = function(options) {
        if (typeof options === 'object') {
            for (var i in options) {
                if (options.hasOwnProperty.call(i)) {
                    _options[i] = options[i];
                }
            }
        }

        if (Menu.isSupported()) {
            Menu.handleState();
            Menu.setAria();
            Menu.enhanceJS();
        }
    };

    window.Mzp.Menu = Menu;

})(window.Mzp);
