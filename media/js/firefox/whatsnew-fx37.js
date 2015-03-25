/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Spinner) {

    'use strict';

    var COUNTRY_CODE = '';

    var $main = $('main');
    var $smsForm = $('#sms-form');
    var $smsFormHeading = $('.sms-form-wrapper > h3');
    var $smsThankYou = $('#sms-form-thank-you');
    var $smsInput = $('#number');

    var $emailForm = $('#newsletter-form');
    var $emailThankYou = $('#newsletter-form-thankyou');
    var $emailInput = $('#id_email');

    /*
     * Initializes the page form based on the user's geo location.
     * Visitors in the US will be shown both the sms form and the email form.
     * Visitors in all other countries will get only the email form
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

            // if the page visitor is in the US, show the SMS form and set as active.
            // can also append '?geo=us' query param for easier testing/debugging
            if (COUNTRY_CODE === 'us' || window.location.href.indexOf('?geo=us') !== -1) {
                bindFormNavigation();
                $main.attr('data-active', 'sms');
            }
            // now we're all set, show the form panel.
            $('.tab-container .inner-wrapper').show();

            setNewsletterDefaults();
        }
    }

    /*
     * Bind form tabbed navigation
     */
    function bindFormNavigation() {
        var $emailTab = $('#send-email');
        var $smsTab = $('#send-sms');

        $emailTab.attr('aria-selected', false);
        $smsTab.attr('aria-selected', true);

        $('.toggle > ul > li > a').on('click', function(e) {
            e.preventDefault();
            var id = e.target.id;

            if (id === 'tab-sms') {
                $main.attr('data-active', 'sms');
                $emailTab.attr('aria-selected', false);
                $smsTab.attr('aria-selected', true);
            } else if (id === 'tab-email') {
                $main.attr('data-active', 'email');
                $smsTab.attr('aria-selected', false);
                $emailTab.attr('aria-selected', true);
            }
        });

        $emailTab.attr({
            'role': 'tab-panel',
            'aria-labelledby': 'tab-email'
        });

        $smsTab.attr({
            'role': 'tab-panel',
            'aria-labelledby': 'tab-sms'
        });
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
     * SMS form submission
     */
    $smsForm.on('submit', function(e) {
        e.preventDefault();

        var $self = $(this);
        var action = $self.attr('action');
        var formData = $self.serialize();
        var $spinnerTarget = $('#sms-spinner');
        var $smsFormWrapper = $('.sms-form-wrapper');
        var spinner = new Spinner({
            lines: 12, // The number of lines to draw
            length: 4, // The length of each line
            width: 2, // The line thickness
            radius: 4, // The radius of the inner circle
            corners: 0, // Corner roundness (0..1)
            rotate: 0, // The rotation offset
            direction: 1, // 1: clockwise, -1: counterclockwise
            color: '#000', // #rgb or #rrggbb or array of colors
            speed: 1, // Rounds per second
            trail: 60, // Afterglow percentage
            shadow: false, // Whether to render a shadow
            hwaccel: true // Whether to use hardware acceleration
        });

        disableForm();

        $.post(action, formData)
            .done(function(data) {
                enableForm();
                if (data.success) {
                    $smsFormHeading.hide();
                    $self.hide();
                    $smsThankYou.show();
                } else if (data.error) {
                    $self.find('.error').html(data.error).show();
                }
            })
            .fail(function() {
                enableForm();
                $self.find('.error').show();
            });

        function disableForm() {
            $smsFormWrapper.addClass('loading');
            $self.find('input').prop('disabled', true);
            spinner.spin($spinnerTarget.show()[0]);
        }

        function enableForm() {
            $smsFormWrapper.removeClass('loading');
            $self.find('input').prop('disabled', false);
            spinner.stop();
            $spinnerTarget.hide();
        }
    });

    /*
     * Once the user has submitted the SMS form,
     * it can be shown again via clicking the link in the thank you page.
     */
    $smsThankYou.find('.send-another').on('click', function(e) {
        e.preventDefault();
        $smsInput.val('');
        $smsForm.find('.error').hide();
        $smsThankYou.hide();
        $smsFormHeading.show();
        $smsForm.show();
        $smsInput.focus();
    });

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
