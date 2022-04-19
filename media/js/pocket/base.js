/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * General DOM ready handler applied to all pages in base template.
 */
(function () {
    'use strict';

    // The `loaded` class is used mostly as a signal for functional tests to run.
    window.addEventListener(
        'load',
        function () {
            document.getElementsByTagName('html')[0].classList.add('loaded');
        },
        false
    );
})();
