$(function() {

  var $window       = $(window);
  var $sliderPrime  = $("#story-slider");
  var wide          = false;

  if ($window.width() >= 745) {
    wide = true;
    setupCarousel();
  }

  $window.resize(function() {
    clearTimeout(this.id);
    this.id = setTimeout(doneResizing, 500);
  });

  function doneResizing() {
    if ($window.width() >= 745) {
      wide = true;
      if ( $("#story-slider-clone").length === 0 ) {
        setupCarousel();
      }
    }
    else if ($window.width() < 745) {
      wide = false;
      if ( $("#story-slider-clone").length >= 1 ) {
        removeCarousel();
      }
    }
  };

  // Add the read buttons
  $("button.read").clone().prependTo(".overlay-wrap");

  // Reveal text overlays when hovering over a block
  // @Uses hoverIntent plugin: http://cherne.net/brian/resources/jquery.hoverIntent.html
  $(".overlay-wrap").hoverIntent(
    function() {
      if (wide) {
        var overlayheight = $(this).height() - 80;
        $(this).find(".overlay").stop().hide().css({
          'left' : 'auto',
          'minHeight' : overlayheight
        }).fadeIn(200);
      }
    },
    function() {
      if (wide) {
        $(this).find(".overlay").stop().delay(300).fadeOut(600, function(){
          $(this).removeAttr('style');
        });
      }
    }
  );

  // Reveal overlays when buttons get focus (for keyboard navigation)
  $(".overlay-wrap .read").focus(function() {
    if (wide) {
      $(".overlay[style]").stop().delay(300).fadeOut(600, function(){   // First hide any visible overlays
        $(this).removeAttr('style');                                    // Then reset them to normal (hidden offscreen by CSS)
      });
      var overlayheight = $(this).parents(".overlay-wrap").height() - 80;
      $(this).parents(".overlay-wrap").find(".overlay").hide().css({
        'left' : 'auto',
        'minHeight' : overlayheight
      }).fadeIn(200);
      $('html, body').animate({
        scrollTop: $(this).parents(".overlay-wrap").offset().top -40
      }, 300);
    }
  });


  // Sticky navigation
  var $nav      = $('#page-nav');
  var $head     = $('#masthead');
  var navTop    = $nav.offset();
  var fixed     = false;
  var didScroll = false;

  $window.scroll(function() {
    didScroll = true;
  });

  $(document).ready(function() {
    var scrollTop = $window.scrollTop();
    if ( scrollTop >= navTop.top ) {
      didScroll = true;
    }
  });

  function adjustScrollbar() {
    if (didScroll) {
      didScroll = false;
      var scrollTop = $window.scrollTop();

      if( scrollTop >= navTop.top ) {
        if(!fixed) {
          fixed = true;
          $nav.addClass("fixed");
          $head.css({ "margin-bottom" : "60px" });
        }
      } else {
        if(fixed) {
          fixed = false;
          $nav.removeAttr("class");
          $nav.find("li").removeClass();
          $("#nav-welcome").addClass("current");
          $head.css({ "margin-bottom" : "0" });
        }
      }
    }
  };

  $('#welcome').waypoint(function(event, direction) {
    if(fixed) {
      $nav.attr('class', 'fixed welcome');
      $nav.find("li").removeClass();
      $("#nav-welcome").addClass("current");
    }
  },{
    offset: 60
  });

  $('#mobilized').waypoint(function(event, direction) {
    if(fixed) {
      if (direction == 'down') {
        $nav.attr('class', 'fixed mobilized');
        $nav.find("li").removeClass();
        $("#nav-mobilized").addClass("current");
      }
      else {
        $nav.attr('class', 'fixed welcome');
        $nav.find("li").removeClass();
        $("#nav-welcome").addClass("current");
      }
    }
  },{
    offset: 60
  });

  $('#action').waypoint(function(event, direction) {
    if(fixed) {
      if (direction == 'down') {
        $nav.attr('class', 'fixed action');
        $nav.find("li").removeClass();
        $("#nav-action").addClass("current");
      }
      else {
        $nav.attr('class', 'fixed mobilized');
        $nav.find("li").removeClass();
        $("#nav-mobilized").addClass("current");
      }
    }
  },{
    offset: 60
  });

  $('#community').waypoint(function(event, direction) {
    if(fixed) {
      if (direction == 'down') {
        $nav.attr('class', 'fixed community');
        $nav.find("li").removeClass();
        $("#nav-community").addClass("current");
      }
      else {
        $nav.attr('class', 'fixed action');
        $nav.find("li").removeClass();
        $("#nav-action").addClass("current");
      }
    }
  },{
    offset: 60
  });

  $('#sustainability').waypoint(function(event, direction) {
    if(fixed) {
      if (direction == 'down') {
        $nav.attr('class', 'fixed sustainability');
        $nav.find("li").removeClass();
        $("#nav-sustainability").addClass("current");
      }
      else {
        $nav.attr('class', 'fixed community');
        $nav.find("li").removeClass();
        $("#nav-community").addClass("current");
      }
    }
  },{
    offset: 60
  });


  // Check for an adjusted scrollbar every 100ms.
  setInterval(adjustScrollbar, 100);

  // Bind scrolling to linked element.
  $window.on('click', '#page-nav a[href^="#"]', function(e) {
    e.preventDefault();
    // Extract the target element's ID from the link's href.
    var elem = $(this).attr("href").replace( /.*?(#.*)/g, "$1" );
    $('html, body').animate({
      scrollTop: $(elem).offset().top - 35
    }, 1000, function() {
      $(elem).attr('tabindex','100').focus().removeAttr('tabindex');
    });
  });

  // Load links in new tab/window
  $("a[rel='external']").click( function(e) {
    e.preventDefault();
    window.open(this.href);
  });

  // Load videos in a full-page modal
  $("a.video-play").click( function(e) {
    e.preventDefault();
    var origin = $(this);
    var video = $(this).attr("data-video-source");
    var poster = $(this).children("img").attr("src");
    $('body').addClass("noscroll").append('<div id="fill"><div id="inner"><video id="video" poster="'+poster+'" controls autoplay></video></div></div>');
    $("#video").append(
      '<source src="'+video+'.webm" type="video/webm">'
     +'<source src="'+video+'.mp4" type="video/mp4">'
    ).focus();
    $("#done").clone().appendTo("#inner");
    closeModal();
  });

  // Load the YouTube video in a full-page modal
  $("a.vid-youtube").click( function(e) {
    e.preventDefault();
    var origin = $(this);
    $('body').addClass("noscroll").append('<div id="fill"><div id="inner"><iframe width="640" height="360" src="http://www.youtube-nocookie.com/embed/f_f5wNw-2c0?rel=0" frameborder="0" allowfullscreen></iframe></div></div>');
    $("#inner iframe").focus();
    $("#done").clone().appendTo("#inner");
    closeModal();
  });

  function closeModal() {
    // Remove the full-page modal
    $("#fill #done").click(function() {
      $("#video")[0].pause();
      $("#fill").remove();
      $("body").removeClass("noscroll");
    });
    
    // Esc key removes the modal, too
    $("#fill").keyup(function(e) {
      if (e.keyCode == 27) { // esc
        $("#fill").remove();
        $("body").removeClass("noscroll");
        origin.focus();
      }
    });
  };


  // Set up the contributor stories carousel
  function setupCarousel() {
    $sliderPrime.clone().attr("id", "story-slider-clone").insertAfter($("#video-stage"));
    if ($("#story-vid")[0].paused == false) {
      $("#story-vid")[0].pause();
    }
    $sliderPrime.hide();      

    $("#story-slider-clone").jcarousel({
      scroll: 1,
      visible: 4,
      buttonNextHTML: null,
      buttonPrevHTML: null,
      itemLastOutCallback: { onAfterAnimation: disableButtons },
      itemLastInCallback: { onAfterAnimation: disableButtons },
      initCallback: controlButtons
    });
    
    function controlButtons(carousel) {
      storyPlay();
      // Add the control buttons
      $(".btn-prev, .btn-next").clone().prependTo(".jcarousel-container");
      // Make the buttons work
      $('.btn-next').bind('click', function() {
        carousel.next();
      });
      $('.btn-prev').bind('click', function() {
        carousel.prev();
      });
    };

    // Disable the buttons at the end of the carousel
    function disableButtons(carousel){
      if (carousel.first == 1) {
        $('.btn-prev').attr('disabled','disabled').addClass('disabled');
      } else {
        $('.btn-prev').removeAttr('disabled').removeClass('disabled');
      }
      if (carousel.last == carousel.size()) {
        $('.btn-next').attr('disabled','disabled').addClass('disabled');
      } else {
        $('.btn-next').removeAttr('disabled').removeClass('disabled');
      }
    }
  };

  function removeCarousel() {
    $("#story-slider-clone").parents(".jcarousel-container").remove();
    if ($("#story-vid")[0].paused == false) {
      $("#story-vid")[0].pause();
    }
    $sliderPrime.show();
  };

  // Set up contributor video
  if ($("#story-slider-clone").length > 0) {
    var video   = $("#story-slider-clone").find("a.contributor:first").attr("href");
    var poster  = $("#story-slider-clone").find("a.contributor:first").attr("data-poster");
    var desc    = $("#story-slider-clone").find(".vcard:first .note").html();
    $("#story-vid").attr('poster', poster).attr('src', video);
    $("#video-stage").append('<figcaption>'+desc+'</figcaption>');

    // Add a play button overlay
    $("#video-stage .player").append('<span class="btn-play"></span>');
    $("span.btn-play").click(function(){
      $("#story-vid").attr('controls','controls')[0].play();
      $(this).fadeOut('fast', function(){ $(this).remove(); });
    });
  };

  // Play contributor stories
  function storyPlay() {  
    $("a.contributor").click( function(e) {
      e.preventDefault();
      var video   = $(this).attr("href");
      var poster  = $(this).attr("data-poster");
      var desc    = $(this).find(".note").html();
      
      if ( $("#video-stage").is(":visible") ) { // If the stage exists, play videos on stage
        if ($("#story-vid")[0].paused == false) {
          $("#story-vid")[0].pause();
        }
        if ( $("span.btn-play") ) {
          $("span.btn-play").remove();
        }
        $("#video-stage figcaption").fadeOut('fast', function(){ $(this).html(desc).fadeIn('fast'); });
        $("#story-vid").attr('poster', poster).attr('controls','controls').attr('src', video)[0].play();
        $('html, body').animate({
          scrollTop: $("#video-stage").offset().top - 80
        }, 200, function() {
          $("#story-vid").focus();
        });
      } else { // Else play in a modal
        $('body').addClass("noscroll").append('<div id="fill"><div id="inner"><video id="video" poster="'+poster+'" controls autoplay></video></div></div>');
        $("#video").append(
          '<source src="'+video+'" type="video/webm">'
        ).focus();
        $("#inner").append('<p class="desc">'+desc+'</p>');
        $("#done").clone().appendTo("#inner");
        closeModal();
      };
    });
  };

});

