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

});
