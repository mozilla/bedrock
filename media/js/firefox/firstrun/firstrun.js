;(function($) {
  'use strict';

  var $video = $('#firstrun-video');

  $video.on('play', function() {
    gaTrack(['_trackEvent', 'first run interaction', 'play', 'First Run Video']);
  }).on('pause', function() {
    // is video over?
    // 'pause' event fires just before 'ended', so
    // using 'ended' results in extra pause tracking.
    var action = ($video[0].currentTime === $video[0].duration) ? 'finish' : 'pause';

    gaTrack(['_trackEvent', 'first run interaction', action, 'First Run Video']);
  });
})(window.jQuery);