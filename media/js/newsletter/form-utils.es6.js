/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * Reallly primative validation (e.g a@a)
 * matches built-in validation in Firefox
 * @param {String} email
 * @returns {Boolean}
 */
function checkEmailValidity(email) {
    return /\S+@\S+/.test(email);
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

export { checkEmailValidity, serialize };
