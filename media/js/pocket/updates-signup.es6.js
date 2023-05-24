/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FormUtils from '../newsletter/form-utils.es6';

let form;

const UpdatesForm = {
    handleFormError: (errorData) => {
        let error;

        FormUtils.enableFormFields(form);

        form.querySelector('.mzp-c-form-errors').classList.remove('hidden');
        if (errorData && errorData['detail']['email']) {
            error = form.querySelector('.error-email-invalid');
        } else {
            // backend error, tampered form/missing fields
            error = form.querySelector('.error-try-again-later');
        }
        if (error) {
            error.classList.remove('hidden');
        }
    },

    handleFormSuccess: () => {
        const formWrapper = document.getElementById(
            'pocket-updates-form-wrapper'
        );
        const thanksWrapper = document.getElementById('pocket-updates-thanks');
        formWrapper.classList.add('hidden');
        thanksWrapper.classList.remove('hidden');
    },
    postToBackend: (payload, url, successCallback, errorCallback) => {
        const xhr = new XMLHttpRequest();

        xhr.onload = function (e) {
            let response = e.target.response || e.target.responseText;

            if (typeof response !== 'object') {
                response = JSON.parse(response);
            }

            if (response) {
                if (
                    response.status === 'success' &&
                    e.target.status >= 200 &&
                    e.target.status < 300
                ) {
                    successCallback();
                } else {
                    errorCallback(response);
                }
            } else {
                errorCallback();
            }
        };
        xhr.onerror = errorCallback;
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-type', 'application/json');
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.timeout = 5000;
        xhr.ontimeout = errorCallback;
        xhr.responseType = 'json';
        xhr.send(JSON.stringify(payload));
    },

    extractUTMsFromQuerystring: () => {
        const utms = {};
        const soughtParams = ['campaign', 'medium', 'source'];
        // Grab the UTM params for the hidden form fields and sanitise
        let key, value;
        for ([key, value] of UpdatesForm.getSearchParams()) {
            value = decodeURIComponent(value);
            const strippedKey = key.replace('utm_', '');
            const allowableRegex = RegExp(/^[\w/.%-]{1,100}$/);
            if (soughtParams.includes(strippedKey)) {
                // We only use the param if its value matches the regex
                if (value.search(allowableRegex) !== -1) {
                    utms[strippedKey] = value;
                }
            }
        }
        return utms;
    },

    subscribe: (e) => {
        // Start with the payload from the form, but then also
        // populate campaign, medium and source keys from the URL
        const formPayload = Object.fromEntries(new FormData(form).entries());
        const utms = UpdatesForm.extractUTMsFromQuerystring();

        const completePayload = Object.assign(formPayload, utms);
        const url = form.getAttribute('action');

        e.preventDefault();
        e.stopPropagation();

        // Disable form fields until POST has completed.
        FormUtils.disableFormFields(form);

        // Clear any prior messages that might have been displayed.
        FormUtils.clearFormErrors(form);

        // Submit to the server
        UpdatesForm.postToBackend(
            completePayload,
            url,
            UpdatesForm.handleFormSuccess,
            UpdatesForm.handleFormError
        );
    },

    getSearchParams: () => {
        // isolated to make easier to mock in tests
        return new URL(window.location.href).searchParams;
    },

    init: () => {
        form = document.getElementById('updates-form');
        if (!form) {
            return;
        }
        form.addEventListener('submit', UpdatesForm.subscribe, false);
    }
};

export default UpdatesForm;
