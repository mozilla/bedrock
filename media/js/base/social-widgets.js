$(function() {
  // GA event tracking
  function _track(event, cmd) {
    if (event.target.target === '_blank' || event.metaKey || event.ctrlKey) {
      // New tab
      gaTrack(cmd);
    } else {
      // Current tab
      event.preventDefault();
      gaTrack(cmd, function() { window.location.href = event.currentTarget.href; });
    }
  }

  // Twitter Follow button
  $('.twitter-follow-button').on('click', function(event) {
    _track(event, ['_trackEvent', 'Social Interactions', 'Twitter Follow']);
  });

  // Twitter timeline widget
  $('#twitter-timeline-widget').on('click', 'a', function(event) {
    if ($(this).hasClass('twitter-follow-button')) {
      return; // Tracking will be done by the function above
    }

    _track(event, ['_trackEvent', 'Social Interactions', 'Twitter ' + ({
      'post': 'Post Link Exit',
      'author': 'Author Link Exit',
      'credit': 'Retweet Credit Link Exit',
      'image': 'Preview Image Exit',
      'hash': 'Hashtag Link Exit',
      'mention': 'Mention Link Exit',
      'media': 'Media Link Exit',
      'reply': 'Reply',
      'retweet': 'Retweet',
      'favorite': 'Favorite'
    }[$(this).attr('class')] || 'General Link Exit')]);
  });
});
