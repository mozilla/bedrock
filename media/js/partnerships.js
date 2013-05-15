/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function(){
  $sf_form = $('#sf-form');

  $sf_form.validate();

  var scrollup = function() {
    $('html, body').animate({ scrollTop: 0 }, 500);
  };

  $('#sf-form-submit').on('click', function(e) {
    e.preventDefault();

    if ($sf_form.valid()) {
      $.ajax({
        url: $sf_form.attr('action'),
        data: $sf_form.serialize(),
        type: $sf_form.attr('method'),
        dataType: 'text',
        success: function(data, status, xhr) {
          $('#partner-form').fadeOut('fast', function() {
            $('#partner-form-success').css('visibility', 'visible').fadeIn('fast', function() {
              scrollup();
            });
          });
        },
        error: function(xhr, status, error) {
          $('#partner-form-error').css('visibility', 'visible').slideDown('fast', function() {
            scrollup();
          });
        }
      });
    }
  });
});