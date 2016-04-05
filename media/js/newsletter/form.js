/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global Spinner */

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
     * Get the newsletter name for tracking in GA
     * @param jQuery form object
     */
    function getNewsletterName ($form) {
        var $input = $form.children('input[name=newsletters]');

        // If there's a name=newsletter input field, we can get the newsletter
        // from that. If not, assume we've got one of the forms that subscribes
        // to the foundation newsletter.
        if ($input.length === 0) {
            return 'Registered for Firefox Updates';
        }
        return $input.val();
    }

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
        disableForm();

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

                // enableForm to cancel interval and enable form elements.
                // if page is refreshed and form elements are disabled,
                // they will be disabled after refresh.
                enableForm();

                // show the thank you message
                $thanks.show();

                // track signup in GA

                var newsletter = getNewsletterName($self);
                window.dataLayer.push({
                    'event': 'newsletter-signup-success',
                    'newsletter': newsletter
                });

            } else if (data.errors) {
                for (var i = 0; i < data.errors.length; i++) {
                    $errorlist.append('<li>' + data.errors[i] + '</li>');
                }
                $errors.show();
                enableForm();
            }
        }).fail(function () {
            // shouldn't need l10n. This should almost never happen.
            $errorlist.append('<li>An unknown error occurred. Please try again later</li>');
            $errors.show();
            enableForm();
        });

        function disableForm() {
            $self.addClass('loading');
            $self.find('input,select').prop('disabled', true);
            $submitbutton.addClass('insensitive');
            spinner.spin($spinnerTarget.show()[0]);
        }

        function enableForm() {
            $self.removeClass('loading');
            $self.find('input,select').prop('disabled', false);
            $submitbutton.removeClass('insensitive');
            spinner.stop();
            $spinnerTarget.hide();
        }
    });
});
