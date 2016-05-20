(function($) {
    'use strict';

    var $message = $('<div id="survey-message"><span class="survey-invite">Hello! Would you be willing to take a minute to answer a few questions for Mozilla?</span><a class="survey-button" href="https://www.surveygizmo.com/s3/2811071/Help-us-by-sharing-your-feedback-about-Mozilla">Sure. I\'ll help.</a></div>');

    $('main').prepend($message);
})(window.jQuery);
