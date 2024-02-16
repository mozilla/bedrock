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

    function initNavButton() {
        if (typeof Mozilla.Client === 'undefined') {
            return false;
        }

        var nav = document.querySelector('.c-navigation');

        // Nav should be present on page.
        if (nav) {
            // Add a CSS hook for animating the nav button (issue #9009)
            nav.classList.add('nav-button-is-ready');
        }
    }

    initNavButton();

    window.MzpMenu.init({
        onMenuOpen: handleOnMenuOpen
    });

    window.MzpNavigation.init();
})();
