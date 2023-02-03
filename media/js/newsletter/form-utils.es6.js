/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const BASKET_COOKIE_ID = 'nl-token';

const UUID_REGEX =
    /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/;

const errorList = {
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

let _userToken;

const FormUtils = {
    errorList,

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

    /**
     * Looks for UUID token in the page URL. If found, removes token
     * from the URL and stores in a cookie. If not found, look for an
     * existing cookie with a token. If still not found, reject.
     * @returns {Promise}
     */
    checkForUserToken: () => {
        return new window.Promise((resolve, reject) => {
            const urlToken = FormUtils.getURLToken(window.location);

            // If the page URL contains a token, grab it and replace history.
            if (urlToken) {
                FormUtils.setUserToken(urlToken);
                FormUtils.removeTokenFromURL(window.location, urlToken);
            }

            const token = FormUtils.getUserToken();

            if (!token) {
                reject();
            } else {
                resolve();
            }
        });
    },

    /**
     * Add disabled property to all form fields.
     * @param {HTMLFormElement} form
     */
    disableFormFields: (form) => {
        const formFields = form.querySelectorAll('input, button, select');

        for (let i = 0; i < formFields.length; i++) {
            formFields[i].disabled = true;
        }
    },

    /**
     * Remove disabled property to all form fields.
     * @param {HTMLFormElement} form
     */
    enableFormFields: (form) => {
        const formFields = form.querySelectorAll('input, button, select');

        for (let i = 0; i < formFields.length; i++) {
            formFields[i].disabled = false;
        }
    },

    getURLToken: (location) => {
        const token = location.pathname.match(UUID_REGEX);

        if (token && token.length) {
            return token[0];
        }

        return '';
    },

    /**
     * Gets the user's UUID token.
     * Looks to cookie first, falling back to local variable.
     * Will return an empty string if token is not a valid format.
     * @returns {String}
     */
    getUserToken: () => {
        let token;

        const cookiesEnabled =
            typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();

        if (cookiesEnabled) {
            token = Mozilla.Cookies.getItem(BASKET_COOKIE_ID);
        } else {
            token = _userToken;
        }

        if (FormUtils.isValidToken(token)) {
            return token;
        } else {
            return '';
        }
    },

    /**
     * Validates the supplied token matches the expected UUID format.
     * @param {String} token
     * @returns {Boolean}
     */
    isValidToken: (token) => {
        if (typeof token !== 'string') {
            return false;
        }

        return UUID_REGEX.test(token);
    },

    /**
     * Returns true if URL string starts with http(s) or a relative path.
     * @param {String} url
     * @returns {Boolean}
     */
    isWellFormedURL: (url) => {
        const absolute = /^https?:\/\//;
        const relative = /^\//;
        return absolute.test(url) || relative.test(url);
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
        xhr.setRequestHeader(
            'Content-type',
            'application/x-www-form-urlencoded'
        );
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.timeout = 5000;
        xhr.ontimeout = errorCallback;
        xhr.responseType = 'json';
        xhr.send(params);
    },

    /**
     * Removes Basket UUID token from page URL path and updates browser history.
     * Note: this function will remove *everything* from the path *after* the token.
     * Only query parameters will be preserved.
     * @param {Object} location (e.g. window.location)
     * @param {String} token
     */
    removeTokenFromURL: (location, token) => {
        if (
            typeof token === 'string' &&
            location.pathname.lastIndexOf(token) !== -1
        ) {
            const url =
                location.pathname.substring(
                    0,
                    location.pathname.lastIndexOf(token)
                ) + location.search;

            try {
                window.history.replaceState(null, null, url);
            } catch (e) {
                // do nothing
            }
        }
    },

    /**
     * Sets a cookie with the user's UUID token. If cookies are disabled,
     * then falls back to storing the token to a variable in memory.
     * @param {String} token
     */
    setUserToken: (token) => {
        if (FormUtils.isValidToken(token)) {
            const cookiesEnabled =
                typeof Mozilla.Cookies !== 'undefined' &&
                Mozilla.Cookies.enabled();

            if (cookiesEnabled) {
                const date = new Date();
                date.setTime(date.getTime() + 1 * 3600 * 1000); // expiry in 1 hour.
                const expires = date.toUTCString();

                Mozilla.Cookies.setItem(
                    BASKET_COOKIE_ID,
                    token,
                    expires,
                    '/',
                    undefined,
                    false,
                    'lax'
                );
            } else {
                _userToken = token;
            }
        }
    },

    /**
     * Helper function to serialize form data for XHR request.
     * @param {HTMLElement} form
     * @returns {String} query string
     */
    serialize: (form) => {
        const q = [];
        for (let i = 0; i < form.elements.length; i++) {
            const elem = form.elements[i];
            if (elem.name) {
                q.push(elem.name + '=' + encodeURIComponent(elem.value));
            }
        }
        return q.join('&');
    },

    /**
     * Helper function that strips HTML tags from text form input.
     * @param {String} text
     * @returns {String}
     */
    stripHTML: (text) => {
        const div = document.createElement('div');
        div.innerHTML = decodeURIComponent(text);
        return div.textContent;
    }
};

export default FormUtils;
