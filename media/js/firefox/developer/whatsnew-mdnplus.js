/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    var hidden;
    var visibilityChange;
    var mandalaElement = document.getElementById('mandala');

    // Check for support of the Page Visbility API
    if (typeof document.hidden !== 'undefined') {
        hidden = 'hidden';
        visibilityChange = 'visibilitychange';
    } else {
        return;
    }

    // If the page is hidden, stop the mandala.
    // If the page is visible, animate the mandala.
    function handleVisibilityChange() {
        if (document[hidden]) {
            mandalaElement.classList.remove('animated');
        } else {
            mandalaElement.classList.add('animated');
            // Stop animating after five minutes
            setTimeout(function () {
                mandalaElement.classList.remove('animated');
            }, 300000);
        }
    }

    // Check if the browser doesn't support addEventListener or the Page Visibility API
    if (
        typeof document.addEventListener === 'undefined' ||
        hidden === undefined
    ) {
        return;
    } else {
        // Handle page visibility change
        document.addEventListener(
            visibilityChange,
            handleVisibilityChange,
            false
        );
    }

    window.Mozilla.run(handleVisibilityChange);
})(window.Mozilla);
