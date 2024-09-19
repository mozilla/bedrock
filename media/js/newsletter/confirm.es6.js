/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FormUtils from './form-utils.es6';

let _form;

const ConfirmationForm = {
    meetsRequirements: () => {
        return 'Promise' in window;
    },

    handleFormError: (msg) => {
        FormUtils.enableFormFields(_form);
        _form.querySelector('.mzp-c-form-errors').classList.remove('hidden');

        if (msg && msg === FormUtils.errorList.TOKEN_INVALID) {
            _form
                .querySelector('.error-invalid-token')
                .classList.remove('hidden');
        } else if (msg && msg === FormUtils.errorList.UPDATE_BROWSER) {
            _form
                .querySelector('.error-update-browser')
                .classList.remove('hidden');
        } else {
            _form
                .querySelector('.error-try-again-later')
                .classList.remove('hidden');
        }
    },

    handleFormSuccess: () => {
        _form.classList.add('hidden');
        document
            .querySelector('.c-confirm-form-thanks')
            .classList.remove('hidden');
    },

    redirectToRecoveryPage: () => {
        const recoveryUrl = _form.getAttribute('data-recovery-url');

        if (FormUtils.isWellFormedURL(recoveryUrl)) {
            window.location.href = recoveryUrl;
        } else {
            ConfirmationForm.handleFormError();
        }
    },

    getFormActionURL: () => {
        return _form.getAttribute('action');
    },

    serialize: () => {
        const params = FormUtils.serialize(_form);
        const token = FormUtils.getUserToken();

        if (params && token) {
            return `${params}&token=${token}`;
        }

        return '';
    },

    subscribe: (e) => {
        const url = ConfirmationForm.getFormActionURL();

        e.preventDefault();
        e.stopPropagation();

        // Disable form fields until POST has completed.
        FormUtils.disableFormFields(_form);

        // Clear any prior messages that might have been displayed.
        FormUtils.clearFormErrors(_form);

        const params = ConfirmationForm.serialize();

        FormUtils.postToBasket(
            null,
            params,
            url,
            ConfirmationForm.handleFormSuccess,
            ConfirmationForm.handleFormError
        );
    },

    init: () => {
        _form = document.getElementById('confirmation-form');

        if (!ConfirmationForm.meetsRequirements()) {
            ConfirmationForm.handleFormError('Update your browser');
            return;
        }

        _form.addEventListener('submit', ConfirmationForm.subscribe, false);

        // Look for a valid user token before rendering the page.
        // If not found, redirect to /newsletter/recovery/.
        return FormUtils.checkForUserToken().catch(
            ConfirmationForm.redirectToRecoveryPage
        );
    }
};

export default ConfirmationForm;
