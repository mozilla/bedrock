/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    /*
     * Expand footer email form on input focus or submit if details aren't visible
     */
    function initFooterEmailForm () {
        var $submitButton = $('.footer-newsletter-form input[type=submit]');
        var $formDetails = $('.footer-newsletter-form #form-details');
        var $formDetailsSecondary = $('.footer-newsletter-form .form-details');

        function footerEmailFormShowDetails() {
            if (!$formDetails.is(':visible')) {
                $formDetails.slideDown('normal');
                $formDetailsSecondary.slideDown('normal');
            }
        }

        $('.footer-newsletter-form').on('focus', 'select, input', footerEmailFormShowDetails);

        $submitButton.on('click', function (e) {
            if (!$formDetails.is(':visible')) {
                e.preventDefault();
                footerEmailFormShowDetails();
            }
        });
    }

    initFooterEmailForm();

    /*
     * Reallly primative validation e.g a@a matches built-in validation in Firefox
     * @param string email
     */
    function validateEmail (email) {
        var emailPattern = /\S+@\S+/;
        return emailPattern.test(email);
    }

    /*
     * Validate required form fields are met
     * @param jQuery form object
     */
    function validateForm ($form) {
        var email = $form.find('#id_email').val();
        var $privacy = $form.find('#id_privacy');
        return validateEmail(email) && $privacy.is(':checked');
    }

    /*
     * Get the newsletter name for tracking in GA
     * @param jQuery form object
     */
    function getNewsletterName ($form) {
        var $input = $form.children('input[name=newsletters]');

        // If there's a name=newsletter input field, we can get the newsletter
        // from that. If not, assume we've got one of the forms that subscribes
        // to the foundation newsletter.
        if ($input.length === 0) {
            return "Registered for Firefox Updates";
        }
        return $input.val();
    }

    /*
     * Mozorg newsletter submit does not use ajax as it goes to sendto.mozilla.org
     */
    $('#mozorg-newsletter-form').on('submit', function (e) {
        var $self = $(this);
        var newsletter;

        // If the browser has native validation, we know the input is valid
        // because this submit handler won't even be invoked until the input
        // validates.
        if (('checkValidity' in $self) || validateForm($self)) {

            newsletter = getNewsletterName($self);

            if (typeof(gaTrack) === 'function' && newsletter !== '') {
                // Need to wait to submit, until after we're sure we've sent
                // the tracking event to GA.
                e.preventDefault();
                e.stopImmediatePropagation();
                $self.off('submit');
                gaTrack(['_trackEvent', 'Newsletter Registration', 'submit', newsletter], function () {
                    $self.submit();
                });
            }
        }
        // Else, just let the form submit.
    });

    /*
     * Standard newsletter form uses ajax submission
     */
    $('#newsletter-form').on('submit', function (e) {
        e.preventDefault();

        var $self = $(this);
        var $errors = $('#footer-email-errors');
        var $errorlist = $errors.find('ul.errorlist');
        var $submitbutton = $('#footer_email_submit');
        var $spinnerTarget = $('#newsletter-spinner');
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

        $errors.hide();
        $errorlist.empty();

        // have to collect data before disabling inputs
        var formData = $self.serialize();
        disable_form();

        $.ajax($self.attr('action'), {
            'method': 'post',
            'data': formData,
            'dataType': 'json'
        }).done(function (data) {
            if (data.success) {
                var $thanks = $('#newsletter-form-thankyou');
                var formHeight = $self.css('height');

                // set the min-height of the thank you message
                // to the height of the form to stop page height
                // jumping on success
                $thanks.css('min-height', formHeight);
                $self.hide();

                // enable_form to cancel interval and enable form elements.
                // if page is refreshed and form elements are disabled,
                // they will be disabled after refresh.
                enable_form();

                // show the thank you message
                $thanks.show();

                // track signup in GA
                var newsletter = getNewsletterName($self);
                gaTrack(['_trackEvent', 'Newsletter Registration', 'submit', newsletter]);

            } else if (data.errors) {
                for (var i = 0; i < data.errors.length; i++) {
                    $errorlist.append('<li>' + data.errors[i] + '</li>');
                }
                $errors.show();
                enable_form();
            }
        }).fail(function () {
            // shouldn't need l10n. This should almost never happen.
            $errorlist.append('<li>An unknown error occurred. Please try again later</li>');
            $errors.show();
            enable_form();
        });

        function disable_form() {
            $self.addClass('loading');
            $self.find('input,select').prop('disabled', true);
            $submitbutton.addClass('insensitive');
            spinner.spin($spinnerTarget.show()[0]);
        }

        function enable_form() {
            $self.removeClass('loading');
            $self.find('input,select').prop('disabled', false);
            $submitbutton.removeClass('insensitive');
            spinner.stop();
            $spinnerTarget.hide();
        }
    });
});
