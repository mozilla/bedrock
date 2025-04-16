/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const MzpMenu = {};
let _menuOpen = false;
let _hoverTimeout;
const _hoverTimeoutDelay = 150;
let _mqWideNav;
const _wideBreakpoint = '768px';

const _options = {
    onMenuOpen: null,
    onMenuClose: null,
    onMenuButtonClose: null
};

/**
 * Opens a menu panel.
 * @param {Object} el - DOM element (`.mzp-c-menu-category.mzp-js-expandable`)
 * @param {Boolean} animate - show animation when menu panel opens.
 */
MzpMenu.open = (el, animate) => {
    if (animate) {
        el.classList.add('mzp-is-animated');
    }

    el.classList.add('mzp-is-selected');

    _menuOpen = true; // For checking menu state on keyup.

    el.querySelector('.m24-c-menu-title').setAttribute('aria-expanded', true);

    if (typeof _options.onMenuOpen === 'function') {
        _options.onMenuOpen(el);
    }

    // set new nav focusable elements to be focusable elements on MzpMenu
    if (typeof window.MzpNavigation !== 'undefined') {
        if (typeof window.MzpNavigation.setFocusList === 'function') {
            window.MzpNavigation.setFocusList(
                '.m24-c-navigation-logo-link, .m24-c-navigation-menu-button, .mzp-is-selected a'
            );
        }
    }
};

/**
 * Closes all currently open menu panels.
 * Note: on small screens more than one menu can be open at the same time.
 */
MzpMenu.close = () => {
    const current = document.querySelectorAll(
        '.m24-c-menu-category.mzp-is-selected'
    );

    for (let i = 0; i < current.length; i++) {
        // The following classes must be removed in the correct order
        // to work around a bug in bedrock's classList polyfill for IE9.
        // https://github.com/mozilla/bedrock/issues/6221 :/
        current[i].classList.remove('mzp-is-selected');
        current[i].classList.remove('mzp-is-animated');

        current[i]
            .querySelector('.m24-c-menu-title')
            .setAttribute('aria-expanded', false);
    }

    _menuOpen = false; // For checking menu state on keyup.

    if (typeof _options.onMenuClose === 'function' && current.length > 0) {
        _options.onMenuClose();
    }

    // reset keyboard navigation focus trap for MzpNavigation
    window.MzpNavigation.resetFocusListFunction();

    return current.length > 0;
};

MzpMenu.onDocumentKeyUp = (e) => {
    if (e.keyCode === 27 && _menuOpen) {
        MzpMenu.close();
    }
};

/**
 * Menu panel close button `click` event handler.
 * @param {Object} e - Event object.
 */
MzpMenu.onCloseButtonClick = (e) => {
    e.preventDefault();

    if (typeof _options.onMenuButtonClose === 'function') {
        _options.onMenuButtonClose();
    }

    MzpMenu.close();
};

/**
 * Toggles the open/closed state of a menu panel.
 * @param {Object} el - DOM element (`.mzp-c-menu-category.mzp-js-expandable`)
 */
MzpMenu.toggle = (el) => {
    const state = el.classList.contains('mzp-is-selected') ? true : false;

    if (!state) {
        MzpMenu.open(el);
    } else {
        // The following classes must be removed in the correct order
        // to work around a bug in bedrock's classList polyfill for IE9.
        // https://github.com/mozilla/bedrock/issues/6221 :/
        el.classList.remove('mzp-is-selected');
        el.classList.remove('mzp-is-animated');
        el.querySelector('.m24-c-menu-title').setAttribute(
            'aria-expanded',
            false
        );

        if (typeof _options.onMenuClose === 'function') {
            _options.onMenuClose();
        }

        // reset keyboard navigation focus trap for MzpNavigation
        window.MzpNavigation.resetFocusListFunction();
    }
};

/**
 * Menu `mouseenter` event handler.
 * Opens the menu only when hover intent is shown.
 * Animates only if a menu panel is not already open.
 * @param {Object} e - Event object.
 */
MzpMenu.onMouseEnter = (e) => {
    clearTimeout(_hoverTimeout);

    _hoverTimeout = setTimeout(() => {
        const current = MzpMenu.close();
        const animate = current ? false : true;

        MzpMenu.open(e.target, animate);
    }, _hoverTimeoutDelay);
};

/**
 * Menu `mouseleave` event handler.
 * Closes the menu only when hover intent is shown.
 */
MzpMenu.onMouseLeave = () => {
    clearTimeout(_hoverTimeout);

    _hoverTimeout = setTimeout(() => {
        MzpMenu.close();
    }, _hoverTimeoutDelay);
};

/**
 * Menu `focusout` event handler.
 * Closes the menu when focus moves to an element outside of the currently open panel.
 */
MzpMenu.onFocusOut = function () {
    /**
     * Note: 'this' needs to reference the active DOM node, so here `focusOut` is not
     * an arrow (=>) function, since that would lexically bind `this` to `window`.
     */
    const self = this;

    /**
     * After an element loses focus, `document.activeElement` will always be `body` before
     * moving to the next element. A `setTimeout` of `0` circumvents this issue as it
     * re-queues the JavaScript to run at the end of the current execution.
     */
    setTimeout(() => {
        // If the menu is open and the newly focused element is not a child, then call close().
        if (
            !self.contains(document.activeElement) &&
            self.classList.contains('mzp-is-selected')
        ) {
            MzpMenu.close();
        }
    }, 0);
};

/**
 * Menu link `click` event handler for wide viewports.
 * Closes any currently open menu panels before opening the selected one.
 * @param {Object} e - Event object.
 */
MzpMenu.onClickWide = (e) => {
    e.preventDefault();
    MzpMenu.close();
    MzpMenu.open(e.target.parentNode);
};

/**
 * Menu link `click` event handler for small viewports.
 * Toggles the currently selected menu open open/close state.
 * @param {Object} e - Event object.
 */
MzpMenu.onClickSmall = (e) => {
    e.preventDefault();
    MzpMenu.toggle(e.target.parentNode);
};

/**
 * Convenience function for checking `matchMedia` state.
 * @return {Boolean}
 */
MzpMenu.isWideViewport = () => {
    return _mqWideNav.matches;
};

/**
 * Toggle desktop/mobile navigation using `matchMedia` event handler.
 */
MzpMenu.handleState = () => {
    _mqWideNav = matchMedia('(min-width: ' + _wideBreakpoint + ')');

    function menuBind(mq) {
        MzpMenu.close();

        if (mq.matches) {
            MzpMenu.unbindEventsSmall();
            MzpMenu.bindEventsWide();
        } else {
            MzpMenu.unbindEventsWide();
            MzpMenu.bindEventsSmall();
        }
    }

    if (window.matchMedia('all').addEventListener) {
        _mqWideNav.addEventListener('change', menuBind, false);
    } else if (window.matchMedia('all').addListener) {
        _mqWideNav.addListener(menuBind);
    }

    if (MzpMenu.isWideViewport()) {
        MzpMenu.bindEventsWide();
    } else {
        MzpMenu.bindEventsSmall();
    }
};

/**
 * Bind events for wide view ports.
 */
MzpMenu.bindEventsWide = () => {
    const items = document.querySelectorAll(
        '.m24-c-menu-category.mzp-js-expandable'
    );
    let link;
    let close;

    for (let i = 0; i < items.length; i++) {
        items[i].addEventListener('mouseenter', MzpMenu.onMouseEnter, false);
        items[i].addEventListener('mouseleave', MzpMenu.onMouseLeave, false);
        items[i].addEventListener('focusout', MzpMenu.onFocusOut, false);
        link = items[i].querySelector('.m24-c-menu-title');
        link.addEventListener('click', MzpMenu.onClickWide, false);

        close = items[i].querySelector('.m24-c-menu-button-close');
        close.addEventListener('click', MzpMenu.onCloseButtonClick, false);
    }

    // close with escape key
    document.addEventListener('keyup', MzpMenu.onDocumentKeyUp, false);
};

/**
 * Unbind events for wide view ports.
 */
MzpMenu.unbindEventsWide = () => {
    const items = document.querySelectorAll(
        '.m24-c-menu-category.mzp-js-expandable'
    );
    let link;
    let close;

    for (let i = 0; i < items.length; i++) {
        items[i].removeEventListener('mouseenter', MzpMenu.onMouseEnter, false);
        items[i].removeEventListener('mouseleave', MzpMenu.onMouseLeave, false);
        items[i].removeEventListener('focusout', MzpMenu.onFocusOut, false);

        link = items[i].querySelector('.m24-c-menu-title');
        link.removeEventListener('click', MzpMenu.onClickWide, false);

        close = items[i].querySelector('.m24-c-menu-button-close');
        close.removeEventListener('click', MzpMenu.onCloseButtonClick, false);
    }

    document.removeEventListener('keyup', MzpMenu.onDocumentKeyUp, false);
};

/**
 * Bind events for small view ports.
 */
MzpMenu.bindEventsSmall = () => {
    const items = document.querySelectorAll(
        '.m24-c-menu-category.mzp-js-expandable .m24-c-menu-title'
    );

    for (let i = 0; i < items.length; i++) {
        items[i].addEventListener('click', MzpMenu.onClickSmall, false);
    }
};

/**
 * Unbind events for small view ports.
 */
MzpMenu.unbindEventsSmall = () => {
    const items = document.querySelectorAll(
        '.m24-c-menu-category.mzp-js-expandable .m24-c-menu-title'
    );

    for (let i = 0; i < items.length; i++) {
        items[i].removeEventListener('click', MzpMenu.onClickSmall, false);
    }
};

/**
 * Set initial ARIA menu panel states.
 */
MzpMenu.setAria = () => {
    const items = document.querySelectorAll(
        '.m24-c-menu-category.mzp-js-expandable .m24-c-menu-title'
    );

    for (let i = 0; i < items.length; i++) {
        items[i].setAttribute('aria-expanded', false);
    }
};

/**
 * Enhances the menu for 1st class JS support.
 */
MzpMenu.enhanceJS = () => {
    const menu = document.querySelectorAll('.m24-c-menu');

    for (let i = 0; i < menu.length; i++) {
        menu[i].classList.remove('m24-mzp-is-basic');
        menu[i].classList.add('m24-mzp-is-enhanced');
    }
};

/**
 * Basic feature detect for 1st class menu JS support.
 */
MzpMenu.isSupported = () => {
    if (typeof window.MzpSupports !== 'undefined') {
        return window.MzpSupports.matchMedia && window.MzpSupports.classList;
    } else {
        return false;
    }
};

/**
 * Initialize menu.
 * @param {Object} options - configurable options.
 */
MzpMenu.init = (options) => {
    if (typeof options === 'object') {
        for (const i in options) {
            if (Object.prototype.hasOwnProperty.call(options, i)) {
                _options[i] = options[i];
            }
        }
    }

    if (MzpMenu.isSupported()) {
        MzpMenu.handleState();
        MzpMenu.setAria();
        MzpMenu.enhanceJS();
    }
};

export default MzpMenu;
