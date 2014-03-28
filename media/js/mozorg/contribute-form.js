/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {
    $('#help-form #id_email, #help-form #form-submit').focus(function() {
        $('#help-form .help-form-details').slideDown();
    });

    $('#help-form #id_interest').change(function() {
        $('#help-form .help-form-details').slideDown();
    });
});
