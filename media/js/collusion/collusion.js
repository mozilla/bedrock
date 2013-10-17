/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function(){
    $("#updates").validate({
      errorPlacement: function(error, element) {
        $element = $(element);

        if ($element.attr('id') == 'privacy-check') {
          error.appendTo($('#privacy-field'));
        } else {
          error.appendTo($('#email-wrapper'));
        }
      }
    });
});