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
} from '../../newsletter/form-utils.es6';

let form;

const WaitListForm = {
    handleFormError: (msg) => {
        let error;

        enableFormFields(form);

        form.querySelector('.mzp-c-form-errors').classList.remove('hidden');

        switch (msg) {
            case 'Invalid email address':
                error = form.querySelector('.error-email-invalid');
                break;
            case 'Country not selected':
                error = form.querySelector('.error-select-country');
                break;
            case 'Language not selected':
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
        if (!checkEmailValidity(email)) {
            form.handleFormError('Invalid email address');
            return false;
        }

        // Check for country selection value.
        if (countrySelect && !countrySelect.value) {
            WaitListForm.handleFormError('Country not selected');
            return false;
        }

        // Check for language selection value.
        if (!lang) {
            WaitListForm.handleFormError('Language not selected');
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

        // Platform interest selection (optional)
        let platforms = '';
        const hasPlatformInterest = form.querySelector(
            '.vpn-invite-platform-options'
        );

        if (hasPlatformInterest) {
            const checkedPlatforms = document.querySelectorAll(
                'input[name="platforms"]:checked'
            );

            if (checkedPlatforms.length) {
                platforms =
                    '&fpn_platform=' +
                    encodeURIComponent(
                        Array.from(checkedPlatforms)
                            .map(function (platform) {
                                return platform.value;
                            })
                            .join(',')
                    );
            }
        }

        return `email=${email}&newsletters=${newsletter}&fpn_country=${country}&lang=${lang}&format=H&source_url=${sourceUrl}${platforms}`;
    },

    newsletterSubscribe: (e) => {
        const email = form.querySelector('input[type="email"]').value;
        const url = form.getAttribute('action');

        e.preventDefault();
        e.stopPropagation();

        // Disable form fields until POST has completed.
        disableFormFields(form);

        // Clear any prior messages that might have been displayed.
        clearFormErrors(form);

        // Perform client side form field validation.
        if (!WaitListForm.validateFields()) {
            return;
        }

        const params = WaitListForm.serialize();

        postToBasket(
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
