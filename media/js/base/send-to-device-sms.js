/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

var Spinner = require('../libs/spin.min.js');

(function () {
    'use strict';

    var SendToDevice = function (id) {
        this.formId = typeof id !== 'undefined' ? id : 'send-to-device';

        this.formLoaded = false;
        this.formTimeout = null;

        this.widget = document.getElementById(this.formId);

        // If there's no widget on the page, do nothing.
        if (!this.widget) {
            return;
        }

        this.form = this.widget.querySelector('.send-to-device-form');
        this.formFields = this.form.querySelector(
            '.send-to-device-form-fields'
        );
        this.input = this.formFields.querySelector('.send-to-device-input');
        this.thankyou = this.widget.querySelectorAll('.thank-you');
        this.errorList = this.form.querySelector('.mzp-c-form-errors');
        this.spinnerTarget = this.form.querySelector('.loading-spinner');
        this.sendAnotherLink = this.form.querySelector('.send-another');
        this.formHeading = this.widget.querySelector('.form-heading');
        this.spinnerColor =
            this.widget.getAttribute('data-spinner-color') || '#000';

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

    /**
     * Initialise the form messaging and bind events.
     */
    SendToDevice.prototype.init = function () {
        if (this.widget) {
            this.formSubmitHandler = this.onFormSubmit.bind(this);
            this.sendAnotherHandler = this.sendAnother.bind(this);
            this.bindEvents();
        }
    };

    /**
     * Binds form submission and click events
     */
    SendToDevice.prototype.bindEvents = function () {
        this.form.addEventListener('submit', this.formSubmitHandler, false);
        this.sendAnotherLink.addEventListener(
            'click',
            this.sendAnotherHandler,
            false
        );
    };

    /**
     * Remove all form event handlers
     */
    SendToDevice.prototype.unbindEvents = function () {
        this.form.removeEventListener('submit', this.formSubmitHandler, false);
        this.sendAnotherLink.removeEventListener(
            'click',
            this.sendAnotherHandler,
            false
        );
    };

    /**
     * Show the form again to send another link
     */
    SendToDevice.prototype.sendAnother = function (e) {
        e.preventDefault();
        this.input.value = '';
        this.errorList.classList.add('hidden');

        for (var i = 0; i < this.thankyou.length; i++) {
            this.thankyou[i].classList.add('hidden');
        }

        if (this.formHeading) {
            this.formHeading.classList.remove('hidden');
        }

        this.formFields.classList.remove('hidden');
        this.input.focus();
    };

    /**
     * Enable form fields and hide loading indicator
     */
    SendToDevice.prototype.enableForm = function () {
        this.input.disabled = false;
        this.form.classList.remove('loading');
        this.spinnerTarget.style.display = 'none';
    };

    /**
     * Disable form fields and show loading indicator
     */
    SendToDevice.prototype.disableForm = function () {
        this.input.disabled = true;
        this.form.classList.add('loading');
        this.spinnerTarget.style.display = 'block';
        this.spinner.spin(this.spinnerTarget);
    };

    /**
     * Validate 10-digit number
     * @param {number}
     */
    SendToDevice.prototype.checkNumberValidity = function (number) {
        var digits = number.replace(/\D/g, ''); // Strip anything not a number
        var digitsTen = /^\d{10}$/; // Check that it's ten digits
        return digitsTen.test(digits);
    };

    /**
     * Helper function to serialize form data for XHR request.
     */
    SendToDevice.prototype.serialize = function () {
        var q = [];
        for (var i = 0; i < this.form.elements.length; i++) {
            var elem = this.form.elements[i];
            if (elem.name) {
                q.push(elem.name + '=' + encodeURIComponent(elem.value));
            }
        }
        var formData = q.join('&');

        return formData;
    };

    /**
     * Handle form submission via XHR
     */
    SendToDevice.prototype.onFormSubmit = function (e) {
        e.preventDefault();

        var self = this;
        var action = this.form.getAttribute('action');
        var formData = this.serialize();

        this.disableForm();

        // perform some basic phone number validation before submitting the form.
        if (!this.checkNumberValidity(this.input.value)) {
            this.onFormError(['number']);
            return;
        }

        var xhr = new XMLHttpRequest();

        xhr.onload = function (r) {
            if (r.target.status >= 200 && r.target.status < 300) {
                var response = r.target.response || r.target.responseText;

                if (typeof response !== 'object') {
                    response = JSON.parse(response);
                }

                if (response.success) {
                    self.onFormSuccess(response.success);
                } else {
                    self.onFormError(response.errors);
                }
            } else {
                self.onFormFailure();
            }
        };

        xhr.onerror = function (e) {
            self.onFormFailure(e);
        };

        xhr.open('POST', action, true);
        xhr.setRequestHeader(
            'Content-type',
            'application/x-www-form-urlencoded'
        );
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.timeout = 5000;
        xhr.ontimeout = self.onFormFailure;
        xhr.responseType = 'json';
        xhr.send(formData);
    };

    SendToDevice.prototype.onFormSuccess = function () {
        this.errorList.classList.add('hidden');
        this.formFields.classList.add('hidden');

        if (this.formHeading) {
            this.formHeading.classList.add('hidden');
        }

        for (var i = 0; i < this.thankyou.length; i++) {
            this.thankyou[i].classList.remove('hidden');
        }

        this.enableForm();

        window.dataLayer.push({
            event: 'send-to-device-success',
            input: 'phone_number'
        });
    };

    SendToDevice.prototype.onFormError = function (errors) {
        var errorClass;
        var errorListItems = this.errorList.querySelectorAll('li');

        for (var i = 0; i < errorListItems.length; i++) {
            errorListItems[i].style.display = 'none';
        }

        this.errorList.classList.remove('hidden');

        if (errors.indexOf('platform', errors) !== -1) {
            errorClass = '.system';
        } else if (errors.indexOf('number', errors) !== -1) {
            errorClass = '.number';
        } else {
            errorClass = '.sms';
        }

        var foundErrors = this.errorList.querySelectorAll(errorClass);

        for (var j = 0; j < foundErrors.length; j++) {
            foundErrors[j].style.display = 'block';
        }

        this.enableForm();
    };

    SendToDevice.prototype.onFormFailure = function () {
        var errorListItems = this.errorList.querySelectorAll('li');

        for (var i = 0; i < errorListItems.length; i++) {
            errorListItems[i].style.display = 'none';
        }

        this.errorList.classList.remove('hidden');

        var foundErrors = this.errorList.querySelectorAll('.system');

        for (var j = 0; j < foundErrors.length; j++) {
            foundErrors[j].style.display = 'block';
        }

        this.enableForm();
    };

    window.Mozilla.SendToDevice = SendToDevice;
})();
