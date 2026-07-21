/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Copy paste from https://raw.githubusercontent.com/mozilla/protocol/refs/heads/main/assets/js/protocol/newsletter.js
// With AWS-specific changes commented

let form;

const ERROR_LIST = {
    COUNTRY_ERROR: 'Country not selected',
    EMAIL_INVALID_ERROR: 'Invalid email address',
    EMAIL_UNKNOWN_ERROR: 'Email address not known',
    LANGUAGE_ERROR: 'Language not selected',
    LEGAL_TERMS_ERROR: 'Terms not checked',
    NEWSLETTER_ERROR: 'Newsletter not selected',
    NOT_FOUND: 'Not Found',
    PRIVACY_POLICY_ERROR: 'Privacy policy not checked',
    REASON_ERROR: 'Reason not selected'
};

const MzpNewsletter = {
    /**
     * Really primitive validation (e.g a@a)
     * matches built-in validation in Firefox
     * @param {String} email
     * @returns {Boolean}
     */
    checkEmailValidity: (email) => {
        return /\S+@\S+/.test(email);
    },

    /**
     * Add disabled property to all form fields. Show loading indicator.
     * @param {HTMLFormElement} form
     */
    disableFormFields: (form) => {
        const submitText = form.querySelector('.submit-text');
        const submitLoading = form.querySelector('.submit-loading');

        // Hide text and show loader
        if (submitText) {
            submitText.style.opacity = 0;
        }
        if (submitLoading) {
            submitLoading.removeAttribute('hidden');
        }

        const formFields = form.querySelectorAll('input, button, select');

        for (let i = 0; i < formFields.length; i++) {
            formFields[i].disabled = true;
        }
    },

    /**
     * Remove disabled property to all form fields. Hide loading indicator.
     * @param {HTMLFormElement} form
     */
    enableFormFields: (form) => {
        const submitText = form.querySelector('.submit-text');
        const submitLoading = form.querySelector('.submit-loading');

        // Hide loader and show text
        if (submitLoading) {
            submitLoading.setAttribute('hidden', true);
        }
        if (submitText) {
            submitText.style.opacity = 1;
        }

        const formFields = form.querySelectorAll('input, button, select');

        for (let i = 0; i < formFields.length; i++) {
            formFields[i].disabled = false;
        }
    },

    /**
     * Hide all visible form error labels.
     * @param {HTMLFormElement} form
     */
    clearFormErrors: (form) => {
        const errorMsgs = form.querySelectorAll('.mzp-c-form-errors li');

        form.querySelector('.mzp-c-form-errors').classList.add('hidden');

        for (let i = 0; i < errorMsgs.length; i++) {
            errorMsgs[i].classList.add('hidden');
        }
    },

    handleFormError: (msg) => {
        let error;

        MzpNewsletter.enableFormFields(form);

        form.querySelector('.mzp-c-form-errors').classList.remove('hidden');

        switch (msg) {
            case ERROR_LIST.EMAIL_INVALID_ERROR:
                error = form.querySelector('.error-email-invalid');
                break;
            case ERROR_LIST.NEWSLETTER_ERROR:
                error = form.querySelector('.error-newsletter-checkbox');
                break;
            case ERROR_LIST.COUNTRY_ERROR:
                error = form.querySelector('.error-select-country');
                break;
            case ERROR_LIST.LANGUAGE_ERROR:
                error = form.querySelector('.error-select-language');
                break;
            case ERROR_LIST.PRIVACY_POLICY_ERROR:
                error = form.querySelector('.error-privacy-policy');
                break;
            case ERROR_LIST.LEGAL_TERMS_ERROR:
                error = form.querySelector('.error-terms');
                break;
            default:
                error = form.querySelector('.error-try-again-later');
        }

        if (error) {
            error.classList.remove('hidden');
        }

        if (typeof MzpNewsletter.customErrorCallback === 'function') {
            MzpNewsletter.customErrorCallback(msg);
        }
    },

    handleFormSuccess: () => {
        form.classList.add('hidden');
        document.getElementById('newsletter-thanks').classList.remove('hidden');

        if (typeof MzpNewsletter.customSuccessCallback === 'function') {
            MzpNewsletter.customSuccessCallback();
        }
    },

    /**
     * Perform an AJAX POST to Basket
     * @param {String} email
     * @param {String} params (URI encoded query string)
     * @param {String} url (Basket API endpoint)
     * @param {Function} successCallback
     * @param {Function} errorCallback
     */
    postToBasket: (email, params, url, successCallback, errorCallback) => {
        const xhr = new XMLHttpRequest();

        // Emails used in automation for page-level integration tests
        // should avoid hitting server directly.
        if (email === 'success@example.com') {
            successCallback();
            return;
        } else if (email === 'failure@example.com') {
            errorCallback();
            return;
        }

        xhr.onload = function (e) {
            let response = e.target.response || e.target.responseText;

            if (typeof response !== 'object') {
                response = JSON.parse(response);
            }

            if (response) {
                if (response.status !== undefined) {
                    // BASKET response structure
                    if (
                        response.status === 'ok' &&
                        e.target.status >= 200 &&
                        e.target.status < 300
                    ) {
                        successCallback();
                    } else if (response.status === 'error' && response.desc) {
                        errorCallback(response.desc);
                    } else {
                        errorCallback();
                    }
                } else {
                    // AWS response structure
                    if (e.target.status >= 200 && e.target.status < 300) {
                        successCallback();
                    } else {
                        errorCallback();
                    }
                }
            } else {
                errorCallback();
            }
        };

        xhr.onerror = errorCallback;
        xhr.open('POST', url, true);
        xhr.setRequestHeader(
            'Content-type',
            'application/x-www-form-urlencoded'
        );
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.timeout = 10000; // increased AWS timeout
        xhr.ontimeout = errorCallback;
        xhr.responseType = 'json';
        xhr.send(params);
    },

    serialize: () => {
        // Email address
        const email = encodeURIComponent(
            form.querySelector('input[type="email"]').value
        );

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

        return `email=${email}${country}&lang=${lang}&source_url=${sourceUrl}&newsletters=${newsletters}`;
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
        if (!MzpNewsletter.checkEmailValidity(email)) {
            MzpNewsletter.handleFormError(ERROR_LIST.EMAIL_INVALID_ERROR);
            return false;
        }

        // Check for country selection value.
        if (countrySelect && !countrySelect.value) {
            MzpNewsletter.handleFormError(ERROR_LIST.COUNTRY_ERROR);
            return false;
        }

        // Check for language selection value.
        if (!lang) {
            MzpNewsletter.handleFormError(ERROR_LIST.LANGUAGE_ERROR);
            return false;
        }

        // Confirm at least one newsletter is checked
        if (newsletters.length === 0) {
            MzpNewsletter.handleFormError(ERROR_LIST.NEWSLETTER_ERROR);
            return false;
        }

        // Confirm privacy policy is checked
        if (!privacy) {
            MzpNewsletter.handleFormError(ERROR_LIST.PRIVACY_POLICY_ERROR);
            return false;
        }

        if (terms && !terms.checked) {
            MzpNewsletter.handleFormError(ERROR_LIST.LEGAL_TERMS_ERROR);
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
        MzpNewsletter.disableFormFields(form);

        // Clear any prior messages that might have been displayed.
        MzpNewsletter.clearFormErrors(form);

        // Perform client side form field validation.
        if (!MzpNewsletter.validateFields()) {
            return;
        }

        const params = MzpNewsletter.serialize();

        MzpNewsletter.postToBasket(
            email,
            params,
            url,
            MzpNewsletter.handleFormSuccess,
            MzpNewsletter.handleFormError
        );
    },

    init: (customSuccessCallback, customErrorCallback) => {
        form = document.getElementById('newsletter-form');

        let submitButton;
        let formDetails;
        let emailField;
        let formExpanded;

        function emailFormShowDetails() {
            if (!formExpanded) {
                formDetails.style.display = 'block';
                formExpanded = true;
            }
        }

        if (form) {
            submitButton = document.getElementById('newsletter-submit');
            formDetails = document.getElementById('newsletter-details');
            emailField = document.querySelector('.mzp-js-email-field');
            formExpanded =
                window.getComputedStyle(formDetails).display === 'none'
                    ? false
                    : true;

            // Expand email form on input focus or submit if details aren't visible
            emailField.addEventListener(
                'focus',
                () => {
                    emailFormShowDetails();
                },
                false
            );

            submitButton.addEventListener(
                'click',
                (e) => {
                    if (!formExpanded) {
                        e.preventDefault();
                        emailFormShowDetails();
                    }
                },
                false
            );

            form.addEventListener(
                'submit',
                (e) => {
                    if (!formExpanded) {
                        e.preventDefault();
                        emailFormShowDetails();
                    }
                },
                false
            );

            form.addEventListener('submit', MzpNewsletter.subscribe, false);

            if (typeof customSuccessCallback === 'function') {
                MzpNewsletter.customSuccessCallback = customSuccessCallback;
            }

            if (typeof customErrorCallback === 'function') {
                MzpNewsletter.customErrorCallback = customErrorCallback;
            }
        }
    }
};

module.exports = MzpNewsletter;
