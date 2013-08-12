/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function($) {
  'use strict';

  var $w = $(window);

  var isUS = $('html').attr('lang') === 'en-US';

  var isSmallViewport = $w.width() < 760;
  var isTouch = 'ontouchstart' in window || navigator.msMaxTouchPoints || navigator.maxTouchPoints || isSmallViewport;

  var $tabzilla = $('#tabzilla');
  var $masthead = $('#masthead');

  // phone
  var $screen_a = $('#screen-intro .screen');
  var $screen_b = $screen_a.clone();
  var $screen_cur, $screen_next; // for animating/rotating screens

  // signup
  var $signup_content;

  // purchase
  var $get_phone_content;

  // intro background
  var adapt_bg_rotate_interval;
  var $intro_bg_a = $('#intro-bg-a');
  var intro_bg_index = 0;
  var intro_bgs = ['soccer', 'cafe', 'birthday'];
  var $intro_bg_b = $intro_bg_a.clone();

  var nav_height = $masthead.height();

  // adaptive scroll
  var adaptive_text_offset = 200;
  var scene_hooks_top = 620;
  var $soccer_hook = $('#soccer-hook');
  var $cafe_hook = $('#cafe-hook');
  var $bday_hook = $('#birthday-hook');

  // have it all
  var $have_it_all = $('#have-it-all');

  /*
  * Rotating intro background
  */

  function rotateIntroBG () {
    intro_bg_index = ((intro_bg_index + 1) < intro_bgs.length) ? intro_bg_index + 1 : 0;

    var $bg_cur, $bg_next;

    // determine current/next bg
    if ($intro_bg_a.is(':visible')) {
      $bg_cur = $intro_bg_a;
      $bg_next = $intro_bg_b;
    } else {
      $bg_cur = $intro_bg_b;
      $bg_next = $intro_bg_a;
    }

    $bg_next.attr('class', 'intro-bg bg-' + intro_bgs[intro_bg_index]).show();
    $bg_cur.fadeOut(1000, function() {
      $bg_next.css('z-index', 2);
      $bg_cur.css('z-index', 1);
    });

    setTimeout(function () {
      displayPhoneScreen(intro_bg_index);
    }, 100);
  }

  function engageIntroBGRotation() {
    clearInterval(adapt_bg_rotate_interval);
    adapt_bg_rotate_interval = setInterval(function() {
      rotateIntroBG();
    }, 3500);
  }

  function disengageIntroBGRotation() {
    clearInterval(adapt_bg_rotate_interval);
  }

  function initIntroBGRotation() {
    // switch out initial/default screen & bg
    $screen_a.removeClass('screen-birthday').addClass('screen-soccer').attr('data-current', 1);
    $intro_bg_a.removeClass('bg-birthday').addClass('bg-soccer').css('z-index', '2');

    $intro_bg_b.attr('id', 'intro-bg-b').css('z-index', '1').removeClass('bg-soccer');
    $intro_bg_b.insertAfter($intro_bg_a);

    // set up secondary phone screen for rotation
    $screen_b.attr({'id': 'screen-intro-b', 'data-current': 0}).removeClass('screen-birthday').addClass('screen-cafe').insertAfter($screen_a);

    // start intro bg rotation on page load
    engageIntroBGRotation();
  }

  function displayPhoneScreen(bg_index) {
    // determine current/next screen
    if (Number($screen_a.attr('data-current')) === 1) {
      $screen_cur = $screen_a;
      $screen_next = $screen_b;
    } else {
      $screen_cur = $screen_b;
      $screen_next = $screen_a;
    }

    // stop any existing animations
    if ($screen_cur.is(':animated')) {
      $screen_cur.stop();
    }

    if ($screen_next.is(':animated')) {
      $screen_next.stop();
    }

    if (!$screen_cur.hasClass('screen-' + intro_bgs[bg_index])) {
      // update next screen's bg and slide it in
      $screen_next.attr({'class': 'screen screen-' + intro_bgs[bg_index], 'data-current': 1}).animate({
        left: 0
      }, 300);

      // slide current screen out, then place it over to the right
      $screen_cur.attr('data-current', 0).animate({
        left: '-218px'
      }, 300, function() {
        $screen_cur.css('left', '218px');
      });
    } else {
      // make sure screen is visible and set back to 0px left
      $screen_cur.show().animate({
        left: 0
      }, 150);

      // make sure next goes back to the right and gets hidden
      $screen_next.animate({
        left: '218px'
      }, 150);
    }
  }

  function displayAdaptiveBG(bg) {
    // set all to non-active and top level z-index
    $('.adaptive-bg').stop();

    $('.adaptive-bg[data-current="1"]').attr('data-current', 0).css('opacity', 1).addClass('top');

    // set new bg to current, fully visible, and put on bottom of stack
    $('#adaptive-bg-' + bg).attr('data-current', 1).css('opacity', 1).removeClass('top');

    // fade out non-current bg
    $('.adaptive-bg[data-current="0"]').animate({
      'opacity': 0
    }, 350);
  }

  /*
  * Sign up form
  */
  $('.newsletter-signup-toggle').on('click', function(e) {
    e.preventDefault();

    var cta = (this.id === 'signup-toggle-icon') ? 'Sign Me Up - Nav' : 'Sign Me Up - Primary';

    if (!$signup_content) {
      $signup_content = $('#email-form-content').detach();
    }

    Mozilla.Modal.createModal(this, $signup_content, { onDestroy: reattachSignupContent, allowScroll: true });

    //track GA event for newsletter CTA
    trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'click', cta]);
  });

  $('#sign-up-form-close').on('click', function() {
    Mozilla.Modal.closeModal();
  });

  function reattachSignupContent() {
    $('#email-form-wrapper').append($signup_content);
  }

  // reallly primative validation e.g a@a
  // matches built-in validation in Firefox
  function validateEmail(elementValue) {
    var emailPattern = /\S+@\S+/;
    return emailPattern.test(elementValue);
  }

  function validateForm() {
    var $form = $('#footer-email-form');
    var email = $('#id_email').val();
    var $privacy = $('#id_privacy');

    if ('checkValidity' in $form) {
      // do native form validation
      return $form.checkValidity();
    }
    return validateEmail(email) && $privacy.is(':checked');
  }

  $(document).ready(function() {
    // turn off default newsletter JS (from footer-email-form.js) and wire up our own
    $('.newsletter-form').off('submit').on('submit', function(e) {
      e.preventDefault();

      if (validateForm()) {
        var $form = $(this);

        $.ajax({
          url: $form.attr('action'),
          data: $form.serialize(),
          type: 'POST',
          success: function(data) {
            $('#footer-email-form').fadeOut('fast', function() {
              $('#footer-email-thanks').fadeIn('fast');
              setTimeout(function() {
                Mozilla.Modal.closeModal();
              }, 3000);
            });
          },
          error: function() {
            // ??
          }
        });

        //track GA event for newsletter signup
        trackGAEvent(['_trackEvent', 'Newsletter Registration', 'submit', $form.find('input[name="newsletter"]').val()]);
      } else {
        //highlight the required fields
        if (validateEmail($('#id_email').val())) {
          $('input[required]:not([type=email])').addClass('error');
        } else {
          $('input[required]:not(:checked)').addClass('error');
        }
      }
    });
  });

  /*
  * Purchase modal
  */
  $('a[href="#get-phone"]').on('click', function(e) {
    e.preventDefault();

    if (!$get_phone_content) {
      $get_phone_content = $('#get-phone').detach();
    }

    Mozilla.Modal.createModal(this, $get_phone_content, { onDestroy: reattachGetPhoneContent, allowScroll: true });

    //track GA event for get a phone CTA
    trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'click', 'Get a Phone']);
  });

  var reattachGetPhoneContent = function() {
    $('#get-phone-wrapper').append($get_phone_content);
  };

  // toggle sticky masthead when tabzilla is opened/closed
  $tabzilla.on('click', function () {
    var $tab = $('#tabzilla-panel');

    $('#masthead .wrapper').toggleClass('stuck');

    //if we're on mobile then masthead position is relative
    if ($w.width() < 760) { return; }

    if ($tab.hasClass('open')) {
      $tab.css('height', 0);
    }
  });

  /*
   * Sticky masthead navigation
   */
  $masthead.waypoint(function(direction) {
    var $tab = $('#tabzilla-panel');
    var $btn = $('#masthead .cta-button');
    var $current = $('#masthead .curr');
    var $wrapper = $('#masthead .wrapper');

    //don't stick the masthead on mobile viewport
    if ($w.width() < 760) { return; }

    if (direction === 'down') {
      // if tabzilla is open then close if we start to scroll
      if ($tab.hasClass('open')) {
        $tab.css('height', 0);
        $tabzilla.trigger('click');
      }
      $tabzilla.fadeOut('fast');
      $btn.fadeIn();
      $wrapper.animate({backgroundColor: '#fff'}, 'fast');
      $current.promise().done(function () {
        $wrapper.addClass('scroll');
      });
      $('#masthead ul li a').animate({color: '#0096DD'}, 'fast');

    } else {
      $btn.fadeOut('fast');
      $tabzilla.fadeIn();
      $wrapper.animate({backgroundColor: '#D3DAE2'}, 'fast');
      $current.promise().done(function () {
        $wrapper.removeClass('scroll');
      });
      $('#masthead ul li a').animate({color: '##484848'}, 'fast');
    }
  }, { offset: -1 });


  function toggleSharePane () {
    var $share = $('#share-pane');
    var $button = $('#share-pane .share-button');

    $share.toggleClass('open');

    if($share.hasClass('open')) {
      $button.trigger('click').attr('aria-expanded','true');
      $share.attr('aria-expanded','true');
      $share.fadeIn('fast');
    } else {
      $share.attr('aria-expanded','true');
      $share.fadeOut('fast');
      $('#side-nav .share').blur();
    }
  }

  /*
  * Share widget togggle
  */

  $('#side-nav').on('click', '.share', function (e) {
    e.preventDefault();
    toggleSharePane();
  });

  /*
  * Nav scroll
  */

  // tracks click even on nav link, and pauses scroll tracking momentarily
  function navClickGATrack(section_hash) {
    //track GA event for nav clicks
    trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'nav click', section_hash]);

    // do not track while page is flying around
    pause_ga_tracking = true;

    // enable tracking shortly after forcing scroll position
    setTimeout(function() {
      pause_ga_tracking = false;
    }, 600);
  }

  function initNavScroll () {
    // navigation
    var $navs = $('nav[role="navigation"], #ffos-main-logo');
    var $side_nav = $('#side-nav');
    var side_nav_targets = [];

    // handle clicks on any nav element
    $navs.on('click', '.nav', function(e) {
      e.preventDefault();

      // GA track click
      navClickGATrack(this.hash);

      var href = $(this).attr('href');
      var new_scroll = $(href).offset().top;

      // special case for adaptive section
      // text is offset for scrolling, so we want to jump a bit
      // further than the actual anchor
      if (href == '#adaptive-wrapper') {
        new_scroll += adaptive_text_offset;
      }

      $w.scrollTop(new_scroll - nav_height);
    });

    // store possible nav targets in array for easier searching
    $side_nav.find('a').each(function(index, anchor) {
      side_nav_targets.push(anchor.getAttribute('href'));
    });

    // update side/masthead nav when scrolling
    $('.nav-anchor').waypoint(function(direction) {
      $navs.find('a').removeClass('curr');

      if (direction === 'down') {
        $navs.find('a[href="#' + $(this).attr('id') + '"]').addClass('curr');
      } else {
        // find index in nav array of currently scrolled to target
        var cur_target_index = $.inArray('#' + $(this).attr('id'), side_nav_targets);

        // if there's a previous target, update the active navs
        if (cur_target_index > 0) {
          $navs.find('a[href="' + side_nav_targets[cur_target_index - 1] + '"]').addClass('curr');
        }
      }
    }, { offset: nav_height + 1 });
  }

  function initTouchNavScroll() {
    $('nav[role="navigation"], #ffos-main-logo').on('click', '.nav', function(e) {
      e.preventDefault();
      var offset = isSmallViewport ? 0 : nav_height;
      $w.scrollTop($($(this).attr('href')).offset().top - offset);
      navClickGATrack(this.hash);
    });
  }

  function initAdaptiveAppSearchScroller() {
    var $scenes = $('#scenes');
    var bday_hook_height = 520;
    var cafe_hook_height = 920;
    var soccer_hook_height = 1520;
    var controller = $.superscrollorama({ playoutAnimations: false });

    var phone_screen_timeout;
    var phone_screen_timeout_delay = 350;

    var $adaptive_mask = $('#adaptive-mask');
    var $fox_tail_tip = $('#fox-tail-tip');

    // height of hook determines scroll duration (available animation time) for each scene
    $('#scene-hooks').css('top', scene_hooks_top + 'px');
    $soccer_hook.css('height', soccer_hook_height + 'px');
    $cafe_hook.css('height', cafe_hook_height + 'px');
    $bday_hook.css('height', bday_hook_height + 'px');

    var pinDur = soccer_hook_height + cafe_hook_height + bday_hook_height;

    // add scroller-on class for css repositioning, & set total height
    $('#adaptive-wrapper').addClass('scroller-on').css('height', pinDur + 'px');

    // add offset to initial adaptive text (so user doesn't scroll by too fast)
    $('#adaptive-app-search').css('top', adaptive_text_offset + 'px');

    // set height of blue mask covering bottom of adaptive content
    $adaptive_mask.css('height', 620);

    $('#phone-hook').css('position', 'fixed');

    // pin the adaptive background and let rest of content scroll naturally
    controller.pin($('#adaptive-bgs'), pinDur, {
      offset: -(nav_height - 1),
      pushFollowers: false
    });

    // pin the blue mask
    controller.pin($adaptive_mask, pinDur, {
      offset: -(nav_height + 620 - 1),
      pushFollowers: false,
      onPin: function() {
        // make sure we have space for the tail
        if ($w.height() > 744) {
          $fox_tail_tip.animate({
            'bottom': 0
          }, 350);
        }
      },
      onUnpin: function(going_down) {
        // only slide tail down if we're scrolling up
        if (!going_down) {
          $fox_tail_tip.animate({
            'bottom': '-45px'
          }, 350);
        }
      }
    });

    // pin the adaptive features list
    controller.pin($('#adapt2'), pinDur, {
      offset: -nav_height,
      pushFollowers: false
    });

    // toggle background when scrolling up/down from masthead
    $masthead.waypoint(function (dir) {
      if (dir === 'up') {
        engageIntroBGRotation();
        displayAdaptiveBG('birthday');
      } else {
        disengageIntroBGRotation();
        displayAdaptiveBG('birthday');
      }
    }, { offset: -1 });

    // toggle phone screen when scrolling to first adaptive section
    // offset a bit from masthead/bg change above
    $bday_hook.waypoint(function (dir) {
      clearTimeout(phone_screen_timeout);

      if (dir === 'down') {
        phone_screen_timeout = setTimeout(function() {
          displayPhoneScreen(2); // birthday
        }, phone_screen_timeout_delay);
      } else {
        phone_screen_timeout = setTimeout(function() {
          displayPhoneScreen(intro_bg_index); // last bg shown in intro screen
        }, phone_screen_timeout_delay);
      }
    }, { offset: 300 });

    $cafe_hook.waypoint(function (dir) {
      clearTimeout(phone_screen_timeout);

      if (dir === 'down') {
        phone_screen_timeout = setTimeout(function() {
          displayPhoneScreen(1); // birthday
        }, phone_screen_timeout_delay);

        displayAdaptiveBG('cafe');
      } else {
        phone_screen_timeout = setTimeout(function() {
          displayPhoneScreen(2); // birthday
        }, phone_screen_timeout_delay);

        displayAdaptiveBG('birthday');
      }
    }, { offset: -nav_height });

    $soccer_hook.waypoint(function (dir) {
      clearTimeout(phone_screen_timeout);

      if (dir === 'down') {
        phone_screen_timeout = setTimeout(function() {
          displayPhoneScreen(0); // soccer
        }, phone_screen_timeout_delay);

        displayAdaptiveBG('soccer');
      } else {
        phone_screen_timeout = setTimeout(function() {
          displayPhoneScreen(1); // cafe
        }, phone_screen_timeout_delay);

        displayAdaptiveBG('cafe');
      }
    }, { offset: -nav_height });

    // define adaptive features tweens    
    var to_feature_type = TweenMax.to(
      $('#adapt-feature-type'),// element to animate
      1,// duration in seconds
      {
        css: { 'opacity': 1 }// CSS to alter
      }
    );
    var to_feature_results = TweenMax.to($('#adapt-feature-results'), 1, { css: { 'marginTop': 0, 'opacity': 1 } });
    var to_feature_save = TweenMax.to($('#adapt-feature-save'), 1, { css: { 'marginTop': 0, 'opacity': 1 } });
    var to_feature_discover = TweenMax.to($('#adapt-feature-discover'), 1, { css: { 'opacity': 1, 'marginTop': ((isUS) ? '44px' : '0px') } });

    controller.addTween(
      $cafe_hook,// execute tween when this element is visible
      to_feature_type,// tween to execute
      150,// scroll duration (px) of tween
      425// offset of tween (start 425 pixels after $cafe_hook comes in to viewport)
    );
    controller.addTween($cafe_hook, to_feature_results, 150, 700);
    controller.addTween($soccer_hook, to_feature_save, 250, 400);
    controller.addTween($soccer_hook, to_feature_discover, 225, 550);

    // if en-US, show sprites
    if (isUS) {
      var to_blue_line = TweenMax.to($('#adapt-feature-sprite-blue-line'), 1, { css: { 'width': '123px' } });
      var to_orange_line = TweenMax.to($('#adapt-feature-sprite-orange-line'), 1, { css: { 'width': '123px' } });
      var to_feature_plus = TweenMax.to($('#adapt-feature-sprite-plus'), 1, { css: { 'top': '286px', 'opacity': 1 } });

      controller.addTween($cafe_hook, to_blue_line, 250, 400);
      controller.addTween($cafe_hook, to_orange_line, 250, 700);
      controller.addTween($soccer_hook, to_feature_plus, 200, 525);
    }

    // position fox tail tip when have it all comes in to view
    $have_it_all.waypoint(function(dir) {
        if (dir === 'down') {
          $fox_tail_tip.css('position', 'absolute');
        } else {
          $fox_tail_tip.css('position', 'fixed');
        }
      },{ offset: '100%' }
    );

    $('#keep-scrolling').click(function(e) {
      e.preventDefault();

      //track GA event for monitoring if users are clicking on animated scroller
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'click', 'Adaptive animated scroll arrows']);
    });
  }

  function trackGAPageNoScroll () {
    $('#adapt1').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'It adapts, so you can too']);
    });
    $('#adapt2').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Adaptive App Search']);
    });
    $have_it_all.waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Have it All']);
    });
    $('#mission').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Transform the Future']);
    });
  }

  function trackGAPageScroller () {
    $soccer_hook.waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'It adapts, so you can too']);
    });
    $cafe_hook.waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Adaptive App Search (restaurant)']);
    });
    $bday_hook.waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Adaptive App Search (birthday)']);
    });
    $have_it_all.waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Have it All']);
    });
    $('#mission').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Transform the Future']);
    });
  }

  // track clicks on plus sprite (only visible for US on tablet & larger)
  if (isUS && !isSmallViewport) {
    var click_event = (isTouch) ? "touchend" : "click";

    $('#adapt-feature-sprite-plus').on(click_event, function(e) {
      e.preventDefault();
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'click', 'Adaptive sprite plus']);
    });
  }

  // if we have touch or pointer events, use a slider
  // else use scrolling interactions
  if (isTouch) {
    trackGAPageNoScroll();
    initTouchNavScroll();
  } else {
    /*
    * Desktop only fixes/hacks
    */

    // fix for loading page with scroll position > 0 (breaks scrollorama stuff)
    // can't fire immediately, must let browser do it's thing first
    $(function() {
      setTimeout(function() {
        if (window.location.hash === '') {
          if ($w.scrollTop() > 0) {
            $w.scrollTop(0);
          }
        }
      }, 100);
    });

    // refresh page when below 760px only for browsers supporting media queries
    // (spoof responsiveness)
    if (window.matchMedia) {
      var mobile_sized = matchMedia("(max-width: 760px)");
      mobile_sized.addListener(function() {
        window.location.reload();
      });
    }

    /*
    * Desktop interaction
    */

    initIntroBGRotation();
    initAdaptiveAppSearchScroller();
    initNavScroll();
    trackGAPageScroller();
  }
})(jQuery);
