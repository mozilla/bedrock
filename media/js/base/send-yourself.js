/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* globals Spinner */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function($) {
    'use strict';

    var SendYourself = function(widgetID) {

        this.formLoaded = false;
        this.formTimeout = null;
        this.smsEnabled = false;

        this.$widget = $('#' + widgetID);
        this.$form = this.$widget.find('.mzp-c-sendyourself-form');
        this.$formFields = this.$form.find('.mzp-c-sendyourself-formfields');
        this.$input = this.$form.find('.mzp-c-sendyourself-input');
        this.$thankyou = this.$widget.find('.mzp-c-sendyourself-thanks');
        this.$errorList = this.$form.find('.mzp-c-form-errors');
        this.$spinnerTarget = this.$form.find('.mzp-js-loading-spinner');
        this.$footerLinks = this.$widget.find('.mzp-c-sendyourself-store-badges');
        this.$sendAnotherLink = this.$form.find('.mzp-js-send-another');
        this.$formHeading = this.$widget.find('.mzp-c-sendyourself-title');
        this.spinnerColor = this.$widget.data('spinnerColor') || '#fff';
        this.countries = this.$widget.data('countries');

        this.spinner = new Spinner({
            lines: 12, // The number of lines to draw
            length: 4, // The length of each line
            width: 2, // The line thickness
            radius: 4, // The radius of the inner circle
            corners: 0, // Corner roundness (0..1)
            rotate: 0, // The rotation offset
            direction: 1, // 1: clockwise, -1: counterclockwise
            color: this.spinnerColor, // #rgb or #rrggbb or array of colors
            speed: 1, // Rounds per second
            trail: 60, // Afterglow percentage
            shadow: false, // Whether to render a shadow
            hwaccel: true // Whether to use hardware acceleration
        });
    };

    // static value for user country code
    SendYourself.COUNTRY_CODE = '';

    SendYourself.prototype.geoCallback; // jshint ignore:line

    /**
     * Initialise the form messaging and bind events.
     */
    SendYourself.prototype.init = function(countryCode) {
        if (this.$widget.length === 1) {
            // if a country code was passed (from an outside geo lookup),
            // store the value and skip any further geo lookups
            if (countryCode) {
                SendYourself.COUNTRY_CODE = countryCode;
            }

            this.getLocation();
            this.bindEvents();
        }
    };

    /**
     * Gets the country code of the location of the user
     * using bedrock's /country-code.json service
     */
    SendYourself.prototype.getLocation = function() {
        var self = this;

        // if a dev has added ?geo=<country code> to the URL
        // we can skip the geo lookup and act as if it worked

        // this will override any countryCode passed in via
        // the init method
        if (window.location.search.indexOf('geo=') !== -1) {
            var urlRe = /geo=([a-z]{2})/i;
            var match = urlRe.exec(window.location.search);
            if (match) {
                SendYourself.COUNTRY_CODE = match[1].toLowerCase();
                self.updateMessaging();
                if (typeof self.geoCallback === 'function') {
                    self.geoCallback(SendYourself.COUNTRY_CODE);
                }
                return;
            }
        }

        // if a country code is already set, skip the geo lookup (but
        // still run the callback)
        if (!SendYourself.COUNTRY_CODE) {
            // should /country-code.json be slow to load,
            // just show the email messaging after 5 seconds waiting.
            this.formTimeout = setTimeout(function() { self.updateMessaging(); }, 5000);

            $.get('/country-code.json')
                .done(function(data) {
                    if (data && data.country_code) {
                        SendYourself.COUNTRY_CODE = data.country_code.toLowerCase();
                    }
                    self.updateMessaging();
                })
                .fail(function() {
                    // something went wrong, show only the email messaging.
                    self.updateMessaging();
                }).always(function() {
                    if (typeof self.geoCallback === 'function') {
                        self.geoCallback(SendYourself.COUNTRY_CODE);
                    }
                });
        } else {
            self.updateMessaging();

            if (typeof self.geoCallback === 'function') {
                self.geoCallback(SendYourself.COUNTRY_CODE);
            }
        }
    };

    /**
     * Returns boolean indication whether or not the user is in a supported country
     */
    SendYourself.prototype.inSupportedCountry = function() {
        var ccode = SendYourself.COUNTRY_CODE;
        return (ccode && this.countries.indexOf('|' + ccode + '|') !== -1);
    };

    /**
     * Checks to update the form messaging based on the users location
     */
    SendYourself.prototype.updateMessaging = function() {
        clearTimeout(this.formTimeout);
        if (!this.formLoaded) {
            this.formLoaded = true;

            // if the page visitor is in a supportec country, show the SMS messaging / copy
            if (this.inSupportedCountry()) {
                this.showSMS();
            }
        }
    };

    /**
     * Updates the form fields to include SMS messaging
     */
    SendYourself.prototype.showSMS = function() {
        var $label = this.$form.find('.mzp-js-input-label');
        this.$form.addClass('mzp-is-sms-country');
        $label.html($label.data('alt'));
        this.$input.attr('placeholder', this.$input.data('alt'));
        this.smsEnabled = true;
    };

    /**
     * Binds form submission and click events
     */
    SendYourself.prototype.bindEvents = function() {
        this.$form.on('submit', $.proxy(this.onFormSubmit, this));
        this.$sendAnotherLink.on('click', $.proxy(this.sendAnother, this));
    };

    /**
     * Remove all form event handlers
     */
    SendYourself.prototype.unbindEvents = function() {
        this.$form.off('submit');
        this.$footerLinks.off('click');
        this.$sendAnotherLink.off('click');
    };

    /**
     * Show the form again to send another link
     */
    SendYourself.prototype.sendAnother = function(e) {
        e.preventDefault();
        this.$input.val('');
        this.$errorList.addClass('mzp-u-hidden');
        this.$thankyou.addClass('mzp-u-hidden');
        this.$formHeading.removeClass('mzp-u-hidden');
        this.$formFields.removeClass('mzp-u-hidden');
        this.$input.trigger('focus');
    };

    /**
     * Enable form fields and hide loading indicator
     */
    SendYourself.prototype.enableForm = function() {
        this.$input.prop('disabled', false);
        this.$form.removeClass('mzp-is-loading');
        this.$spinnerTarget.hide();
    };

    /**
     * Disable form fields and show loading indicator
     */
    SendYourself.prototype.disableForm = function() {
        this.$input.prop('disabled', true);
        this.$form.addClass('mzp-is-loading');
        this.spinner.spin(this.$spinnerTarget.show()[0]);
    };

    /**
     * Really primitive validation (e.g a@a)
     * matches built-in validation in Firefox
     * @param {email}
     */
    SendYourself.prototype.checkEmailValidity = function(email) {
        return /\S+@\S+/.test(email);
    };

    /**
     * Handle form submission via XHR
     */
    SendYourself.prototype.onFormSubmit = function(e) {
        e.preventDefault();

        var self = this;
        var action = this.$form.attr('action');
        var formData = this.$form.serialize();

        this.disableForm();

        // if we know the user has not been prompted to enter an SMS number,
        // perform some basic email validation before submitting the form.
        if (!this.smsEnabled && !this.checkEmailValidity(this.$input.val())) {
            this.onFormError(['email']);
            return;
        }

        if (SendYourself.COUNTRY_CODE) {
            formData += '&country=' + SendYourself.COUNTRY_CODE;
        }

        // else POST and let the server work out whether the input is a
        // valid email address or US phone number.
        $.post(action, formData)
            .done(function(data) {
                if (data.success) {
                    self.onFormSuccess(data.success);
                } else if (data.errors) {
                    self.onFormError(data.errors);
                }
            })
            .fail(function(error) {
                self.onFormFailure(error);
            });
    };

    SendYourself.prototype.onFormSuccess = function() {
        this.$errorList.addClass('mzp-u-hidden');
        this.$formHeading.addClass('mzp-u-hidden');
        this.$formFields.addClass('mzp-u-hidden');
        this.$thankyou.removeClass('mzp-u-hidden');
        this.enableForm();

        // track signup type in GA
        var isEmail = this.checkEmailValidity(this.$input.val());

        window.dataLayer.push({
            'event': 'send-to-device-success',
            'input': isEmail ? 'email-address' : 'phone-number'
        });
    };

    SendYourself.prototype.onFormError = function(errors) {
        var errorClass;
        this.$errorList.find('li').hide();
        this.$errorList.removeClass('mzp-u-hidden');

        if ($.inArray('platform', errors) !== -1) {
            errorClass = '.mzp-js-error-platform';
        } else if (this.smsEnabled && $.inArray('number', errors) !== -1) {
            errorClass = '.mzp-js-error-sms';
        } else {
            errorClass = '.mzp-js-error-email';
        }

        this.$errorList.find(errorClass).show();
        this.enableForm();
    };

    SendYourself.prototype.onFormFailure = function() {
        this.$errorList.find('li').hide();
        this.$errorList.removeClass('mzp-u-hidden');
        this.$errorList.find('.mzp-js-error-system').show();
        this.enableForm();
    };

    window.Mozilla.SendYourself = SendYourself;

})(window.jQuery);
