/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {

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

NavMain.init = function()
{
    NavMain.mainMenuItems = $('#nav-main .has-submenus > li');
    NavMain.mainMenuLinks = $('#nav-main ul > li > [tabindex="0"]');

    NavMain.mainMenuItems
        .bind('mouseover focusin', NavMain.handleFocusIn)
        .bind('mouseout focusout', NavMain.handleFocusOut)
        .each(NavMain.initSubmenu);

    if (!NavMain.isMSIEpre9) {
        $(window).resize(NavMain.handleResize);
        NavMain.handleResize();
    }

    // set up small-mode menu toggle button
    $('#nav-main .toggle')
        .click(function(e) {
            e.preventDefault();
            NavMain.toggleSmallMenu();
        })
        .keydown(function(e) {
            if (e.keyCode == 13) {
                e.preventDefault();
                NavMain.toggleSmallMenu();
            }
        });

    // On touch-enabled devices, hijack the click event and just make it focus
    // the item. This prevents flashing menus on iOS and prevents clicking on
    // a top-level item causing navigation on Android.
    if ('ontouchstart' in window) {
        NavMain.mainMenuLinks.click(function(e) {
            e.preventDefault();
            this.focus();
        });
    }

    // With JavaScript enabled, we can provide a full navigation with
    // #nav-main. Now "hide" the duplicated #footer-menu from AT.
    $('#footer-menu').attr('role', 'presentation');
};

NavMain.handleFocusIn = function(e)
{
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
    item
        .addClass('hover')
        .find('[aria-expanded="false"]')
        .attr('aria-expanded', 'true');
};

NavMain.handleFocusOut = function(e)
{
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

NavMain.initSubmenu = function(menu_idx)
{
    var menuItems = $(this).find('a');

    menuItems.mouseover(function(e) {
        this.focus(); // Sometimes $(this).focus() doesn't work
    }).focus(function() {
        NavMain.currentSubmenuItem = $(this);
    }).each(function(item_idx) {
        $(this).keydown(function(e) {
            var target;
            switch (e.keyCode) {
                case 33: // Page Up
                case 36: // Home
                    target = menuItems.first();
                    break;

                case 34: // Page Down
                case 35: // End
                    target = menuItems.last();
                    break;

                case 38: // Up
                    target = (item_idx > 0)
                        ? menuItems.eq(item_idx - 1)
                        : menuItems.last();

                    break;

                case 40: // Down
                    target = (item_idx < menuItems.length - 1)
                        ? menuItems.eq(item_idx + 1)
                        : menuItems.first();

                    break;

                case 37: // Left
                    target = (menu_idx > 0)
                        ? NavMain.mainMenuLinks.eq(menu_idx - 1)
                        : NavMain.mainMenuLinks.last();

                    break;

                case 39: // Right
                    target = (menu_idx < NavMain.mainMenuLinks.length - 1)
                        ? NavMain.mainMenuLinks.eq(menu_idx + 1)
                        : NavMain.mainMenuLinks.first();

                    break;
            }
            if (target) {
                target.get(0).focus(); // Sometimes target.focus() doesn't work
                return false;
            }
            return true;
        });
    });
};

NavMain.handleResize = function()
{
    var width = $(window).width();

    if (width <= 760 && !NavMain.smallMode) {
        NavMain.enterSmallMode();
    }

    if (width > 760 && NavMain.smallMode) {
        NavMain.leaveSmallMode();
    }
};

NavMain.enterSmallMode = function()
{
    NavMain.unlinkMainMenuItems();

    $('#nav-main-menu')
	.css('display', 'none')
	.attr('aria-hidden');

    $(document).click(NavMain.handleDocumentClick);
    $('a, input, textarea, button, :focus')
        .focus(NavMain.handleDocumentFocus);

    $('#nav-main-menu, #nav-main-menu .submenu')
	.attr('aria-hidden', 'true');

    // remove submenu click handler and CSS class
    NavMain.mainMenuLinks
	.addClass('submenu-item')
	.unbind('click', NavMain.handleSubmenuClick);

    NavMain.smallMode = true;
};

NavMain.leaveSmallMode = function()
{
    NavMain.relinkMainMenuLinks();

    $('#nav-main-menu')
	.css('display', '')
	.removeAttr('aria-hidden');

    $(document).unbind('click', NavMain.handleDocumentClick);
    $('a, input, textarea, button, :focus')
        .unbind('focus', NavMain.handleDocumentFocus);

    $('#nav-main .toggle').removeClass('open');

    // reset submenus
    $('#nav-main-menu > li > .submenu')
	.stop(true)
	.css(
	    {
		'left'         : '',
		'top'          : '',
		'display'      : '',
		'opacity'      : '',
		'height'       : '',
		'marginTop'    : '',
		'marginBottom' : ''
	    }
	)
	.attr('aria-expanded', 'false');

    NavMain.currentSmallSubmenu = null;
    NavMain.smallMode = false;
    NavMain.smallMenuOpen = false;
};

/**
 * Removes the href attribute from menu items with submenus
 *
 * This prevents load bar from appearing on iOS when you press
 * an item.
 */
NavMain.unlinkMainMenuItems = function()
{
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
NavMain.relinkMainMenuLinks = function()
{
    NavMain.mainMenuLinks.each(function(i, n) {
        var node = $(n);
        if (node.attr('data-old-href')) {
            node.attr('href', node.attr('data-old-href'));
            node.removeAttr('data-old-href');
        }
    });
};

NavMain.handleDocumentClick = function(e)
{
    if (NavMain.smallMode) {
        var $clicked = $(e.target);
        if (!$clicked.parents().is('#nav-main')) {
            NavMain.closeSmallMenu();
        }
    }
};

NavMain.handleDocumentFocus = function(e)
{
    var $focused = $(e.target);
    if (!$focused.parents().is('#nav-main')) {
        NavMain.closeSmallMenu();
    }
};

NavMain.handleToggleKeypress = function(e)
{
    if (e.keyCode == 13) {
        NavMain.toggleSmallMenu();
    }
};

NavMain.toggleSmallMenu = function()
{
    if (NavMain.smallMenuOpen) {
        NavMain.closeSmallMenu();
    } else {
        NavMain.openSmallMenu();
    }
};

NavMain.openSmallMenu = function()
{
    if (NavMain.smallMenuOpen) {
        return;
    }

    $('#nav-main-menu')
        .slideDown(150)
        .removeAttr('aria-hidden');

    $('#nav-main .toggle').addClass('open');

    // add click handler and set submenu class on submenus
    NavMain.mainMenuLinks
        .addClass('submenu-item')
        .click(NavMain.handleSubmenuClick);

    // focus first item
    $('#nav-main-menu [tabindex=0]').get(0).focus();

    NavMain.smallMenuOpen = true;
};

NavMain.closeSmallMenu = function()
{
    if (!NavMain.smallMenuOpen) {
        return;
    }

    $('#nav-main-menu, #nav-main-menu .submenu')
        .slideUp(100)
        .attr('aria-hidden', 'true');

    $('#nav-main .toggle').removeClass('open');

    // remove submenu click handler and CSS class
    NavMain.mainMenuLinks
        .addClass('submenu-item')
        .unbind('click', NavMain.handleSubmenuClick);

    if (NavMain.currentSmallSubmenu) {
        NavMain.closeSmallSubmenu(NavMain.currentSmallSubmenu);
    }
    NavMain.currentSmallSubmenu = null;

    NavMain.smallMenuOpen = false;
};

NavMain.handleSubmenuClick = function(e)
{
    e.preventDefault();
    var menu = $(this).siblings('.submenu');
    NavMain.openSmallSubmenu(menu);
};

NavMain.openSmallSubmenu = function(menu)
{
    // close previous menu
    if ( NavMain.currentSmallSubmenu
        && NavMain.currentSmallSubmenu.get(0).id !== menu.get(0).id) {
        NavMain.closeSmallSubmenu(NavMain.currentSmallSubmenu);
    }

    // skip current menu
    if ( NavMain.currentSmallSubmenu
        && NavMain.currentSmallSubmenu.get(0).id === menu.get(0).id) {
        // still focus first item
        menu.find('a').get(0).focus();
        return;
    }

    menu
        .stop(true)
        .css(
            {
                'left'         : '80px',
                'top'          : 'auto',
                'display'      : 'none',
                'opacity'      : '1',
                'height'       : 'auto',
                'marginTop'    : '-8px',
                'marginBottom' : '0'
            }
        )
        .slideDown(150)
        .attr('aria-expanded', 'true');

    // focus first item
    menu.find('a').get(0).focus();

    NavMain.currentSmallSubmenu = menu;
};

NavMain.closeSmallSubmenu = function(menu)
{
    menu
        .stop(true)
        .fadeOut(100, function() {
        menu
	    .css(
		{
		    'left'         : '',
		    'top'          : '',
		    'display'      : '',
		    'opacity'      : '',
		    'height'       : '',
		    'marginTop'    : '',
		    'marginBottom' : ''
		}
	    )
            .attr('aria-expanded', 'false');
    });
};

$(document).ready(NavMain.init);

})();
