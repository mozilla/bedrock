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


  // Show the download survey to 1% of visitors
  var $survey_content = $('#survey-wrapper').show().detach();

  if ($survey_content.length > 0) {
    var surveyProbability = 0.01;
    var showSurvey = (Math.random() < surveyProbability) ? 'yes' : 'no';

    if (showSurvey === 'yes') {
      $('p.survey').show();
      $('#launch-survey').on('click', function(e) {
        e.preventDefault();
        Mozilla.Modal.createModal(this, $survey_content, {
          allowScroll: false
        });
      });
    }

  }

})(window.jQuery);
