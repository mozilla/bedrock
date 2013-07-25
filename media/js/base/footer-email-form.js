/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {
  var $submit_button = $('#footer-email-form input[type=submit], #help-form input[type=submit]');
  var $form_details = $('#form-details');

  function footer_email_form_show_details(trigger_click) {
    $('#form-details').slideDown('normal', function() {
      if (trigger_click) {
        $submit_button.trigger('click');
      }
    });

    $form_details.slideDown();
  }

  $('#id_email, #id_interest, #footer-email-form select, #footer-email-form input').focus(function () {
    footer_email_form_show_details(false);
  });

  $submit_button.click(function(e) {
    if (!$form_details.is(':visible')) {
      e.preventDefault();
      footer_email_form_show_details(true);
    }
  });

  // reallly primative validation e.g a@a
  // matches built-in validation in Firefox
  function validateEmail(elementValue) {
    var emailPattern = /\S+@\S+/;
    return emailPattern.test(elementValue);
  }

  function validateForm($form) {
    var email = $('#id_email').val();
    var $privacy = $('#id_privacy');

    return validateEmail(email) && $privacy.is(':checked');
  }

  $('.newsletter-form').submit(function (e) {
    var $form = $(this);

    // If the browser has native validation, we know the input is valid
    // because this submit handler won't even be invoked until the input
    // validates.
    if (('checkValidity' in $form) || validateForm($form)) {

      // If there's a name=newsletter input field, we can get the newsletter
      // from that. If not, assume we've got one of the forms that subscribes
      // to the foundation newsletter.
      var $input = $form.children('input[name=newsletter]');
      var newsletter;
      if ($input.length === 0) {
        newsletter = "Registered for Firefox Updates";
      } else {
        newsletter = $input.val();
      }

      if (typeof(gaTrack) === 'function' && newsletter !== '') {
        // Need to wait to submit, until after we're sure we've sent
        // the tracking event to GA.
        e.preventDefault();
        $form.unbind('submit');
        gaTrack(
          ['_trackEvent', 'Newsletter Registration', 'submit', newsletter],
          function (){ $form.submit(); }
        );
      }
    }
    // Else, just let the form submit.
  });
});
