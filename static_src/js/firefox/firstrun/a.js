;(function($) {
  'use strict';

  $('#sticky-nav').waypoint('sticky');

  // Scroll to the linked section
  $(window).on('click', '#sticky-nav a[href^="#"]', function(e) {
    e.preventDefault();

    // Extract the target element's ID from the link's href.
    var elem = $(this).attr("href").replace( /.*?(#.*)/g, "$1" );

    $('html, body').animate({
      scrollTop: $(elem).offset().top - 70
    }, 700, function() {
      $(elem).attr('tabindex','100').focus().removeAttr('tabindex');
    });

    // GA tracking
    window.gaq_track('navigation interaction', 'click', $(this).attr('href'));
  });
})(window.jQuery);