/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FormUtils from '../newsletter/form-utils.es6';

const SendToDevice = function (id) {
    this.formId = typeof id !== 'undefined' ? id : 'send-to-device';

    this.formLoaded = false;
    this.formTimeout = null;

    this.widget = document.getElementById(this.formId);

    // If there's no widget on the page, do nothing.
    if (!this.widget) {
        return;
    }

    this.form = this.widget.querySelector('.send-to-device-form');
    this.formFields = this.form.querySelector('.send-to-device-form-fields');
    this.input = this.formFields.querySelector('.send-to-device-input');
    this.thankyou = this.widget.querySelectorAll('.thank-you');
    this.spinnerTarget = this.form.querySelector('.loading-spinner');
    this.sendAnotherLink = this.form.querySelector('.send-another');
    this.formHeading = this.widget.querySelector('.form-heading');
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

    for (let i = 0; i < this.thankyou.length; i++) {
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
};

SendToDevice.prototype.validateFields = function () {
    // Really basic client side email validity check.
    if (!FormUtils.checkEmailValidity(this.input.value)) {
        this.onFormError(FormUtils.errorList.EMAIL_INVALID_ERROR);
        return false;
    }

    return true;
};

/**
 * Handle form submission via XHR
 */
SendToDevice.prototype.onFormSubmit = function (e) {
    e.preventDefault();

    const url = this.form.getAttribute('action');
    const params = FormUtils.serialize(this.form);

    // Disable form fields until POST has completed.
    this.disableForm();

    // Clear any prior messages that might have been displayed.
    FormUtils.clearFormErrors(this.form);

    // Perform client side form field validation.
    if (!this.validateFields()) {
        return;
    }

    FormUtils.postToBasket(
        this.input.value,
        params,
        url,
        this.onFormSuccess.bind(this),
        this.onFormError.bind(this)
    );
};

SendToDevice.prototype.onFormSuccess = function () {
    this.formFields.classList.add('hidden');

    if (this.formHeading) {
        this.formHeading.classList.add('hidden');
    }

    for (let i = 0; i < this.thankyou.length; i++) {
        this.thankyou[i].classList.remove('hidden');
    }

    this.enableForm();

    // GA4
    window.dataLayer.push({
        event: 'send_to_device',
        method: 'email'
    });

    // Glean
    if (typeof window.Mozilla.Glean !== 'undefined') {
        window.Mozilla.Glean.clickEvent({
            id: 'send_to_device',
            type: 'email'
        });
    }
};

SendToDevice.prototype.onFormError = function (msg) {
    let error;

    this.enableForm();

    this.form.querySelector('.mzp-c-form-errors').classList.remove('hidden');

    switch (msg) {
        case FormUtils.errorList.EMAIL_INVALID_ERROR:
            error = this.form.querySelector('.error-email-invalid');
            break;
        default:
            error = this.form.querySelector('.error-try-again-later');
    }

    if (error) {
        error.classList.remove('hidden');
    }
};

export default SendToDevice;
