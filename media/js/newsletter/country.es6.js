/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FormUtils from './form-utils.es6';

let _form;
let _countrySelect;

const CountryForm = {
    handleFormError: () => {
        FormUtils.enableFormFields(_form);
        _form.querySelector('.mzp-c-form-errors').classList.remove('hidden');
        _form
            .querySelector('.error-try-again-later')
            .classList.remove('hidden');
    },

    handleFormSuccess: () => {
        document
            .querySelector('.country-newsletter-content')
            .classList.add('hidden');
        document
            .querySelector('.country-newsletter-thanks')
            .classList.remove('hidden');
    },

    redirectToRecoveryPage: () => {
        const recoveryUrl = _form.getAttribute('data-recovery-url');

        if (FormUtils.isWellFormedURL(recoveryUrl)) {
            window.location.href = recoveryUrl;
        }
    },

    serialize: () => {
        return `country=${_countrySelect.value}`;
    },

    validateFields: () => {
        // Check for country selection value.
        if (!_countrySelect.value) {
            CountryForm.handleFormError();
            return false;
        }

        return true;
    },

    getFormActionURL: () => {
        const token = FormUtils.getUserToken();
        return `${_form.getAttribute('action')}${token}/`;
    },

    subscribe: (e) => {
        const url = CountryForm.getFormActionURL();

        e.preventDefault();
        e.stopPropagation();

        // Disable form fields until POST has completed.
        FormUtils.disableFormFields(_form);

        // Clear any prior messages that might have been displayed.
        FormUtils.clearFormErrors(_form);

        // Perform client side form field validation.
        if (!CountryForm.validateFields()) {
            return;
        }

        const params = CountryForm.serialize();

        FormUtils.postToBasket(
            null,
            params,
            url,
            CountryForm.handleFormSuccess,
            CountryForm.handleFormError
        );
    },

    init: () => {
        _form = document.getElementById('country-newsletter-form');
        _countrySelect = _form.querySelector('select[name="country"]');

        if (!_form) {
            return;
        }

        const urlToken = FormUtils.getURLToken(window.location);

        // If the page URL contains a token, grab it and replace history.
        if (urlToken) {
            FormUtils.setUserToken(urlToken);
            FormUtils.removeTokenFromURL(window.location, urlToken);
        }

        const token = FormUtils.getUserToken();

        // if there's no locally stored token, redirect to recovery page.
        if (!token) {
            CountryForm.redirectToRecoveryPage();
        }

        _form.addEventListener('submit', CountryForm.subscribe, false);
    }
};

export default CountryForm;
