;(function($) {
  'use strict';

  var gaq_track = function(action) {
    if (window._gaq) {
      _gaq.push(['_trackEvent', "first run interaction", action, "First Run Video"]);
    }
  };

  $('#firstrun-video').on('play', function() {
    gaq_track("play");
  }).on('pause', function() {
    gaq_track("pause");
  }).on('ended', function() {
    gaq_track("finish");
  });
})(window.jQuery);