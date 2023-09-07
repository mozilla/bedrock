/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FormUtils from './form-utils.es6';

let form;

const NewsletterForm = {
    handleFormError: (msg) => {
        let error;

        FormUtils.enableFormFields(form);

        form.querySelector('.mzp-c-form-errors').classList.remove('hidden');

        switch (msg) {
            case FormUtils.errorList.EMAIL_INVALID_ERROR:
                error = form.querySelector('.error-email-invalid');
                break;
            case FormUtils.errorList.NEWSLETTER_ERROR:
                form.querySelector(
                    '.error-newsletter-checkbox'
                ).classList.remove('hidden');
                break;
            case FormUtils.errorList.COUNTRY_ERROR:
                error = form.querySelector('.error-select-country');
                break;
            case FormUtils.errorList.LANGUAGE_ERROR:
                error = form.querySelector('.error-select-language');
                break;
            case FormUtils.errorList.PRIVACY_POLICY_ERROR:
                error = form.querySelector('.error-privacy-policy');
                break;
            case FormUtils.errorList.LEGAL_TERMS_ERROR:
                error = form.querySelector('.error-terms');
                break;
            default:
                error = form.querySelector('.error-try-again-later');
        }

        if (error) {
            error.classList.remove('hidden');
        }
    },

    handleFormSuccess: () => {
        const newsletters = Array.from(
            document.querySelectorAll("input[name='newsletters']:checked")
        ).map((newsletter) => newsletter.value);

        form.classList.add('hidden');
        document.getElementById('newsletter-thanks').classList.remove('hidden');

        if (window.dataLayer) {
            // UA
            window.dataLayer.push({
                event: 'newsletter-signup-success',
                newsletter: newsletters
            });
            // GA4
            for (let i = 0; i < newsletters.length; ++i) {
                window.dataLayer.push({
                    event: 'newsletter_subscribe',
                    newsletter_id: newsletters[i]
                });
            }
        }

        // Glean
        if (typeof window.Mozilla.Glean !== 'undefined') {
            window.Mozilla.Glean.pageEvent({
                label: 'newsletter-sign-up-success',
                type: newsletters.join(', ')
            });
        }
    },

    serialize: () => {
        // Email address
        const email = encodeURIComponent(
            form.querySelector('input[type="email"]').value
        );

        // Newsletter format
        const format = form.querySelector('input[name="format"]:checked').value;

        // Country (optional form <select>)
        const countrySelect = form.querySelector('select[name="country"]');
        const country = countrySelect ? `&country=${countrySelect.value}` : '';

        // Language (get by DOM ID as field can be <input> or <select>)
        const lang = form.querySelector('#id_lang').value;

        // Selected newsletter(s)
        let newsletters = Array.from(
            form.querySelectorAll('input[name="newsletters"]:checked')
        )
            .map((newsletter) => {
                return `${newsletter.value}`;
            })
            .join(',');
        newsletters = encodeURIComponent(newsletters);

        // Source URL (hidden field)
        const sourceUrl = encodeURIComponent(
            form.querySelector('input[name="source_url"]').value
        );

        return `email=${email}&format=${format}${country}&lang=${lang}&source_url=${sourceUrl}&newsletters=${newsletters}`;
    },

    validateFields: () => {
        const email = form.querySelector('input[type="email"]').value;
        const privacy = form.querySelector('input[name="privacy"]:checked')
            ? true
            : false;
        const newsletters = form.querySelectorAll(
            'input[name="newsletters"]:checked'
        );
        const countrySelect = form.querySelector('select[name="country"]');
        const lang = form.querySelector('#id_lang').value;
        const terms = form.querySelector('input[name="terms"]');

        // Really basic client side email validity check.
        if (!FormUtils.checkEmailValidity(email)) {
            NewsletterForm.handleFormError(
                FormUtils.errorList.EMAIL_INVALID_ERROR
            );
            return false;
        }

        // Check for country selection value.
        if (countrySelect && !countrySelect.value) {
            NewsletterForm.handleFormError(FormUtils.errorList.COUNTRY_ERROR);
            return false;
        }

        // Check for language selection value.
        if (!lang) {
            NewsletterForm.handleFormError(FormUtils.errorList.LANGUAGE_ERROR);
            return false;
        }

        // Confirm at least one newsletter is checked
        if (newsletters.length === 0) {
            NewsletterForm.handleFormError(
                FormUtils.errorList.NEWSLETTER_ERROR
            );
            return false;
        }

        // Confirm privacy policy is checked
        if (!privacy) {
            NewsletterForm.handleFormError(
                FormUtils.errorList.PRIVACY_POLICY_ERROR
            );
            return false;
        }

        // Terms checkbox only appears on /firefox/ios/testflight/ page.
        if (terms && !terms.checked) {
            NewsletterForm.handleFormError(
                FormUtils.errorList.LEGAL_TERMS_ERROR
            );
            return false;
        }

        return true;
    },

    subscribe: (e) => {
        const url = form.getAttribute('action');
        const email = form.querySelector('input[type="email"]').value;

        e.preventDefault();
        e.stopPropagation();

        // Disable form fields until POST has completed.
        FormUtils.disableFormFields(form);

        // Clear any prior messages that might have been displayed.
        FormUtils.clearFormErrors(form);

        // Perform client side form field validation.
        if (!NewsletterForm.validateFields()) {
            return;
        }

        const params = NewsletterForm.serialize();

        FormUtils.postToBasket(
            email,
            params,
            url,
            NewsletterForm.handleFormSuccess,
            NewsletterForm.handleFormError
        );
    },

    init: () => {
        form = document.getElementById('newsletter-form');

        if (!form) {
            return;
        }

        form.addEventListener('submit', NewsletterForm.subscribe, false);
    }
};

export default NewsletterForm;
