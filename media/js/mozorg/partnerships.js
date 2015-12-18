/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $sfForm = $('#sf-form');
    var $sfFormSubmit = $('#sf-form-submit');

    var $partnerFormError = $('#partner-form-error');
    var $mainContent = $('#main-content');
    var $htmlBody = $('html, body');

    $sfForm.validate();

    var scrollup = function() {
        $htmlBody.animate({ scrollTop: $mainContent.offset().top }, 500);
    };

    $sfFormSubmit.on('click', function(e) {
        e.preventDefault();

        if ($sfForm.valid()) {
            $.ajax({
                url: $sfForm.attr('action'),
                data: $sfForm.serialize(),
                type: $sfForm.attr('method'),
                dataType: 'json',
                success: function(data, status, xhr) {
                    $('#partner-form').fadeOut('fast', function() {
                        $('#partner-form-success').css('visibility', 'visible').fadeIn('fast', function() {
                            scrollup();
                        });
                    });
                },
                error: function(xhr, status, error) {
                    // grab json string from server and convert to JSON obj
                    var json = $.parseJSON(xhr.responseText);
                    Mozilla.FormHelper.displayErrors(json.errors);
                    $partnerFormError.css('visibility', 'visible').slideDown('fast', function() {
                        scrollup();
                    });
                }
            });
        }
    });
})(window.jQuery);
