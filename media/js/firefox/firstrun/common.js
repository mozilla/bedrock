;(function($) {
  'use strict';

  var $video_container = $('#video-container');
  var $video = $('#pinnedtabs-video');
  var $video_content;
  var video_closing = false;

  if ($('html').hasClass('osx')) {
    $video.attr('src', '//videos-cdn.mozilla.net/serv/drafts/pinnedtabs-mac.webm');
  } else {
    $video.attr('src', '//videos-cdn.mozilla.net/serv/drafts/pinnedtabs-win.webm');
  }

  window.gaq_track = function(category, action, label) {
    if (window._gaq) {
      window._gaq.push(['_trackEvent', category, action, label]);
    }
  };

  // video should be positioned directly over pinned tabs screenshot
  var position_video = function() {
    var pos = $('#pinnedtabs-screenshot').offset();
    var scroll_top = $(window).scrollTop();

    var top = pos.top - scroll_top;
    var left = pos.left;

    $video.css({
      'top': top,
      'left': left
    });

    $('#modal-close').css({
      'top': (top - 16),
      'left': (left + $video.width() - 4)
    });
  };

  var reattach_video = function() {
    // to avoid tracking video pause event fired when modal closes
    if (!$video[0].paused) {
      video_closing = true;
    }
    $video_container.append($video_content);
  };

  $('a[href="#pinnedtabs-video"]').on('click', function(e) {
    e.preventDefault();

    $video_content = $video.detach();

    Mozilla.Modal.createModal(this, $video_content, { onCreate: position_video, onDestroy: reattach_video });

    video_closing = false;

    gaq_track('first run interaction', 'open video', 'Pinned Tabs Video');
  });

  // GA tracking
  $('a.featurelink').on('click', function(e) {
    track_and_redirect(e,
                       ['_trackEvent', 'first run interaction', 'click', $(this).attr('href')],
                       $(this).attr('href'));
  });

  $('.social a').on('click', function(e) {
    track_and_redirect(e,
                       ['_trackEvent', 'social interaction', 'click', $(this).attr('class')],
                       $(this).attr('href'));
  });

  $video.on('play', function() {
    gaq_track("first run interaction", "play", "Pinned Tabs Video");
  }).on('pause', function() {
    // video pause event is fired when modal closes
    // do not track this particular pause event
    if (!video_closing) {
      // is video over?
      // 'pause' event fires just before 'ended', so
      // using 'ended' results in extra pause tracking.
      var action = ($video[0].currentTime === $video[0].duration) ? 'finish' : 'pause';

      gaq_track("first run interaction", action, "Pinned Tabs Video");

      video_closing = false;
    }
  });

})(window.jQuery);
