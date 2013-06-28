/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function($) {
  'use strict';

  var $w = $(window);

  var is_us = $('html').attr('lang') === 'en-US';

  var isSmallViewport = $w.width() < 760;

  var $tabzilla = $('#tabzilla');
  var $masthead = $('#masthead');

  // phone
  var $screen = $('#screen-intro');

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

  var nav_height = $('#masthead').height();

  // adaptive scroll
  var scene_hooks_top = 420;
  var $soccer_hook = $('#soccer-hook');
  var $cafe_hook = $('#cafe-hook');
  var $bday_hook = $('#birthday-hook');

  /*
  * Handle hash in URL
  * #adapt{x} hashes are the only trouble makers
  */

  // if hash changes, make sure parallax doesn't go haywire
  function _handle_hash() {
    if (window.location.hash !== '') {
      if (window.location.hash.indexOf('adapt') > -1) {
        setTimeout(function() {
          // make sure hash didn't scroll the adaptive section to the right
          $('#adaptive-app-search').scrollLeft(0);

          // scroll user to #adapt1
          $('html, body').animate({
            scrollTop: scene_hooks_top
          }, 300);
        }, 100);

        // clear out URL hash
        window.location.hash = '';
      }
    } else {
      // force page to the top when refreshing
      if ($w.scrollTop() > 0) {
        $w.scrollTop(0);
      }
    }
  }

  // fix for loading page with hash in URL
  // can't fire immediately, must let browser do it's thing first
  $(function() {
    setTimeout(function() {
      _handle_hash();
    }, 60);
  });

  $w.on('hashchange', function() {
    _handle_hash();
  });

  /*
  * Spoofing responsiveness
  */

  // refresh page when below 760px only for browsers supporting media queries
  if (window.matchMedia) {
    var mobile_sized = matchMedia("(max-width: 760px)");
    mobile_sized.addListener(function() {
      window.location.reload();
    });
  }

  /*
  * Rotating intro background
  */

  function rotate_intro_bg () {
    intro_bg_index = ((intro_bg_index + 1) < intro_bgs.length) ? intro_bg_index + 1 : 0;

    var $cur, $next;

    if ($intro_bg_a.is(':visible')) {
      $cur = $intro_bg_a;
      $next = $intro_bg_b;
    } else {
      $cur = $intro_bg_b;
      $next = $intro_bg_a;
    }

    // transition phone screen
    setTimeout(function() {
      $screen.attr('class', 'screen screen-' + intro_bgs[intro_bg_index]);
    }, 300);

    $next.attr('class', 'intro-bg bg-' + intro_bgs[intro_bg_index]).show();
    $cur.fadeOut(1000, function() {
      $next.css('z-index', 2);
      $cur.css('z-index', 1);
    });
  }

  function engageIntroBGRotation() {
    clearInterval(adapt_bg_rotate_interval);
    adapt_bg_rotate_interval = setInterval(function() {
      rotate_intro_bg();
    }, 3500);
  }

  function disengageIntroBGRotation() {
    clearInterval(adapt_bg_rotate_interval);
  }

  function initIntroBGRotation() {
    // switch out initial/default screen & bg
    $screen.removeClass('screen-birthday').addClass('screen-soccer');
    $intro_bg_a.removeClass('bg-birthday').addClass('bg-soccer').css('z-index', '2');

    $intro_bg_b.attr('id', 'intro-bg-b').css('z-index', '1').removeClass('bg-soccer');
    $intro_bg_b.insertAfter($intro_bg_a);

    // start intro bg rotation on page load
    engageIntroBGRotation();
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

    Mozilla.Modal.create_modal(this, $signup_content, { onDestroy: reattachSignupContent, allowScroll: true });

    //track GA event for newsletter CTA
    trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'click', cta]);
  });

  $('#sign-up-form-close').on('click', function() {
    Mozilla.Modal.close_modal();
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

  $('#footer-email-form').on('submit', function(e) {
    e.preventDefault();

    if (validateForm()) {
      $.ajax({
        // Form action is just an anchor - must prepend current URL for IE.
        url: document.location.href + $(this).attr('action'),
        data: $(this).serialize(),
        type: 'POST',
        success: function(data) {
          $('#footer-email-form').fadeOut('fast', function() {
            $('#footer-email-thanks').fadeIn('fast');
            setTimeout(function() {
              Mozilla.Modal.close_modal();
            }, 3000);
          });
        },
        error: function() {
          // ??
        }
      });
    } else {
      //highlight the required fields
      if (validateEmail($('#id_email').val())) {
        $('input[required]:not([type=email])').addClass('error');
      } else {
        $('input[required]:not(:checked)').addClass('error');
      }
    }
  });

  /*
  * Purchase modal
  */
  $('a[href="#get-phone"]').on('click', function(e) {
    e.preventDefault();

    if (!$get_phone_content) {
      $get_phone_content = $('#get-phone').detach();
    }

    Mozilla.Modal.create_modal(this, $get_phone_content, { onDestroy: reattachGetPhoneContent, allowScroll: true });

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
  $('#masthead').waypoint(function(direction) {
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

      var destination = $(this).attr('href');
      var new_scroll;

      switch (destination) {
        case '#adapt1': // first scene (soccer) of adaptive section
          // animations aren't resetting when forcing scroll to #soccer-hook top position.
          // i don't know why - probably moving too fast for tweens to catch up.
          // works fine forcing to 0, but we don't want that - we want #adapt1 to show up.
          // for some reason, setting the scroll to about 100, then animating the scroll to
          // the top position of #scene-hooks works. it's a little not-perfect, but i'd say
          // good enough.
          new_scroll = 100;

          // excuse me while i pull out my pickaxe
          setTimeout(function() {
            $('html, body').animate({
              scrollTop: scene_hooks_top
            }, 300);
          }, 100);

          break;
        default:
          new_scroll = $($(this).attr('href')).offset().top;
          break;
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
        //var cur_target_index = side_nav_targets.indexOf('#' + $(this).attr('id'));

        // if there's a previous target, update the active navs
        if (cur_target_index > 0) {
          $navs.find('a[href="' + side_nav_targets[cur_target_index - 1] + '"]').addClass('curr');
        }
      }
    }, { offset: nav_height });
  }

  function initTouchNavScroll() {
    $('#nav-main').on('click', 'a', function(e) {
      navClickGATrack(this.hash);
    });
  }

  // if user begins transition into next scene and stops scrolling, force transition to complete
  var tween_previous = 0; // previous progress of executing tween
  var scroll_queued = false; // boolean to know if auto-scroll is queued up
  var scroll_timeout = null; // holds timeout to auto-scroll

  // sets or clears timeout to auto-scroll screen to the specified top position
  function autoAdvanceAdaptiveScene(new_scroll) {
    if (new_scroll === false) {
      clearTimeout(scroll_timeout);
      scroll_queued = false;
    } else {
      if (!scroll_queued) {
        scroll_timeout = setTimeout(function() {
          $('html, body').animate({ scrollTop: new_scroll }, 500);
          scroll_queued = false;
        }, 500);

        scroll_queued = true;
      }
    }
  }

  // called in onUpdate handler in tweens
  function onUpdateHandler(new_scroll, current_tween_progress) {
    // if there's no auto-scroll queued up, check if there should be
    if (!scroll_queued) {
      // is the tween reversing?
      // (my kingdom for an onReverseStart callback. jeez.)
      if (current_tween_progress < tween_previous) {
        autoAdvanceAdaptiveScene(new_scroll);
        tween_previous = 0;
      } else {
        tween_previous = current_tween_progress;
      }
    }
  }

  function initAdaptiveAppSearchScroller() {
    var $adapt_features = $('#adapt-features').detach();
    var $scenes = $('#scenes');
    var soccer_hook_height = 520;
    var cafe_hook_height = 1220;
    var bday_hook_height = 1520;
    var controller = $.superscrollorama({ playoutAnimations: false });

    // height of hook determines scroll duration (available animation time) for each scene
    $('#scene-hooks').css('top', scene_hooks_top + 'px');
    $soccer_hook.css('height', soccer_hook_height + 'px');
    $cafe_hook.css('height', cafe_hook_height + 'px');
    $bday_hook.css('height', bday_hook_height + 'px');

    var pinDur = soccer_hook_height + cafe_hook_height + bday_hook_height + $('#every-moment').height();

    // add scroller-on class for css repositioning, & set total height
    $('#get-firefox-os').addClass('scroller-on').css('height', pinDur + 'px');

    // re-position adative features bullet list in markup
    $adapt_features.insertAfter('#phone-item-intro');

    // pin the ffos section pretty much immediately on page load
    controller.pin($('#adaptive-wrapper'), pinDur, {
      offset: -(nav_height-2), // -2 is for tabzilla top border
      pushFollowers: false
    });

    // define all tweens

    var to_soccer = TweenMax.to(
      $scenes, // element to animate
      1, // duration of animation in seconds
      { // animation parameters
        css: { 'left': '-100%' }, // CSS properties to animate
        onStart: function(tween) {
          autoAdvanceAdaptiveScene(scene_hooks_top + nav_height);
        },
        onComplete: function() { // call when animation completes
          autoAdvanceAdaptiveScene(false);

          disengageIntroBGRotation();

          setTimeout(function() {
            $screen.attr('class', 'screen screen-soccer');
          }, 500);
        },
        onReverseComplete: function() { // call when animation completes reversal
          autoAdvanceAdaptiveScene(false);
          engageIntroBGRotation();
        },
        onUpdate: function() { // call every time animation changes frames
          onUpdateHandler(0, this.totalTime());
        }
    });

    var to_fox_wrapper = TweenMax.to($('#fox-wrapper-intro'), 1, { css: { 'left': '-100%' } });

    var to_cafe = TweenMax.to($scenes, 1, {
      css: { 'left': '-200%' },
      onStart: function() {
        autoAdvanceAdaptiveScene(soccer_hook_height + cafe_hook_height);
      },
      onComplete: function() {
        autoAdvanceAdaptiveScene(false);
        $screen.attr('class', 'screen screen-cafe');
      },
      onReverseComplete: function() {
        autoAdvanceAdaptiveScene(false);
        $screen.attr('class', 'screen screen-soccer');
      },
      onUpdate: function() {
        onUpdateHandler(scene_hooks_top + nav_height, this.totalTime());
      }
    });

    var to_cafe_features = TweenMax.to($adapt_features, 1, {
      css: { 'opacity': 1 },
      onStart: function() {
        $adapt_features.css('display', 'block');
      },
      onReverseComplete: function() {
        $adapt_features.css('display', 'none');
      }
    });

    var to_cafe_blue_line = TweenMax.to($('#adapt-feature-sprite-blue-line'), 1, { css: { 'width': '123px' } });
    var to_cafe_type = TweenMax.to($('#adapt-feature-type'), 1, {
      css: { 'opacity': 1 }
    });
    var to_cafe_orange_line = TweenMax.to($('#adapt-feature-sprite-orange-line'), 1, { css: { 'width': '123px' } });
    var to_cafe_results = TweenMax.to($('#adapt-feature-results'), 1, {
      css: { 'marginTop': 0, 'opacity': 1 }
    });

    var to_bday = TweenMax.to($scenes, 1, {
      css: { 'left': '-300%' },
      onStart: function() {
        autoAdvanceAdaptiveScene(cafe_hook_height + bday_hook_height);
      },
      onComplete: function() {
        autoAdvanceAdaptiveScene(false);
        $screen.attr('class', 'screen screen-birthday');
      },
      onReverseComplete: function() {
        autoAdvanceAdaptiveScene(false);
        $screen.attr('class', 'screen screen-cafe');
      },
      onUpdate: function() {
        onUpdateHandler(soccer_hook_height + cafe_hook_height, this.totalTime());
      }
    });

    var to_bday_save = TweenMax.to($('#adapt-feature-save'), 1, { css: { 'marginTop': 0, 'opacity': 1 } });

    var to_bday_plus = TweenMax.to($('#adapt-feature-sprite-plus'), 1, {
      css: { 'top': '286px', 'opacity': 1 }
    });

    var to_bday_discover = TweenMax.to($('#adapt-feature-discover'), 1, { css: { 'opacity': 1, 'marginTop': ((is_us) ? '44px' : '0px') } });

    controller.addTween(
      $soccer_hook, // trigger animation when this element is scrolled to
      to_soccer, // tween to execute
      200, // duration of animation in pixels
      0 // trigger offset in pixels
    );

    controller.addTween($soccer_hook, to_fox_wrapper, 300, 0);

    controller.addTween($cafe_hook, to_cafe, 200, 0);
    controller.addTween($cafe_hook, to_cafe_features, 200, 80);
    controller.addTween($cafe_hook, to_cafe_type, 150, 425);
    controller.addTween($cafe_hook, to_cafe_results, 150, 700);

    controller.addTween($bday_hook, to_bday, 200, 0);
    controller.addTween($bday_hook, to_bday_save, 250, 400);
    controller.addTween($bday_hook, to_bday_discover, 225, 550);

    // if en-US, show sprites
    if (is_us) {
      controller.addTween($cafe_hook, to_cafe_blue_line, 250, 250);
      controller.addTween($cafe_hook, to_cafe_orange_line, 250, 550);

      controller.addTween($bday_hook, to_bday_plus, 200, 525);
    }

    // position fox tail tip when have it all comes in to view
    $('#have-it-all').waypoint(function(dir) {
        if (dir === 'down') {
          $('#fox-tail-tip').css('position', 'absolute');
        } else {
          $('#fox-tail-tip').css('position', 'fixed');
        }
      },{ offset: '100%' }
    );

    //reset default position if we scroll really fast to top of page (e.g. home key)
    $('#masthead').waypoint(function (dir) {
        if (dir === 'up') {
          $('#scenes').css('left', 0);
        }
      },{ offset: -1 }
    );
  }

  function trackGAPageNoScroll () {
    $('#adapt1').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'It adapts, so you can too']);
    });
    $('#adapt2').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Adaptive App Search']);
    });
    $('#have-it-all').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Have it All']);
    });
    $('#mission').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Transform the Future']);
    });
  }

  function trackGAPageScroller () {
    $('#soccer-hook').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'It adapts, so you can too']);
    });
    $('#cafe-hook').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Adaptive App Search (restaurant)']);
    });
    $('#birthday-hook').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Adaptive App Search (birthday)']);
    });
    $('#have-it-all').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Have it All']);
    });
    $('#mission').waypoint(function () {
      trackGAEvent(['_trackEvent', 'FxOs Consumer Page', 'scroll', 'Transform the Future']);
    });
  }

  // if we have touch or pointer events, use a slider
  // else use scrolling interactions
  if ('ontouchstart' in window || navigator.msMaxTouchPoints || navigator.maxTouchPoints || isSmallViewport) {
    trackGAPageNoScroll();
    initTouchNavScroll();
  } else {
    initIntroBGRotation();
    initNavScroll();
    initAdaptiveAppSearchScroller();
    trackGAPageScroller();
  }
})(jQuery);
