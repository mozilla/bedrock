/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// eslint-disable-next-line

(function () {
    'use strict';
    var backLink = document.getElementById('go-back');

    // Issue 9642
    if (!backLink) {
        return;
    }

    // Hides back button if there is no previous page to go back to.
    if (window.history.length > 1) {
        backLink.classList.remove('hide-back');
    }

    backLink.addEventListener('click', function () {
        window.history.back();
    });
})();
