;(function($) {
  'use strict';

  var $video = $('#firstrun-video');

  var gaq_track = function(action) {
    if (window._gaq) {
      _gaq.push(['_trackEvent', "first run interaction", action, "First Run Video"]);
    }
  };

  $video.on('play', function() {
    gaq_track("play");
  }).on('pause', function() {
    // is video over?
    // 'pause' event fires just before 'ended', so
    // using 'ended' results in extra pause tracking.
    var action = ($video[0].currentTime === $video[0].duration) ? 'finish' : 'pause';

    gaq_track(action);
  });
})(window.jQuery);