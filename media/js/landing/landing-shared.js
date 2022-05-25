/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    // test to see if users are clicking on the workmark in the header of the SEM landing pages
    function handleWorkmarkClick(event) {
        var label = event.target.innerText;
        window.dataLayer.push({
            event: 'sem-wordmark-click',
            label: label + ' SEM landing page'
        });
    }

    var wordmark = document.querySelector('.sem-landing-nav-icon');
    wordmark.addEventListener('click', handleWorkmarkClick);
})();
