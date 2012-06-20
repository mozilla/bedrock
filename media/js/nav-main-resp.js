$(document).ready(function() {
  if ($('#nav-main').length === 0) {
    return;
  }

  var main_menuitems = $('#nav-main [tabindex="0"]');
  var prev_li, new_li, focused_item;

  $('#nav-main [role="menubar"] > li').bind('mouseover focusin', function(event) {
    new_li = $(this);
    if (!prev_li || prev_li.attr('id') !== new_li.attr('id')) {
      // Open the menu
      new_li.addClass('hover').find('[aria-expanded="false"]').attr('aria-expanded', 'true');
      if (prev_li) {
        // Close the last selected menu
        prev_li.dequeue();
      }
    } else {
      prev_li.clearQueue();
    }
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
      this.focus(); // Sometimes $(this).focus() doesn"t work
    }).focus(function() {
      focused_item = $(this);
    }).each(function(item_idx) {
      // Enable keyboard navigation
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


  // Set up nav dropdowns
  $("#nav-main .toggle").click(function() {
    if ( $("#nav-main-menu, #nav-main-menu .submenu").is(":visible") ) {
      $("#nav-main-menu, #nav-main-menu .submenu").slideUp(100).attr("aria-hidden", "true");
    }
    else {
      $("#nav-main-menu").slideToggle(150).removeAttr("aria-hidden");
      $("#nav-main-menu .submenu").hide().attr("aria-hidden", "true");
    }
    return false;
  });

  $("#nav-main-menu a[aria-haspopup='true']").click(function() {
    new_foo = $(this);
    if (!prev_foo || prev_foo.attr('id') !== new_foo.attr('id')) {
      // Open the menu
      new_foo.addClass('hover').find('[aria-expanded="false"]').attr('aria-expanded', 'true');
      if (prev_foo) {
        // Close the last selected menu
        prev_foo.dequeue();
      }
    } else {
      prev_foo.clearQueue();
    }

    $("#nav-main-menu .submenu:visible").hide();
    if ( $(this).next(".submenu").is(":visible") ) {
      $(this).next(".submenu").slideUp(100).attr("aria-expanded", "false");
    }
    else {
      $(this).next(".submenu").slideDown(150).attr("aria-expanded", "true");
    }
    return false;
  });

  // Hide dropdowns when anything else is clicked
  $(document).bind('click', function(e) {
    var $clicked = $(e.target);
    if (! $clicked.parents().is("#nav-main") )
      $("#nav-main-menu, #nav-main-menu .submenu").hide().attr("aria-hidden", "true");
      $("#nav-main .toggle").removeClass("open");
  });

  // or gets focus
  $("a, input, textarea, button, :focus").bind('focus', function(e) {
    var $focused = $(e.target);
    if (! $focused.parents().is("#nav-main")) {
      $("#nav-main-menu, #nav-main-menu .submenu").hide().attr("aria-hidden", "true");
      $("#nav-main .toggle").removeClass("open");
    }
  });

  // With JavaScript enabled, we can provide a full navigation with #nav-main.
  // Now "hide" the duplicated #footer-menu from AT.
  $('#footer-menu').attr('role', 'presentation');
});

// Reset menus on resize
$(window).resize(function(){
  $("#nav-main-menu, #nav-main-menu .submenu").removeAttr("style");
});
