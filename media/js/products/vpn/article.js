/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // Init hero image carousel for large viewports only.
    var hasMediaQueries = typeof window.matchMedia !== 'undefined';

    if (!hasMediaQueries || !window.matchMedia('(min-width: 768px)').matches) {
        return;
    }

    var index = 0;
    var heroImage = document.querySelector('.vpn-hero-image');
    setInterval(function () {
        index = (index + 1) % 5;
        heroImage.setAttribute('data-illustration', 'n-' + (index + 1));
    }, 5000);
})();
