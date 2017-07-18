/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var _closeButton = document.getElementById('nav-drawer-close-button');
    var _drawer = document.getElementById('moz-global-nav-drawer');
    var _menuButton = document.getElementById('nav-button-menu');
    var _nav = document.getElementById('moz-global-nav');
    var _page = document.getElementsByTagName('html')[0];

    // feature detects
    var _supportsBoundingClientRect = 'getBoundingClientRect' in document.createElement('div');
    var _featureQueriesSupported = typeof CSS !== 'undefined' && typeof CSS.supports !== 'undefined';
    var _supportsTransition = _featureQueriesSupported && CSS.supports('(transition: max-height .6s ease-in-out)');

    /**
     * Determine if node is a child element of a given parent.
     * @param {Object} parent - DOM parent node.
     * @param {Object} child - DOM child node.
     * @return {Boolean}
     */
    var _isChildNode = function(parent, child) {
        var node = child.parentNode;
        while (node !== null) {
            if (node === parent) {
                return true;
            }
            node = node.parentNode;
        }
        return false;
    };

    /**
     * Scrolls an element into visible viewport
     * @param {Object} el - DOM node.
     */
    var _scrollElementIntoView = function(el) {
        if (_supportsBoundingClientRect) {
            window.scrollTo(0, (el.getBoundingClientRect().top - document.body.getBoundingClientRect().top) - 20);
        }
    };

    /**
     * Mozilla global navigation
     */
    var mozGlobalNav = {

        // Simple feature detect for grade-A browser support.
        cutsTheMustard: function() {
            return 'querySelector' in document &&
                   'querySelectorAll' in document &&
                   'addEventListener' in window &&
                   'classList' in document.createElement('div');
        },

        /**
         * Toggle the drawer state
         * @param {String} id - optional accordion id to expand on open.
         */
        toggleDrawer: function(accordionId) {

            // make sure we're at the top of the window before opening drawer.
            if (!_page.classList.contains('moz-nav-open')) {
                window.scrollTo(0, 0);
            }

            _page.classList.toggle('moz-nav-open');

            if (_page.classList.contains('moz-nav-open')) {
                mozGlobalNav.onDrawerOpen(accordionId);
            } else {
                mozGlobalNav.onDrawerClose();
            }
        },

        // handle menu button & mask click events to toggle drawer
        handleToggleDrawerEvent: function() {
            mozGlobalNav.toggleDrawer();
        },

        onDrawerOpen: function() {
            document.addEventListener('keydown', mozGlobalNav.handleEscKey, false);
            _page.addEventListener('focusin', mozGlobalNav.handleDrawerFocusOut, false);

            _drawer.setAttribute('aria-hidden', 'false');
        },

        onDrawerClose: function() {
            document.removeEventListener('keydown', mozGlobalNav.handleEscKey, false);
            _page.removeEventListener('focusin', mozGlobalNav.handleDrawerFocusOut, false);

            _drawer.setAttribute('aria-hidden', 'true');

            // clear selected link in horizontal primary navigation
            mozGlobalNav.clearSelectedNavLink();

            // return focus to the menu button.
            _menuButton.focus();
        },

        // Keeps keyboard focus in the drawer when in open state.
        handleDrawerFocusOut: function(e) {
            var elemIsChild = _isChildNode(_drawer, e.target);

            if (!elemIsChild) {
                _closeButton.focus();
            }
        },

        /**
         * Adjust scroll position to Y offset of accordion after expand.
         * @param {Object} el - DOM node to be scrolled to.
         */
        handleAccordionTransition: function(heading) {
            var selectedMenu = document.querySelector('.nav-menu-primary-links > li > .summary.selected + .detail');
            var originalScrollPosition = window.pageYOffset;
            var scrollThreshold = 100; // has user has scrolled down from top of viewport.

            var onTransitionEnd = function(e) {
                var scrollPosition = window.pageYOffset;

                if (e.propertyName !== 'max-height') {
                    return;
                }

                // only adjust scroll position if user has not already scrolled independently.
                if (scrollPosition > scrollThreshold && scrollPosition === originalScrollPosition) {
                    _scrollElementIntoView(heading);
                }

                selectedMenu.removeEventListener('transitionend', onTransitionEnd, false);
            };

            if (selectedMenu) {
                // if we support transitions, wait until accordion expands.
                if (_supportsTransition) {
                    selectedMenu.addEventListener('transitionend', onTransitionEnd, false);
                }
                // else adjust scroll position straight away.
                else if (originalScrollPosition > scrollThreshold) {
                    _scrollElementIntoView(heading);
                }
            }
        },

        // Toggle vertical navigation menu in the side drawer.
        toggleDrawerMenu: function(id) {
            var link = document.querySelector('.nav-menu-primary-links > li > .summary[data-id="'+ id +'"] > a');
            var heading = link.parentNode;

            if (link && heading && heading.classList.contains('summary')) {
                link.focus();

                if (!heading.classList.contains('selected')) {
                    mozGlobalNav.closeDrawerMenu();
                }

                heading.classList.toggle('selected');

                if (heading.classList.contains('selected')) {
                    // Set aria roles for expanded state.
                    heading.setAttribute('aria-selected', 'true');
                    heading.setAttribute('aria-expanded', 'true');

                    // Set GA attribute for next time heading is clicked.
                    link.setAttribute('data-link-name', 'collapse');

                    // When expanding a menu, adjust the scroll position if needed.
                    mozGlobalNav.handleAccordionTransition(heading);
                } else {
                    // Set aria roles for collapsed state.
                    heading.setAttribute('aria-selected', 'false');
                    heading.setAttribute('aria-expanded', 'false');

                    // Set GA attribute for next time heading is clicked.
                    link.setAttribute('data-link-name', 'expand');
                }
            }
        },

        // Closes currently selected vertical navigation menu.
        closeDrawerMenu: function() {
            var summary = document.querySelector('.nav-menu-primary-links .summary.selected');
            var link = document.querySelector('.nav-menu-primary-links .summary.selected > a');

            if (summary && link) {
                summary.classList.remove('selected');
                summary.setAttribute('aria-selected', 'false');
                summary.setAttribute('aria-expanded', 'false');
                link.setAttribute('data-link-name', 'expand');
            }
        },

        /**
         * Selects horizontal navigation link
         * @param (String) - id of item to be selected
         */
        selectNavLink: function(id) {
            var target = document.querySelector('.nav-primary-links > li > a[data-id="' + id + '"]');

            if (target) {
                mozGlobalNav.clearSelectedNavLink();
                target.classList.add('selected');
                target.setAttribute('aria-selected', 'true');
            }
        },

        // Clears the currently selected horizontal navigation link.
        clearSelectedNavLink: function() {
            var target = document.querySelector('.nav-primary-links > li > a.selected');

            if (target) {
                target.classList.remove('selected');
                target.setAttribute('aria-selected', 'false');
            }
        },

        // Closes the horizontal drawer if escape key is pressed.
        handleEscKey: function(e) {
            var isEscape = false;
            e = e || window.event;

            if ('key' in e) {
                isEscape = (e.key === 'Escape' || e.key === 'Esc');
            } else {
                isEscape = (e.keyCode === 27);
            }

            if (isEscape && _page.classList.contains('moz-nav-open')) {
                mozGlobalNav.toggleDrawer();
            }
        },

        // Handle clicks on the vertical drawer navigation links.
        handleDrawerLinkClick: function(e) {
            e.preventDefault();
            var target = e.target.parentNode.getAttribute('data-id');

            if (target) {
                mozGlobalNav.toggleDrawerMenu(target);
            }
        },

        // Bind common event handlers for the navigation menu
        bindEvents: function() {
            var menuLinks = document.querySelectorAll('.nav-menu-primary-links > li > .summary > a');

            for (var i = 0; i < menuLinks.length; i++) {
                menuLinks[i].addEventListener('click', mozGlobalNav.handleDrawerLinkClick, false);
            }

            _menuButton.addEventListener('click', mozGlobalNav.handleToggleDrawerEvent, false);
            _closeButton.addEventListener('click', mozGlobalNav.handleToggleDrawerEvent, false);

            var mask = document.getElementById('moz-global-nav-page-mask');
            mask.addEventListener('click', mozGlobalNav.handleToggleDrawerEvent, false);
        },

        /**
         * Sets initial WAI-ARIA roles for global navigation state
         */
        initARIARoles: function() {
            var accordion = document.querySelector('.nav-menu-primary-links');
            var accordionHeadings = accordion.querySelectorAll('.summary');
            var rolePrefix = 'moz-global-nav-item-';

            accordion.setAttribute('role', 'tablist');

            for (var i = 0; i < accordionHeadings.length; i++) {
                accordionHeadings[i].setAttribute('role', 'tab');
                accordionHeadings[i].setAttribute('aria-selected', 'false');
                accordionHeadings[i].setAttribute('aria-expanded', 'false');
                accordionHeadings[i].setAttribute('aria-controls',
                    rolePrefix + accordionHeadings[i].getAttribute('data-id'));
            }

            _drawer.setAttribute('aria-hidden', 'true');
            _menuButton.setAttribute('aria-controls', 'moz-global-nav-drawer');
            _closeButton.setAttribute('aria-controls', 'moz-global-nav-drawer');
        },

        /**
         * Adds an element to document.body for the semi-opaque overlay visible
         * when the horizontal drawer menu is open.
         */
        createNavMask: function() {
            var mask = document.createElement('div');
            mask.id = mask.className = 'moz-global-nav-page-mask';
            document.body.appendChild(mask);
        },

        initSimpleNav: function() {
            _nav.setAttribute('class', 'moz-global-nav simple');
        },

        /**
         * Initializes the navigation for interaction
         */
        init: function() {
            if (mozGlobalNav.cutsTheMustard()) {
                _menuButton.classList.remove('nav-hidden');
                mozGlobalNav.initARIARoles();
                mozGlobalNav.createNavMask();
                mozGlobalNav.bindEvents();
            } else {
                mozGlobalNav.initSimpleNav();
            }
        }
    };

    if (_nav) {
        mozGlobalNav.init();
    }

})();
