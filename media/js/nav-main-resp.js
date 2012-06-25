/* vim: set expandtab tabstop=2 shiftwidth=2 softtabstop=2: */

$(document).ready(function() {

  // If there's no nav-main element, don't initialize the menu.
  if ($('#nav-main').length === 0) {
    return;
  }

  var main_menuitems = $('#nav-main ul [tabindex="0"]');
  var prev_li, new_li, focused_item;

  $('#nav-main [role="menubar"] > li').bind('mouseover focusin', function(event) {
    new_li = $(this);

    if (prev_li) {
      if (prev_li.attr('id') !== new_li.attr('id')) {
        // Close the last selected menu
        prev_li.dequeue();
      } else {
        prev_li.clearQueue();
      }
    }

    // Open the menu
    new_li.addClass('hover').find('[aria-expanded="false"]').attr('aria-expanded', 'true');
  }).bind('mouseout focusout', function(event) {

    prev_li = $(this);
    prev_li.delay(100).queue(function() {
      if (prev_li) {
        prev_li.clearQueue();
        // Close the menu
        prev_li.removeClass('hover').find('[aria-expanded="true"]').attr('aria-expanded', 'false');
        prev_li = null;
        if (focused_item) {
          focused_item.get(0).blur();
        }
      }
    });

  }).each(function(menu_idx) {
    var menu = $(this).find('[role="menu"]');
    var menuitems = $(this).find('a');

    menuitems.mouseover(function(event) {
      this.focus(); // Sometimes $(this).focus() doesn't work
    }).focus(function() {
      focused_item = $(this);
    }).each(function(item_idx) {
      $(this).keydown(function(event) {
        var target;
        switch (event.keyCode) {
          case 33: // Page Up
          case 36: // Home
            target = menuitems.first();
            break;

          case 34: // Page Down
          case 35: // End
            target = menuitems.last();
            break;

          case 38: // Up
            target = (item_idx > 0) ? menuitems.eq(item_idx - 1)
                                    : menuitems.last();
            break;

          case 40: // Down
            target = (item_idx < menuitems.length - 1) ? menuitems.eq(item_idx + 1)
                                                       : menuitems.first();
            break;

          case 37: // Left
            target = (menu_idx > 0) ? main_menuitems.eq(menu_idx - 1)
                                    : main_menuitems.last();
            break;

          case 39: // Right
            target = (menu_idx < main_menuitems.length - 1) ? main_menuitems.eq(menu_idx + 1)
                                                            : main_menuitems.first();
            break;
        }
        if (target) {
          target.get(0).focus(); // Sometimes target.focus() doesn't work
          return false;
        }
        return true;
      });
    });
  });

  var NavMain = {};

  /**
   * Whether or not min/max width media queries are supported in CSS
   *
   * If not supported, the small mode is never triggered.
   *
   * @var Boolean
   */
  NavMain.hasMediaQueryWidths = (function() {
    return !(/MSIE\ (4|5|6|7|8)/.test(navigator.userAgent));
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

  NavMain.init = function()
  {
    NavMain.mainMenuItems = $('#nav-main [role="menubar"] > li');
    NavMain.mainMenuLinks = $('#nav-main [role="menubar"] > li > [tabindex="0"]');

    if (NavMain.hasMediaQueryWidths) {
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

  NavMain.toggleSmallMenu = function()
  {
    if (NavMain.smallMenuOpen) {
      NavMain.closeSmallMenu();
    } else {
      NavMain.openSmallMenu();
    }
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

      $('#nav-main-menu').attr('aria-hidden', 'true');

      $(document).click(NavMain.handleDocumentClick);
      $('a, input, textarea, button, :focus')
        .focus(NavMain.handleDocumentFocus);

      NavMain.smallMode = true;
      console.log('small');
  };

  NavMain.leaveSmallMode = function()
  {
      NavMain.relinkMainMenuLinks();

      $('#nav-main-menu').removeAttr('aria-hidden');

      $(document).unbind('click', NavMain.handleDocumentClick);
      $('a, input, textarea, button, :focus')
        .unbind('focus', NavMain.handleDocumentFocus);

      NavMain.smallMode = false;
      NavMain.smallMenuOpen = false;
      console.log('big');
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

  NavMain.openSmallMenu = function()
  {
    if (NavMain.smallMenuOpen) {
      return;
    }

    $('#nav-main-menu')
      .slideToggle(150)
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

  NavMain.handleSubmenuClick = function(e)
  {
    e.preventDefault();
    var menu = $(this).siblings('.submenu');
    NavMain.openSmallSubmenu(menu);
  };

  NavMain.handleToggleKeypress = function(e)
  {
    if (e.keyCode == 13) {
      NavMain.toggleSmallMenu();
    }
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
          'top'          : '0',
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
        .css('left', '-999em')
        .css('top', '0')
        .attr('aria-expanded', 'false');
    });
  };


  NavMain.init();

});
