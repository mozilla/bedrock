/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Spinner) {

    'use strict';

    var COUNTRY_CODE = '';

    var $main = $('main');

    var $emailForm = $('#newsletter-form');
    var $emailThankYou = $('#newsletter-form-thankyou');
    var $emailInput = $('#id_email');

    /*
     * Initializes the page form based on the user's geo location.
     */
    function initGeoLocation() {
        // should geo.mozilla.org be slow to load for some reason,
        // just show the email form anyway after 5 seconds waiting.
        var formTimeout = setTimeout(showForm, 5000);
        var formLoaded = false;

        $.getScript('//geo.mozilla.org/country.js')
            .done(function(script, textStatus) {
                if (textStatus === 'success') {
                    try {
                        COUNTRY_CODE = geoip_country_code().toLowerCase();
                    } catch (e) {
                        COUNTRY_CODE = '';
                    }
                }
                showForm();
            })
            .fail(function() {
                // something went wrong, show the email form anyway.
                showForm();
            });

        function showForm() {
            clearTimeout(formTimeout);
            // should showForm have already been called, do nothing.
            if (formLoaded) {
                return;
            }
            formLoaded = true;

            // now we're all set, show the form panel.
            $('.tab-container .inner-wrapper').show();

            setNewsletterDefaults();
        }
    }

    function setNewsletterDefaults () {
        var $countryInput = $('#id_country');
        var $countrySelection = $countryInput.find('option[value='+ COUNTRY_CODE +']');
        // if cc is in the country option list, select it
        // remove the default selection first
        if ($countrySelection.length !== 0) {
            $countryInput.find('option:selected').prop('selected', false);
            $countrySelection.prop('selected', true);
        }
    }

    /*
     * Once the user has submitted the email form,
     * it can be shown again via clicking the link in the thank you page.
     */
    $emailThankYou.find('.send-another').on('click', function(e) {
        e.preventDefault();
        $emailInput.val('');
        $emailForm.find('.error').hide();
        $emailThankYou.hide();
        $emailForm.show();
        $emailInput.focus();
    });

    initGeoLocation();

})(window.jQuery, window.Spinner);
