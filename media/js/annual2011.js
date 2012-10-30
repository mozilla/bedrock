$(function(){

  // Reveal text overlays when hovering over a block
  // @Uses hoverIntent plugin: http://cherne.net/brian/resources/jquery.hoverIntent.html
  $(".overlay-wrap").hoverIntent(
    function() {
      var overlayheight = $(this).height() - 80;
      $(this).find(".overlay").stop().hide().css({
        'left' : 'auto',
        'minHeight' : overlayheight
      }).fadeIn(200);
    },
    function() {
      $(this).find(".overlay").stop().delay(300).fadeOut(600, function(){
        $(this).removeAttr('style');
      });
    }
  );

  // Add the read buttons
  $("button.read").clone().prependTo(".overlay-wrap");

  // Reveal overlays when buttons get focus (for keyboard navigation)
  $(".overlay-wrap .read").focus(function() {
    $(".overlay[style]").stop().delay(300).fadeOut(600, function(){   // First hide any visible overlays
      $(this).removeAttr('style');                                    // Then reset them to normal (hidden offscreen by CSS)
    });
    var overlayheight = $(this).parents(".overlay-wrap").height() - 80;;
    $(this).parents(".overlay-wrap").find(".overlay").hide().css({
      'left' : 'auto',
      'minHeight' : overlayheight
    }).fadeIn(200);
    $('html, body').animate({
      scrollTop: $(this).parents(".overlay-wrap").offset().top -40
    }, 300);
  });


  // Scroll the window
  var $window = $(window);
  var $nav = $('#page-nav');
  var $head = $('#masthead');
  var navTop = $nav.offset();
  var fixed = false;
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
          $nav.removeClass("fixed");
          $head.css({ "margin-bottom" : "0" });
        }
      }
    }
  };


  // Check for an adjusted scrollbar every 100ms.
  setInterval(adjustScrollbar, 100);

  // Bind scrolling to linked element.
  $window.on('click', '#page-nav a[href^="#"]', function(e) {
    e.preventDefault();
    // Extract the target element's ID from the link's href.
    var elem = $(this).attr("href").replace( /.*?(#.*)/g, "$1" );
    $('html, body').animate({
        scrollTop: $(elem).offset().top -40
    }, 1000);
  });

  // Load links in new tab/window
  $("a[rel='external']").click( function(e) {
    e.preventDefault();
    window.open(this.href);
  });

  // Load videos in a full-page modal
  $("a.video-play").click( function(e) {
    e.preventDefault();
    var video = $(this).attr("data-video-source");
    var poster = $(this).children("img").attr("src");
    $('body').addClass("noscroll").append('<div id="fill"><div id="inner"><video id="video" poster="'+poster+'" controls autoplay></video></div></div>');
    $("#video").append(
      '<source src="'+video+'.webm" type="video/webm">'
     +'<source src="'+video+'.mp4" type="video/mp4">'
    );
    $("#done").clone().appendTo("#inner");

    // Remove the full-page overlay
    $("#fill #done").click(function() {
      $("#video")[0].pause();
      $("#fill").remove();
      $("body").removeClass("noscroll");
    });
  });

  // Load the YouTube video in a full-page modal
  $("a#vid-kovacsted").click( function(e) {
    e.preventDefault();
    $('body').addClass("noscroll").append('<div id="fill"><div id="inner"><iframe width="640" height="360" src="http://www.youtube-nocookie.com/embed/f_f5wNw-2c0?rel=0" frameborder="0" allowfullscreen></iframe></div></div>');
    $("#done").clone().appendTo("#inner");

    // Remove the full-page overlay
    $("#fill #done").click(function() {
      $("#fill").remove();
      $("body").removeClass("noscroll");
    });
  });

});


