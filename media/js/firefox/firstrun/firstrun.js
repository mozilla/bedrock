;(function($) {
  'use strict';

  var $video = $('#firstrun-video');

  var gaq_track = function(category, action, label) {
    if (window._gaq) {
      window._gaq.push(['_trackEvent', category, action, label]);
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
})(window.jQuery);