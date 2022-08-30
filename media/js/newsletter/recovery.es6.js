/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    checkEmailValidity,
    clearFormErrors,
    disableFormFields,
    enableFormFields,
    postToBasket
} from './form-utils.es6';

let _recoveryForm;

const RecoveryEmailForm = {
    handleFormSuccess: () => {
        document
            .querySelector('.newsletter-recovery-form-fields')
            .classList.add('hidden');
        document
            .querySelector('.newsletter-recovery-form-success-msg')
            .classList.remove('hidden');
    },

    handleFormError: (msg) => {
        enableFormFields(_recoveryForm);

        _recoveryForm
            .querySelector('.mzp-c-form-errors')
            .classList.remove('hidden');

        switch (msg) {
            case 'Invalid email address':
                _recoveryForm
                    .querySelector('.error-email-invalid')
                    .classList.remove('hidden');
                break;
            case 'Email address not known':
                _recoveryForm
                    .querySelector('.error-email-not-found')
                    .classList.remove('hidden');
                break;
            default:
                _recoveryForm
                    .querySelector('.error-try-again-later')
                    .classList.remove('hidden');
        }
    },

    validateFields: () => {
        const email = document.getElementById('id_email').value;

        // Really basic client side email validity check.
        if (!checkEmailValidity(email)) {
            RecoveryEmailForm.handleFormError('Invalid email address');
            enableFormFields(_recoveryForm);
            return false;
        }

        return true;
    },

    recoverEmail: (e) => {
        e.preventDefault();

        const email = document.getElementById('id_email').value;
        const params = 'email=' + encodeURIComponent(email);
        const url = _recoveryForm.getAttribute('action');

        // Disable form fields until POST has completed.
        disableFormFields(_recoveryForm);

        // Clear any prior messages that might have been displayed.
        clearFormErrors(_recoveryForm);

        // Perform client side form field validation.
        if (!RecoveryEmailForm.validateFields()) {
            return;
        }

        postToBasket(
            email,
            params,
            url,
            RecoveryEmailForm.handleFormSuccess,
            RecoveryEmailForm.handleFormError
        );
    },

    init: () => {
        _recoveryForm = document.getElementById('newsletter-recovery-form');
        _recoveryForm.addEventListener(
            'submit',
            RecoveryEmailForm.recoverEmail,
            false
        );
    }
};

export default RecoveryEmailForm;
