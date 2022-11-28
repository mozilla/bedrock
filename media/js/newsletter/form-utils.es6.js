/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const errorList = {
    EMAIL_INVALID_ERROR: 'Invalid email address',
    EMAIL_UNKNOWN_ERROR: 'Email address not known',
    NEWSLETTER_ERROR: 'Newsletter not selected',
    COUNTRY_ERROR: 'Country not selected',
    LANGUAGE_ERROR: 'Language not selected',
    PRIVACY_POLICY_ERROR: 'Privacy policy not checked',
    LEGAL_TERMS_ERROR: 'Terms not checked'
};

/**
 * Really primitive validation (e.g a@a)
 * matches built-in validation in Firefox
 * @param {String} email
 * @returns {Boolean}
 */
function checkEmailValidity(email) {
    return /\S+@\S+/.test(email);
}

/**
 * Hide all visible form error labels.
 * @param {HTMLFormElement} form
 */
function clearFormErrors(form) {
    const errorMsgs = form.querySelectorAll('.mzp-c-form-errors li');

    form.querySelector('.mzp-c-form-errors').classList.add('hidden');

    for (let i = 0; i < errorMsgs.length; i++) {
        errorMsgs[i].classList.add('hidden');
    }
}

/**
 * Add disabled property to all form fields.
 * @param {HTMLFormElement} form
 */
function disableFormFields(form) {
    const formFields = form.querySelectorAll('input, button, select');

    for (let i = 0; i < formFields.length; i++) {
        formFields[i].disabled = true;
    }
}

/**
 * Remove disabled property to all form fields.
 * @param {HTMLFormElement} form
 */
function enableFormFields(form) {
    const formFields = form.querySelectorAll('input, button, select');

    for (let i = 0; i < formFields.length; i++) {
        formFields[i].disabled = false;
    }
}

function postToBasket(email, params, url, successCallback, errorCallback) {
    const xhr = new XMLHttpRequest();

    // Emails used in automation for page-level integration tests
    // should avoid hitting basket directly.
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
            errorCallback();
        }
    };

    xhr.onerror = errorCallback;
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.timeout = 5000;
    xhr.ontimeout = errorCallback;
    xhr.responseType = 'json';
    xhr.send(params);
}

/**
 * Helper function to serialize form data for XHR request.
 * @param {HTMLElement} form
 * @returns {String} query string
 */
function serialize(form) {
    const q = [];
    for (let i = 0; i < form.elements.length; i++) {
        const elem = form.elements[i];
        if (elem.name) {
            q.push(elem.name + '=' + encodeURIComponent(elem.value));
        }
    }
    return q.join('&');
}

export {
    checkEmailValidity,
    clearFormErrors,
    errorList,
    disableFormFields,
    enableFormFields,
    postToBasket,
    serialize
};
