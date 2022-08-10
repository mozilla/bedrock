/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import Spinner from '../libs/spin.min';
import { checkEmailValidity, serialize } from '../newsletter/form-utils.es6';

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
    this.spinner.spin(this.spinnerTarget);
};

/**
 * Handle form submission via XHR
 */
SendToDevice.prototype.onFormSubmit = function (e) {
    e.preventDefault();

    const self = this;
    const action = this.form.getAttribute('action');
    const formData = serialize(this.form);

    this.disableForm();

    // Perform some basic email validation before submitting the form.
    if (!checkEmailValidity(this.input.value)) {
        this.onFormError(['email']);
        return;
    }

    // Emails used in automation for page-level integration tests
    // should avoid hitting basket directly.
    if (this.input.value === 'success@example.com') {
        self.onFormSuccess();
        return;
    } else if (this.input.value === 'failure@example.com') {
        self.onFormError();
        return;
    }

    const xhr = new XMLHttpRequest();

    xhr.onload = function (r) {
        let response = r.target.response || r.target.responseText;

        // Clear any prior messages that might have been displayed.
        self.clearFormErrors();

        if (typeof response !== 'object') {
            response = JSON.parse(response);
        }

        if (response) {
            if (
                response.status === 'ok' &&
                r.target.status >= 200 &&
                r.target.status < 300
            ) {
                self.onFormSuccess();
            } else if (response.status === 'error' && response.desc) {
                self.onFormError(response.desc);
            } else {
                self.onFormError();
            }
        } else {
            self.onFormError();
        }
    };

    xhr.onerror = function (e) {
        self.onFormError(e);
    };

    xhr.open('POST', action, true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.timeout = 5000;
    xhr.ontimeout = self.onFormError;
    xhr.responseType = 'json';
    xhr.send(formData);
};

SendToDevice.prototype.onFormSuccess = function () {
    this.clearFormErrors();
    this.formFields.classList.add('hidden');

    if (this.formHeading) {
        this.formHeading.classList.add('hidden');
    }

    for (let i = 0; i < this.thankyou.length; i++) {
        this.thankyou[i].classList.remove('hidden');
    }

    this.enableForm();

    window.dataLayer.push({
        event: 'send-to-device-success',
        input: 'email-address'
    });
};

SendToDevice.prototype.clearFormErrors = function () {
    const errorMsgs = this.form.querySelectorAll('.mzp-c-form-errors');

    for (let i = 0; i < errorMsgs.length; i++) {
        errorMsgs[i].classList.add('hidden');
    }
};

SendToDevice.prototype.onFormError = function (error) {
    if (error && error === 'Invalid email address') {
        this.form
            .querySelector('.mzp-c-form-errors.email')
            .classList.remove('hidden');
    } else {
        this.form
            .querySelector('.mzp-c-form-errors.system')
            .classList.remove('hidden');
    }

    this.enableForm();
};

export default SendToDevice;
