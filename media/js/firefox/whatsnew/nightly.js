/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    // Link to `about:preferences#experimental` via UItour.
    const experimentsLink = document.querySelector('.nightly-experiments-link');

    if (experimentsLink) {
        experimentsLink.addEventListener('click', (e) => {
            e.preventDefault();
            window.Mozilla.UITour.openPreferences('experimental');
        });
    }
})();
