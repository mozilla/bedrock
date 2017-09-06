/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* globals Spinner */

// create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function($) {
    'use strict';

    var SendToDevice = function() {

        this.$widget = $('#send-to-device');
        this.$form = this.$widget.find('#send-to-device-form');
        this.$formFields = this.$form.find('.input');
        this.$input = this.$formFields.find('#id-input');
        this.$thankyou = this.$widget.find('.thank-you');
        this.$errorList = this.$form.find('.error-list');
        this.$sendAnotherLink = this.$form.find('.send-another');
        this.linkPrefix = "mailto:";
        this.linkPostfix = "?subject="+encodeURIComponent(this.$form.data('subject'))+"&body="+this.$form.data('link');
    };

    // static value for user country code
    SendToDevice.COUNTRY_CODE = '';

    SendToDevice.prototype.geoCallback;

    /**
     * Initialise the form messaging and bind events.
     */
    SendToDevice.prototype.init = function() {
        if (this.$widget.length === 1) {
            this.bindEvents();
        }
    };

    /**
     * Binds form submission and click events
     */
    SendToDevice.prototype.bindEvents = function() {
        this.$form.on('submit', $.proxy(this.onFormSubmit, this));
        this.$sendAnotherLink.on('click', $.proxy(this.sendAnother, this));
    };

    /**
     * Remove all form event handlers
     */
    SendToDevice.prototype.unbindEvents = function() {
        this.$form.off('submit');
        this.$sendAnotherLink.off('click');
    };

    /**
     * Show the form again to send another link
     */
    SendToDevice.prototype.sendAnother = function(e) {
        e.preventDefault();
        this.$input.val('');
        this.$errorList.addClass('hidden');
        this.$thankyou.addClass('hidden');
        this.$formFields.removeClass('hidden');
        this.$input.focus();
    };

    /**
     * Enable form fields and hide loading indicator
     */
    SendToDevice.prototype.enableForm = function() {
        this.$input.prop('disabled', false);
        this.$form.removeClass('loading');
    };

    /**
     * Disable form fields and show loading indicator
     */
    SendToDevice.prototype.disableForm = function() {
        this.$input.prop('disabled', true);
        this.$form.addClass('loading');
    };

    /**
     * Reallly primative validation (e.g a@a)
     * matches built-in validation in Firefox
     * @param {email}
     */
    SendToDevice.prototype.checkEmailValidity = function(email) {
        return /\S+@\S+/.test(email);
    };

    /**
     * Handle form submission
     */
    SendToDevice.prototype.onFormSubmit = function(e) {
        e.preventDefault();

        var self = this;
        var action = this.$form.attr('action');
        var formData = this.$form.serialize();

        this.disableForm();

        if (!this.checkEmailValidity(this.$input.val())) {
            this.onFormError(['email']);
            return;
        }
        location.href = this.linkPrefix + this.$input.val() + this.linkPostfix;
        this.onFormSuccess();
    };

    SendToDevice.prototype.onFormSuccess = function() {
        this.$errorList.addClass('hidden');
        this.$formFields.addClass('hidden');
        this.$thankyou.removeClass('hidden');
        this.enableForm();

        // track signup type in GA
        var isEmail = this.checkEmailValidity(this.$input.val());

        window.dataLayer.push({
            'event': 'mailto-device-success',
            'input': 'email-address'
        });
    };

    SendToDevice.prototype.onFormError = function(errors) {
        var errorClass;
        this.$errorList.find('li').hide();
        this.$errorList.removeClass('hidden');

        if ($.inArray('email', errors) !== -1) {
            errorClass = '.email';
        }

        this.$errorList.find(errorClass).show();
        this.enableForm();
    };

    window.Mozilla.SendToDevice = SendToDevice;

})(window.jQuery);
