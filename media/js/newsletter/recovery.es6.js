/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { checkEmailValidity } from './form-utils.es6';
let _recoveryForm;

const RecoveryEmailForm = {
    handleFormSuccess: () => {
        document
            .querySelector('.newsletter-recovery-form-fields')
            .classList.add('hide');
        document
            .querySelector('.newsletter-recovery-form-success-msg')
            .classList.add('show');
    },

    handleFormError: (msg) => {
        if (msg && msg === 'Invalid email address') {
            document
                .querySelector('.error-email-invalid')
                .classList.add('show');
        } else if (msg && msg === 'Email address not known') {
            document
                .querySelector('.error-email-not-found')
                .classList.add('show');
        } else {
            document
                .querySelector('.error-try-again-later')
                .classList.add('show');
        }
    },

    clearFormErrors: () => {
        const errorMsgs = document.querySelectorAll('.mzp-c-form-errors');

        for (let i = 0; i < errorMsgs.length; i++) {
            errorMsgs[i].classList.remove('show');
        }
    },

    disableFormFields: () => {
        const formFields = _recoveryForm.querySelectorAll('input, button');

        for (let i = 0; i < formFields.length; i++) {
            formFields[i].disabled = true;
        }
    },

    enableFormFields: () => {
        const formFields = _recoveryForm.querySelectorAll('input, button');

        for (let i = 0; i < formFields.length; i++) {
            formFields[i].disabled = false;
        }
    },

    recoverEmail: (e) => {
        e.preventDefault();

        const email = document.getElementById('id_email').value;
        const params = 'email=' + encodeURIComponent(email);
        const url = _recoveryForm.getAttribute('action');
        const xhr = new XMLHttpRequest();

        // Disable form fields until POST has completed.
        RecoveryEmailForm.disableFormFields();

        // Clear any prior messages that might have been displayed.
        RecoveryEmailForm.clearFormErrors();

        // Really basic client side email validity check.
        if (!checkEmailValidity(email)) {
            RecoveryEmailForm.handleFormError('Invalid email address');
            RecoveryEmailForm.enableFormFields();
            return;
        }

        // Emails used in automation for page-level integration tests
        // should avoid hitting basket directly.
        if (email === 'success@example.com') {
            RecoveryEmailForm.handleFormSuccess();
            return;
        } else if (email === 'failure@example.com') {
            RecoveryEmailForm.handleFormError();
            RecoveryEmailForm.enableFormFields();
            return;
        }

        xhr.onload = (r) => {
            let response = r.target.response || r.target.responseText;

            if (typeof response !== 'object') {
                response = JSON.parse(response);
            }

            if (response) {
                if (
                    response.status === 'ok' &&
                    r.target.status >= 200 &&
                    r.target.status < 300
                ) {
                    RecoveryEmailForm.handleFormSuccess();
                } else if (response.status === 'error' && response.desc) {
                    RecoveryEmailForm.handleFormError(response.desc);
                } else {
                    RecoveryEmailForm.handleFormError();
                }
            } else {
                RecoveryEmailForm.handleFormError();
            }

            RecoveryEmailForm.enableFormFields();
        };

        xhr.onerror = RecoveryEmailForm.handleFormError;
        xhr.open('POST', url, true);
        xhr.setRequestHeader(
            'Content-type',
            'application/x-www-form-urlencoded'
        );
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.timeout = 5000;
        xhr.ontimeout = RecoveryEmailForm.handleFormError;
        xhr.responseType = 'json';
        xhr.send(params);
    },

    init: function () {
        _recoveryForm = document.getElementById('newsletter-recovery-form');
        _recoveryForm.addEventListener(
            'submit',
            RecoveryEmailForm.recoverEmail,
            false
        );
    }
};

export default RecoveryEmailForm;
