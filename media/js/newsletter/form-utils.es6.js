/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * Reallly primative validation (e.g a@a)
 * matches built-in validation in Firefox
 * @param {email}
 */
function checkEmailValidity(email) {
    return /\S+@\S+/.test(email);
}

export { checkEmailValidity };
