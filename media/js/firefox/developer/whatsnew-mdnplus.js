/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    var stopAnimTimeout;
    var mandalaElement = document.getElementById('mandala');

    // Check for support of the Page Visbility API
    if (typeof document.hidden === 'undefined') {
        return;
    }

    // If the page is hidden, stop the mandala.
    // If the page is visible, animate the mandala.
    function handleVisibilityChange() {
        if (document.hidden) {
            mandalaElement.classList.remove('animated');
            clearTimeout(stopAnimTimeout);
        } else {
            mandalaElement.classList.add('animated');
            // Stop animating after five minutes
            stopAnimTimeout = setTimeout(function () {
                mandalaElement.classList.remove('animated');
            }, 300000);
        }
    }

    document.addEventListener(
        'visibilitychange',
        handleVisibilityChange,
        false
    );

    window.Mozilla.run(handleVisibilityChange);
})(window.Mozilla);
