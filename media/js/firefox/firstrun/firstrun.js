;(function($) {
  'use strict';

  var $video = $('#firstrun-video');

  $video.on('play', function() {
    window.dataLayer.push({
      'event': 'first-run-video-interaction',
      'interaction': 'play'
    });
  }).on('pause', function() {
    // is video over?
    // 'pause' event fires just before 'ended', so
    // using 'ended' results in extra pause tracking.
    var action = ($video[0].currentTime === $video[0].duration) ? 'finish' : 'pause';

    window.dataLayer.push({
      'event': 'first-run-video-interaction',
      'interaction': action
    });
  });

})(window.jQuery);
