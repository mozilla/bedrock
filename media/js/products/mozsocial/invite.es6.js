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

        // Glean
        if (typeof window.Mozilla.Glean !== 'undefined') {
            window.Mozilla.Glean.pageEvent({
                label: 'newsletter-sign-up-success',
                type: newsletter
            });
        }
    },

    validateFields: () => {
        const email = form.querySelector('input[type="email"]').value;
        const countrySelect = form.querySelector('select[name="country"]');

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

        return true;
    },

    serialize: () => {
        // First name
        const first_name = encodeURIComponent(
            form.querySelector('input[name="first_name"]').value
        );

        // Last name
        const last_name = encodeURIComponent(
            form.querySelector('input[name="last_name"]').value
        );

        // Email address
        const email = encodeURIComponent(
            form.querySelector('input[type="email"]').value
        );

        // Country
        const country = form.querySelector('select[name="country"]').value;

        // Twitter handle
        const twitter = encodeURIComponent(
            form.querySelector('input[name="mozilla_social_twitter_handle"]')
                .value
        );

        // Mastodon handle
        const mastodon = encodeURIComponent(
            form.querySelector('input[name="mozilla_social_mastodon_handle"]')
                .value
        );

        // Newsletter ID
        const newsletter = form.querySelector(
            'input[name="newsletters"]'
        ).value;

        // Source URL (hidden field)
        const sourceUrl = encodeURIComponent(
            form.querySelector('input[name="source_url"]').value
        );

        return `first_name=${first_name}&last_name=${last_name}&email=${email}&country=${country}&mozilla_social_twitter_handle=${twitter}&mozilla_social_mastodon_handle=${mastodon}&newsletters=${newsletter}&format=H&source_url=${sourceUrl}`;
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

WaitListForm.init();
