/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * Initialize Protocol Navigation.
 */
(function () {
    'use strict';

    if (
        typeof window.MzpMenu === 'undefined' ||
        typeof window.MzpNavigation === 'undefined'
    ) {
        return;
    }

    var hasMediaQueries = typeof window.matchMedia !== 'undefined';

    function handleOnMenuOpen() {
        if (
            !hasMediaQueries ||
            !window.matchMedia('(min-width: 768px)').matches
        ) {
            return;
        }
    }

    window.MzpMenu.init({
        onMenuOpen: handleOnMenuOpen
    });

    window.MzpNavigation.init();
})();
