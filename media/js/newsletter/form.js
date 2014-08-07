/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    "use strict";

    var $submit_button = $('.footer-newsletter-form input[type=submit]');
    var $form_details = $('.footer-newsletter-form #form-details');

    function footer_email_form_show_details() {
        if (!$form_details.is(':visible')) {
            $form_details.velocity('slideDown', 'ease-in-out');
        }
    }

    $('.footer-newsletter-form select, .footer-newsletter-form input')
        .on('focus', footer_email_form_show_details);

    $submit_button.on('click', function (e) {
        if (!$form_details.is(':visible')) {
            e.preventDefault();
            footer_email_form_show_details();
        }
    });

    // reallly primative validation e.g a@a
    // matches built-in validation in Firefox
    function validateEmail(elementValue) {
        var emailPattern = /\S+@\S+/;
        return emailPattern.test(elementValue);
    }

    function validateForm($form) {
        var email = $('.footer-newsletter-form #id_email').val();
        var $privacy = $('.footer-newsletter-form #id_privacy');

        return validateEmail(email) && $privacy.is(':checked');
    }

    $('.newsletter-form').on('submit', function track_form_submit(e) {
        var $form = $(this);

        // If the browser has native validation, we know the input is valid
        // because this submit handler won't even be invoked until the input
        // validates.
        if (('checkValidity' in $form) || validateForm($form)) {

            // If there's a name=newsletter input field, we can get the newsletter
            // from that. If not, assume we've got one of the forms that subscribes
            // to the foundation newsletter.
            var $input = $form.children('input[name=newsletters]');
            var newsletter;
            if ($input.length === 0) {
                newsletter = "Registered for Firefox Updates";
            } else {
                newsletter = $input.val();
            }

            if (typeof(gaTrack) === 'function' && newsletter !== '') {
                // Need to wait to submit, until after we're sure we've sent
                // the tracking event to GA.
                e.preventDefault();
                e.stopImmediatePropagation();
                $form.unbind('submit', track_form_submit);
                gaTrack(
                    ['_trackEvent', 'Newsletter Registration', 'submit', newsletter],
                    function () {
                        $form.trigger('submit');
                    }
                );
            }
        }
        // Else, just let the form submit.
    });

    // ajax newsletter forms
    $('#newsletter-form').on('submit', function (e) {
        var $self = $(this);
        e.preventDefault();
        var $errors = $('#footer-email-errors');
        var $errorlist = $errors.find('ul.errorlist');
        var $submitbutton = $('#footer_email_submit');
        var animation_interval;
        $errors.hide();
        $errorlist.empty();
        var old_submit_html = $submitbutton.val();
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
            hwaccel: true, // Whether to use hardware acceleration
        });
        var $spinnerTarget = $('#newsletter-spinner');
        // have to collect data before disabling inputs
        var data = $self.serialize();
        disable_form();
        $.ajax($self.attr('action'), {
            'method': 'post',
            'data': data,
            'dataType': 'json'
        }).done(function (data) {
            if (data.success) {
                var noqueue = {queue: false};
                // enable_form to cancel interval and enable form elements.
                // if page is refreshed and form elements are disabled,
                // they will be disabled after refresh.
                $self.velocity('slideUp', noqueue).velocity('fadeOut', noqueue, enable_form);
                $('#newsletter-form-thankyou').velocity('slideDown', noqueue).velocity('fadeIn', noqueue);
            }
            else if (data.errors) {
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
            $self.find('input,select').prop('disabled', true);
            $submitbutton.addClass('insensitive');
            spinner.spin($spinnerTarget.show()[0]);
        }

        function enable_form() {
            $self.find('input,select').prop('disabled', false);
            $submitbutton.removeClass('insensitive');
            spinner.stop();
            $spinnerTarget.hide();
        }
    });
});
