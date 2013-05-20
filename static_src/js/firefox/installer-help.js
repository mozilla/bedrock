 ;(function($) {
  'use strict';

  var $survey_content = $('#survey-wrapper').show().detach();

  if ($survey_content.length > 0) {
    $('aside.survey').show();
    $('#launch-survey').on('click', function(e) {
      e.preventDefault();
      Mozilla.Modal.createModal(this, $survey_content, {
        allowScroll: false
      });
    });
  }

})(window.jQuery);
