/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FormUtils from '../../newsletter/form-utils.es6';

let form;

const WaitListForm = {
    handleFormError: (msg) => {
        let error;

        FormUtils.enableFormFields(form);

        form.querySelector('.mzp-c-form-errors').classList.remove('hidden');

        switch (msg) {
            case FormUtils.errorList.EMAIL_INVALID_ERROR:
                error = form.querySelector('.error-email-invalid');
                break;
            case FormUtils.errorList.COUNTRY_ERROR:
                error = form.querySelector('.error-select-country');
                break;
            case FormUtils.errorList.LANGUAGE_ERROR:
                error = form.querySelector('.error-select-language');
                break;
            default:
                error = form.querySelector('.error-try-again-later');
        }

        if (error) {
            error.classList.remove('hidden');
        }
    },

    handleFormSuccess: () => {
        const thanks = document.getElementById('newsletter-thanks');
        const newsletter = form.querySelector(
            'input[name="newsletters"]'
        ).value;

        // show thanks message
        form.classList.add('hidden');
        thanks.classList.remove('hidden');
        window.scrollTo(0, 0);

        if (window.dataLayer) {
            window.dataLayer.push({
                event: 'newsletter-signup-success',
                newsletter: newsletter
            });
        }
    },

    validateFields: () => {
        const email = form.querySelector('input[type="email"]').value;
        const countrySelect = form.querySelector('select[name="country"]');
        const lang = form.querySelector('#id_lang').value;

        // Really basic client side email validity check.
        if (!FormUtils.checkEmailValidity(email)) {
            form.handleFormError(FormUtils.errorList.EMAIL_INVALID_ERROR);
            return false;
        }

        // Check for country selection value.
        if (countrySelect && !countrySelect.value) {
            WaitListForm.handleFormError(FormUtils.errorList.COUNTRY_ERROR);
            return false;
        }

        // Check for language selection value.
        if (!lang) {
            WaitListForm.handleFormError(FormUtils.errorList.LANGUAGE_ERROR);
            return false;
        }

        return true;
    },

    serialize: () => {
        // Email address
        const email = encodeURIComponent(
            form.querySelector('input[type="email"]').value
        );

        // Newsletter ID
        const newsletter = form.querySelector(
            'input[name="newsletters"]'
        ).value;

        // Country
        const country = form.querySelector('select[name="country"]').value;

        // Language
        const lang = form.querySelector('select[name="lang"]').value;

        // Source URL (hidden field)
        const sourceUrl = encodeURIComponent(
            form.querySelector('input[name="source_url"]').value
        );

        return `email=${email}&newsletters=${newsletter}&fpn_country=${country}&lang=${lang}&format=H&source_url=${sourceUrl}`;
    },

    newsletterSubscribe: (e) => {
        const email = form.querySelector('input[type="email"]').value;
        const url = form.getAttribute('action');

        e.preventDefault();
        e.stopPropagation();

        // Disable form fields until POST has completed.
        FormUtils.disableFormFields(form);

        // Clear any prior messages that might have been displayed.
        FormUtils.clearFormErrors(form);

        // Perform client side form field validation.
        if (!WaitListForm.validateFields()) {
            return;
        }

        const params = WaitListForm.serialize();

        FormUtils.postToBasket(
            email,
            params,
            url,
            WaitListForm.handleFormSuccess,
            WaitListForm.handleFormError
        );
    },

    init: () => {
        form = document.getElementById('newsletter-form');

        if (!form) {
            return;
        }

        form.addEventListener(
            'submit',
            WaitListForm.newsletterSubscribe,
            false
        );
    }
};

export default WaitListForm;
