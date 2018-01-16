/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // If there's no nav-main element, don't initialize the menu.
    if ($('#nav-main').length === 0) {
        return;
    }

    var NavMain = {};

    /**
     * Whether or not MS Internet Explorer version 4, 5, 6, 7 or 8 is used
     *
     * If true, the small mode is never triggered.
     *
     * @var Boolean
     */
    NavMain.isMSIEpre9 = (function() {
        return (/MSIE\ (4|5|6|7|8)/.test(navigator.userAgent));
    })();

    /**
     * Whether or not the main nav is in small mode
     *
     * @var Boolean
     */
    NavMain.smallMode = false;

    /**
     * Whether or not the main menu is opened in small mode
     *
     * @var Boolean
     */
    NavMain.smallMenuOpen = false;

    /**
     * Jquery object representing the currently opened sub-menu
     * in small-mode
     *
     * @var jQuery
     */
    NavMain.currentSmallSubmenu = null;

    /**
     * Jquery object representing the previously focused main menu item
     *
     * @var jQuery
     */
    NavMain.previousMenuItem = null;

    /**
     * Jquery object representing the currently focused sub-menu item
     *
     * @var jQuery
     */
    NavMain.currentSubmenuItem = null;

    /**
     * Main menu items in the menubar
     *
     * @var jQuery
     */
    NavMain.mainMenuItems = null;

    /**
     * Main menu items in the menubar
     *
     * @var jQuery
     */
    NavMain.mainMenuLinks = null;

    /**
     * Main menu mobile toggle button
     *
     * @var jQuery
     */
    NavMain.toggleButton = null;

    NavMain.init = function() {
        NavMain.toggleButton = $('#masthead .toggle');
        NavMain.mainMenuItems = $('#nav-main .has-submenus > li');
        NavMain.mainMenuLinks = $('#nav-main ul > li > [tabindex="0"]');

        NavMain.mainMenuItems
            .on('mouseover focusin', NavMain.handleFocusIn)
            .on('mouseout focusout', NavMain.handleFocusOut)
            .each(NavMain.initSubmenu);

        if (!NavMain.isMSIEpre9) {
            $(window).on('resize', NavMain.handleResize);
            NavMain.handleResize();
        }

        // set up small-mode menu toggle button
        $('#masthead .toggle')
            .on('click', function(e) {
                e.preventDefault();
                NavMain.toggleSmallMenu();
            })
            .on('keydown', function(e) {
                if (e.keyCode === 13 || e.keyCode === 32) {
                    e.preventDefault();
                    NavMain.toggleSmallMenu();
                } else if (e.keyCode === 27 && NavMain.smallMenuOpen) {
                    NavMain.closeSmallMenu();
                }
            });

        // On touch-enabled devices, hijack the click event and just make it focus
        // the item. This prevents flashing menus on iOS and prevents clicking on
        // a top-level item causing navigation on Android.
        if ('ontouchstart' in window) {
            NavMain.mainMenuLinks.on('click', function(e) {
                e.preventDefault();
                this.trigger('focus');
            });
        }

        // With JavaScript enabled, we can provide a full navigation with
        // #nav-main. Now "hide" the duplicated #footer-menu from AT.
        $('#footer-menu').attr('role', 'presentation');
    };

    NavMain.handleFocusIn = function() {
        var item = $(this);

        if (NavMain.previousMenuItem) {
            if (NavMain.previousMenuItem.attr('id') !== item.attr('id')) {
                // Close the last selected menu
                NavMain.previousMenuItem.dequeue();
            } else {
                NavMain.previousMenuItem.clearQueue();
            }
        }

        // Open the menu
        item.addClass('hover')
            .find('[aria-expanded="false"]')
            .attr('aria-expanded', 'true');
    };

    NavMain.handleFocusOut = function() {
        NavMain.previousMenuItem = $(this);
        NavMain.previousMenuItem
            .delay(100)
            .queue(function() {
                if (NavMain.previousMenuItem) {
                    // Close the menu
                    NavMain.previousMenuItem
                        .clearQueue()
                        .removeClass('hover')
                        .find('[aria-expanded="true"]')
                        .attr('aria-expanded', 'false');

                    NavMain.previousMenuItem = null;

                    // If there was a focused sub-menu item, blur it
                    if (NavMain.currentSubmenuItem) {
                        NavMain.currentSubmenuItem.get(0).blur();
                    }
                }
            });
    };

    NavMain.initSubmenu = function(menuIdx) {
        var menuItems = $(this).find('a');

        menuItems.on('mouseover', function() {
            this.focus(); // Sometimes $(this).trigger('focus') doesn't work
        }).on('focus', function() {
            NavMain.currentSubmenuItem = $(this);
        }).each(function(itemIdx) {
            $(this).on('keydown', function(e) {
                var target;
                switch (e.keyCode) {
                case 27: // Esc
                    NavMain.handleEscKeypress(e);
                    break;
                case 33: // Page Up
                case 36: // Home
                    target = menuItems.first();
                    break;
                case 34: // Page Down
                case 35: // End
                    target = menuItems.last();
                    break;
                case 38: // Up
                    target = (itemIdx > 0)
                        ? menuItems.eq(itemIdx - 1)
                        : menuItems.last();
                    break;
                case 40: // Down
                    target = (itemIdx < menuItems.length - 1)
                        ? menuItems.eq(itemIdx + 1)
                        : menuItems.first();
                    break;
                case 37: // Left
                    target = (menuIdx > 0)
                        ? NavMain.mainMenuLinks.eq(menuIdx - 1)
                        : NavMain.mainMenuLinks.last();
                    break;
                case 39: // Right
                    target = (menuIdx < NavMain.mainMenuLinks.length - 1)
                        ? NavMain.mainMenuLinks.eq(menuIdx + 1)
                        : NavMain.mainMenuLinks.first();
                    break;
                }
                if (target) {
                    target.get(0).focus(); // Sometimes target.trigger('focus') doesn't work
                    return false;
                }
                return true;
            });
        });
    };

    NavMain.handleResize = function() {
        var width = $(window).width();

        if (width <= 760 && !NavMain.smallMode) {
            NavMain.enterSmallMode();
        }

        if (width > 760 && NavMain.smallMode) {
            NavMain.leaveSmallMode();
        }
    };

    NavMain.enterSmallMode = function() {
        NavMain.unlinkMainMenuItems();

        $('#nav-main-menu').css('display', 'none').attr('aria-hidden');

        $('#outer-wrapper').on('click.mobile-nav', NavMain.handleDocumentClick);
        $('a, input, textarea, button, :focus').on('focus.mobile-nav', NavMain.handleDocumentFocus);

        $('#nav-main-menu, #nav-main-menu .submenu').attr('aria-hidden', 'true');

        // remove submenu click handler and CSS class
        NavMain.mainMenuLinks
            .addClass('submenu-item')
            .off('click', NavMain.handleSubmenuClick);

        // add click handler to menu links to hide menu
        NavMain.linkMenuHideOnClick();

        NavMain.smallMode = true;
    };

    NavMain.leaveSmallMode = function() {
        NavMain.relinkMainMenuLinks();

        $('#nav-main-menu').css('display', '').removeAttr('aria-hidden');

        $('#outer-wrapper').off('click.mobile-nav', NavMain.handleDocumentClick);
        $('a, input, textarea, button, :focus').off('focus.mobile-nav', NavMain.handleDocumentFocus);

        NavMain.toggleButton.removeClass('open').attr('aria-expanded', false);

        // reset submenus
        $('#nav-main-menu > li > .submenu').stop(true).css({
            'left'         : '',
            'top'          : '',
            'display'      : '',
            'opacity'      : '',
            'height'       : '',
            'marginTop'    : '',
            'marginBottom' : ''
        }).attr('aria-expanded', 'false');

        // remove click handler from menu links that hide menu
        NavMain.unlinkMenuHideOnClick();

        NavMain.currentSmallSubmenu = null;
        NavMain.smallMode = false;
        NavMain.smallMenuOpen = false;
    };

    /**
     * Causes smallMode menu to close when clicking on a menu/submenu link
     *
     * Allows closing of smallMode menu when navigating in-page
     */
    NavMain.linkMenuHideOnClick = function() {
        if (NavMain.mainMenuItems.length === 0) {
            $('#nav-main-menu > li > a').on('click.smallmode', function() {
                NavMain.closeSmallMenu();
            });
        } else {
            $('.submenu > li > a').on('click.smallmode', function() {
                NavMain.closeSmallMenu();
            });
        }
    };

    /**
     * Remove smallMode menu closing when clicking menu/submenu link
     */
    NavMain.unlinkMenuHideOnClick = function() {
        if (NavMain.mainMenuItems.length === 0) {
            $('#nav-main-menu > li > a').off('click.smallmode');
        } else {
            $('.submenu > li > a').off('click.smallmode');
        }
    };

    /**
     * Removes the href attribute from menu items with submenus
     *
     * This prevents load bar from appearing on iOS when you press
     * an item.
     */
    NavMain.unlinkMainMenuItems = function() {
        NavMain.mainMenuLinks.each(function(i, n) {
            var node = $(n);
            if (node.siblings('.submenu')) {
                node.attr('data-old-href', node.attr('href'));
                node.removeAttr('href');
            }
        });
    };

    /**
     * Returns the href attribute back to main menu links
     */
    NavMain.relinkMainMenuLinks = function() {
        NavMain.mainMenuLinks.each(function(i, n) {
            var node = $(n);
            if (node.attr('data-old-href')) {
                node.attr('href', node.attr('data-old-href'));
                node.removeAttr('data-old-href');
            }
        });
    };

    NavMain.handleDocumentClick = function(e) {
        if (NavMain.smallMode) {
            var $clicked = $(e.target);
            if (!$clicked.parents().is('#masthead')) {
                NavMain.closeSmallMenu();
            }
        }
    };

    NavMain.handleDocumentFocus = function(e) {
        var $focused = $(e.target);
        if (!$focused.parents().is('#masthead')) {
            NavMain.closeSmallMenu();
        }
    };

    NavMain.handleToggleKeypress = function(e) {
        if (e.keyCode === 13) {
            NavMain.toggleSmallMenu();
        }
    };

    NavMain.handleEscKeypress = function(e) {
        if (e.keyCode === 27 && NavMain.smallMenuOpen) {
            NavMain.closeSmallMenu();
            // Set focus back to the menu button
            NavMain.toggleButton.trigger('focus');
        }
    };

    NavMain.toggleSmallMenu = function() {
        if (NavMain.smallMenuOpen) {
            NavMain.closeSmallMenu();
        } else {
            NavMain.openSmallMenu();
        }
    };

    NavMain.openSmallMenu = function() {
        if (NavMain.smallMenuOpen) {
            return;
        }

        $('#nav-main-menu').slideDown(150, function() {
            NavMain.toggleButton.addClass('open').attr('aria-expanded', true);
        }).removeAttr('aria-hidden');

        // add click handler and set submenu class on submenus
        NavMain.mainMenuLinks
            .addClass('submenu-item')
            .on('click', NavMain.handleSubmenuClick)
            .on('keydown', NavMain.handleSubmenuKeypress);

        $('#nav-main-menu > li > a').on('keydown', NavMain.handleEscKeypress);

        NavMain.smallMenuOpen = true;
    };

    NavMain.closeSmallMenu = function() {
        if (!NavMain.smallMenuOpen) {
            return;
        }

        $('#nav-main-menu, #nav-main-menu .submenu').slideUp(100, function() {
            NavMain.toggleButton.removeClass('open').attr('aria-expanded', false);
        }).attr('aria-hidden', 'true');

        // remove submenu click handler and CSS class
        NavMain.mainMenuLinks
            .addClass('submenu-item')
            .off('click', NavMain.handleSubmenuClick)
            .off('keydown', NavMain.handleSubmenuKeypress);

        $('#nav-main-menu > li > a').off('keydown', NavMain.handleEscKeypress);

        if (NavMain.currentSmallSubmenu) {
            NavMain.closeSmallSubmenu(NavMain.currentSmallSubmenu);
        }
        NavMain.currentSmallSubmenu = null;

        NavMain.smallMenuOpen = false;
    };

    NavMain.handleSubmenuClick = function(e) {
        e.preventDefault();
        var menu = $(this).siblings('.submenu');
        NavMain.openSmallSubmenu(menu);
    };

    NavMain.handleSubmenuKeypress = function(e) {
        if (e.keyCode === 13 || e.keyCode === 32) {
            e.preventDefault();
            var menu = $(this).siblings('.submenu');
            NavMain.openSmallSubmenu(menu);
        }
    };

    NavMain.openSmallSubmenu = function(menu) {
        // close previous menu
        if (NavMain.currentSmallSubmenu && NavMain.currentSmallSubmenu.get(0).id !== menu.get(0).id) {
            NavMain.closeSmallSubmenu(NavMain.currentSmallSubmenu);
        }

        // skip current menu
        if (NavMain.currentSmallSubmenu && NavMain.currentSmallSubmenu.get(0).id === menu.get(0).id) {
            // still focus first item
            menu.find('a').get(0).focus();
            return;
        }

        menu.stop(true).css({
            'left'         : '80px',
            'top'          : 'auto',
            'display'      : 'none',
            'opacity'      : '1',
            'height'       : 'auto',
            'marginTop'    : '-8px',
            'marginBottom' : '0'
        }).slideDown(150).attr('aria-expanded', 'true');

        // focus first item
        menu.find('a').get(0).focus();

        NavMain.currentSmallSubmenu = menu;
    };

    NavMain.closeSmallSubmenu = function(menu) {
        menu.stop(true).fadeOut(100, function() {
            menu.css({
                'left'         : '',
                'top'          : '',
                'display'      : '',
                'opacity'      : '',
                'height'       : '',
                'marginTop'    : '',
                'marginBottom' : ''
            }).attr('aria-expanded', 'false');
        });
    };

    $(document).ready(NavMain.init);

})();
