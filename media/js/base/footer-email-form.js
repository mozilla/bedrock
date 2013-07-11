/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {
    function footer_email_form_show_details(trigger_click) {
        $('#form-details').slideDown('normal', function() {
            if (trigger_click) {
                $('#footer-email-form input[type=submit]').trigger('click');
            }
        });

        $('#footer-email-form .form-details').slideDown();
    }

    $('#footer-email-form select, #footer-email-form input').focus(function () {
        footer_email_form_show_details(false);
    });

    $('#footer-email-form input[type=submit]').click(function(e) {
        if (!$('#form-details').is(':visible')) {
            e.preventDefault();
            footer_email_form_show_details(true);
        }
    });

});
