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
      $(this).addClass("hover");
    },
    function() {
      $(this).find(".overlay").stop().delay(300).fadeOut(600, function(){ 
        $(this).removeAttr('style');
        $(this).parents(".overlay-wrap").removeClass("hover");
      });
    }
  );
  
  // Add the read buttons
  $("button.read").clone().appendTo(".overlay-wrap");
  
  // Reveal overlays when buttons get focus (for keyboard navigation)  
  $(".overlay-wrap .read").focus(function() {
    var overlayheight = $(this).height() - 80;
    $(this).parents(".overlay-wrap").find(".overlay").hide().css({ 
      'left' : 'auto', 
      'minHeight' : overlayheight 
    }).fadeIn(200);
  });
  
  // Hide overlays when button loses focus
  $(".overlay-wrap .read").blur(function() {
    $(this).parents(".overlay-wrap").find(".overlay").delay(300).fadeOut(600, function(){ 
      $(this).parents(".overlay-wrap").find(".overlay").removeAttr('style'); 
    });
  });
  
  // Load entire block into a full-page overlay, prevent scrolling on the body
  $(".has-overlay .read").click(function() {
    var content = $(this).parents(".has-overlay").clone();
    $(this).parents(".has-overlay").find(".overlay").hide( function(){ 
      $(this).removeAttr('style'); 
    } );
    $('body').addClass("noscroll").append('<div id="fill"><div id="inner"></div></div>');
    content.removeClass("has-overlay").appendTo("#inner");
    content.find(".overlay").removeAttr("style");
    $("#inner").focus();
    $("#done").clone().appendTo("#inner");
    
    // Remove the full-page overlay  
    $("#fill #done").click(function() {
      $("#fill").remove();
      $("body").removeClass("noscroll");
    });
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

  // Check for an adjusted scrollbar every 250ms.
  setInterval(adjustScrollbar, 250);

  // Bind scrolling to linked element.
  $window.on('click', '#page-nav a[href^="#"]', function(e) {
    e.preventDefault();
    // Extract the target element's ID from the link's href.
    var elem = $(this).attr("href").replace( /.*?(#.*)/g, "$1" );
    $('html, body').animate({
        scrollTop: $(elem).offset().top -40
    }, 1000);
  });

/*
  // Load videos in a full-screen modal
  $window.on('click', 'a.video-play', function(e) {
    e.preventDefault();
    
    var video = $(this).attr("href");
    var poster = $(this).children("img").attr("src");
    $('body').addClass("noscroll").append('<div id="fill"><div id="inner"><video id="video" poster="'+poster+'" src="'+video+'" controls></div></div>');
    $("#video")[0].play();
    $("#done").clone().appendTo("#inner");
    
    // Remove the full-page overlay  
    $("#fill #done").click(function() {
      $("#video")[0].pause();
      $("#fill").remove();
      $("body").removeClass("noscroll");
    });
  });
*/

});
