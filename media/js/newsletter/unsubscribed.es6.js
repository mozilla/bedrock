/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    clearFormErrors,
    errorList,
    disableFormFields,
    enableFormFields,
    postToBasket,
    stripHTML
} from './form-utils.es6';

let _unsubscribedForm;

const UnsubscribedEmailForm = {
    /**
     * Get an array of checked newsletter IDs from the form.
     * @returns {Array}
     */
    getCheckedReasons: () => {
        return Array.from(
            _unsubscribedForm.querySelectorAll(
                '.c-updated-form input[type="checkbox"]:checked'
            )
        ).map((reason) => stripHTML(reason.value));
    },

    /**
     * Get free form textarea input.
     * @returns {String}
     */
    getReasonText: () => {
        const text = _unsubscribedForm.querySelector(
            'textarea[name="reason-text"'
        ).value;
        return stripHTML(text);
    },

    /**
     * Get hidden token field value from the form.
     * @returns  {String}
     */
    getToken: () => {
        return _unsubscribedForm.querySelector('input[name="token"]').value;
    },

    handleFormError: (msg) => {
        let error;

        enableFormFields(_unsubscribedForm);

        _unsubscribedForm
            .querySelector('.mzp-c-form-errors')
            .classList.remove('hidden');

        switch (msg) {
            case errorList.REASON_ERROR:
                error = _unsubscribedForm.querySelector('.error-reason');
                break;
            default:
                error = _unsubscribedForm.querySelector(
                    '.error-try-again-later'
                );
        }

        if (error) {
            error.classList.remove('hidden');
        }
    },

    handleFormSuccess: () => {
        _unsubscribedForm.classList.add('hidden');
        document
            .querySelector('.c-updated-form-thanks')
            .classList.remove('hidden');
    },

    /**
     * Checks that at least one reason has been checked or the
     * textarea has been populated.
     * @returns {Boolean}
     */
    validateFields: () => {
        const reasons = UnsubscribedEmailForm.getCheckedReasons();
        const text = UnsubscribedEmailForm.getReasonText();

        if (reasons.length > 0 || text !== '') {
            return true;
        }

        return false;
    },

    serialize: () => {
        const reasons = UnsubscribedEmailForm.getCheckedReasons();
        const text = UnsubscribedEmailForm.getReasonText();
        const token = UnsubscribedEmailForm.getToken();

        if (text !== '') {
            reasons.push(text);
        }

        // format reasons as a single string with each reason separated by a blank line.
        const reason = reasons.join('\n\n');

        return `token=${encodeURIComponent(token)}&reason=${encodeURIComponent(
            reason
        )}`;
    },

    sendReasons: (e) => {
        e.preventDefault();

        const url = _unsubscribedForm.getAttribute('action');
        const token = UnsubscribedEmailForm.getToken();

        // Disable form fields until POST has completed.
        disableFormFields(_unsubscribedForm);

        // Clear any prior messages that might have been displayed.
        clearFormErrors(_unsubscribedForm);

        // Perform client side form field validation.
        if (!UnsubscribedEmailForm.validateFields()) {
            UnsubscribedEmailForm.handleFormError(errorList.REASON_ERROR);
            return;
        }

        if (token === '') {
            UnsubscribedEmailForm.handleFormError();
            return;
        }

        const params = UnsubscribedEmailForm.serialize();

        postToBasket(
            null,
            params,
            url,
            UnsubscribedEmailForm.handleFormSuccess,
            UnsubscribedEmailForm.handleFormError
        );
    },

    init: () => {
        _unsubscribedForm = document.getElementById('newsletter-updated-form');
        _unsubscribedForm.addEventListener(
            'submit',
            UnsubscribedEmailForm.sendReasons,
            false
        );
    }
};

export default UnsubscribedEmailForm;
