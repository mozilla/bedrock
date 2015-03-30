/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $sfForm = $('#sf-form');
    var $sfFormSubmit = $('#sf-form-submit');

    var $campaign_type = $('#campaign_type');
    var $typeFields = $('.type-field');
    var $typeInputs = $typeFields.find('input, textarea, select');

    var $country = $('#country');
    var $stateField = $('.state-field');
    var $stateFlydown = $('#state');
    var $provinceField = $('.province-field');

    var $contentFormError = $('#content-form-error');
    var $mainContent = $('#main-content');
    var $htmlBody = $('html, body');

    $sfForm.validate();

    var scrollup = function() {
        $htmlBody.animate({ scrollTop: $mainContent.offset().top }, 500);
    };

    // If Campagin Type is set to "Other", then show the description field

    var campaign_type_other = function() {
        return $campaign_type.val().indexOf('Other') > -1;
        // TODO: Is this an l10n issue?
    };

    var toggleTypeFields = function(activate) {
        if (activate) {
            $typeFields.show();
        } else {
            $typeFields.hide();
        }
    };

    $campaign_type.on('change', function() {
        toggleTypeFields(campaign_type_other());
    });

    // If Country is set to "United States", then hide Prov/Region field
    // and show State field

    var country_is_us = function() {
        return $country.val().indexOf('us') > -1;
    };

    var toggleStateFields = function(activate) {
        if (activate) {
            $stateField.show();
            $provinceField.hide();
        } else {
            $provinceField.show();
            $stateField.hide();
        }
    };

    // If country is not US, do not require State field
    var toggleRequiredState = function(activate) {
        if (activate) {
            $stateFlydown.prop('required', true);
        } else {
            $stateFlydown.removeAttr('required');
        }
    };

    $country.on('change', function() {
        toggleStateFields(country_is_us());
        toggleRequiredState(country_is_us());
    });

    $sfFormSubmit.on('click', function(e) {
        e.preventDefault();

        if ($sfForm.valid()) {
            // if not interested in tiles, clear out the tiles fields
            if (!campaign_type_other()) {
                $typeInputs.val('');
            }

            // if country is US, we can ignore Province/Region
            // if country isn't US, we can ignore State
            if(country_is_us) {
                $provinceField.val('');
            } else {
                $stateField.val('');
            }

            $.ajax({
                url: $sfForm.attr('action'),
                data: $sfForm.serialize(),
                type: $sfForm.attr('method'),
                dataType: 'json',
                success: function(data, status, xhr) {
                    $sfForm.fadeOut('fast', function() {
                        $('#content-form-success').css('visibility', 'visible').fadeIn('fast', function() {
                            scrollup();
                        });
                    });
                },
                error: function(xhr, status, error) {
                    // grab json string from server and convert to JSON obj
                    var json = $.parseJSON(xhr.responseText);
                    Mozilla.FormHelper.displayErrors(json.errors);
                    $contentFormError.css('visibility', 'visible').slideDown('fast', function() {
                        scrollup();
                    });
                }
            });
        }
    });
})(window.jQuery);
