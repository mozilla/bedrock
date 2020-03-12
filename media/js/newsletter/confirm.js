/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // Back link to preferences page
    var backLink = document.querySelector('.c-updated-back-link');

    if (backLink) {
        backLink.addEventListener('click', function(e) {
            e.preventDefault();

            window.history.back();
        });
    }

    // Lazyload images
    Mozilla.LazyLoad.init();
})();
