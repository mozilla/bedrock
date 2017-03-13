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
    var _navLinks;
    var _drawerTimeout;

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

            _page.classList.toggle('moz-nav-open');

            if (_page.classList.contains('moz-nav-open')) {
                mozGlobalNav.onDrawerOpen(accordionId);
            } else {
                mozGlobalNav.onDrawerClose();
            }

            // Add a little delay before toggling the accordion
            // for a smoother transition when the drawer moves.
            clearTimeout(_drawerTimeout);
            _drawerTimeout = setTimeout(function() {
                if (_page.classList.contains('moz-nav-open')) {
                    if (accordionId) {
                        mozGlobalNav.toggleDrawerMenu(accordionId);
                    }
                } else {
                    mozGlobalNav.closeSecondaryMenuItems();
                }
            }, 320);
        },

        // handle menu button & mask click events to toggle drawer
        handleToggleDrawerEvent: function() {
            mozGlobalNav.toggleDrawer();
        },

        onDrawerOpen: function() {
            document.addEventListener('keydown', mozGlobalNav.handleEscKey, false);
            _page.addEventListener('focusin', mozGlobalNav.handleDrawerFocusOut, false);

            window.dataLayer.push({
                'event': 'global-nav',
                'interaction': 'menu-open'
            });
        },

        onDrawerClose: function() {
            document.removeEventListener('keydown', mozGlobalNav.handleEscKey, false);
            _page.removeEventListener('focusin', mozGlobalNav.handleDrawerFocusOut, false);

            // clear selected link in horizontal primary navigation
            mozGlobalNav.clearSelectedNavLink();

            // return focus to the menu button.
            _menuButton.focus();

            window.dataLayer.push({
                'event': 'global-nav',
                'interaction': 'menu-close'
            });
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
            var link = document.querySelector('.nav-menu-primary-links > li > .summary > a[data-id="'+ id +'"]');
            var heading = link.parentNode;
            var interaction;

            if (link && heading && heading.classList.contains('summary')) {
                link.focus();

                if (!heading.classList.contains('selected')) {
                    mozGlobalNav.selectNavLink(id);
                    mozGlobalNav.closeSecondaryMenuItems();
                    interaction = 'expand';
                } else {
                    interaction = 'collapse';
                }

                heading.classList.toggle('selected');

                if (heading.classList.contains('selected')) {
                    // When expanding a menu, adjust the scroll position if needed.
                    mozGlobalNav.handleAccordionTransition(heading);
                }

                window.dataLayer.push({
                    'event': 'global-nav',
                    'interaction': 'secondary-nav-' + interaction,
                    'secondary-nav-heading': id
                });
            }
        },

        // Closes all vertical navigation menu items.
        closeSecondaryMenuItems: function() {
            var menuLinks = document.querySelectorAll('.nav-menu-primary-links > li > .summary');

            for (var i = 0; i < menuLinks.length; i++) {
                menuLinks[i].classList.remove('selected');
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
            }
        },

        // Clears the currently selected horizontal navigation link.
        clearSelectedNavLink: function() {
            for (var i = 0; i < _navLinks.length; i++) {
                _navLinks[i].classList.remove('selected');
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
            var target = e.target.getAttribute('data-id');

            if (target) {
                mozGlobalNav.toggleDrawerMenu(target);
            }
        },

        // Handle clicks on the horozontal navigation links.
        handleNavLinkClick: function(e) {
            e.preventDefault();
            var id = e.target.getAttribute('data-id');

            if (id) {
                mozGlobalNav.selectNavLink(id);
                mozGlobalNav.toggleDrawer(id);
            }
        },

        // Bind common event handlers for the navigation menu
        bindEvents: function() {
            var menuLinks = document.querySelectorAll('.nav-menu-primary-links > li > .summary > a');

            for (var i = 0; i < menuLinks.length; i++) {
                menuLinks[i].addEventListener('click', mozGlobalNav.handleDrawerLinkClick, false);
            }

            for (var j = 0; j < _navLinks.length; j++) {
                _navLinks[j].addEventListener('click', mozGlobalNav.handleNavLinkClick, false);
            }

            _menuButton.addEventListener('click', mozGlobalNav.handleToggleDrawerEvent, false);
            _closeButton.addEventListener('click', mozGlobalNav.handleToggleDrawerEvent, false);

            var mask = document.getElementById('moz-global-nav-page-mask');
            mask.addEventListener('click', mozGlobalNav.handleToggleDrawerEvent, false);
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
                _navLinks = document.querySelectorAll('.nav-primary-links > li > a');

                _menuButton.classList.remove('nav-hidden');

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
