;(function($) {
  'use strict';

  var $video = $('#firstrun-video');

  var gaq_track = function(category, action, label) {
    if (window._gaq) {
      _gaq.push(['_trackEvent', category, action, label]);
    }
  };

  $video.on('play', function() {
    gaq_track("play");
  }).on('pause', function() {
    // is video over?
    // 'pause' event fires just before 'ended', so
    // using 'ended' results in extra pause tracking.
    var action = ($video[0].currentTime === $video[0].duration) ? 'finish' : 'pause';

    gaq_track('first run interaction', action, 'First Run Video');
  });

  $('#footer_email_submit').on('click', function(e) {
    // if form is valid, delay submission to wait for GA tracking
    if ($('#footer-email-form')[0].checkValidity()) {
      e.preventDefault();

      gaq_track("Newsletter Registration", "submit", "Registered for Firefox Updates");

      setTimeout(function() {
        $('#footer-email-form').submit();
      }, 500);
    }
  });
})(window.jQuery);