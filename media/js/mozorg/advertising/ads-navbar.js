/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';
    const mainNavBar = document.querySelector('.m24-navigation-refresh');
    const subNavBar = document.querySelector('.mza-c-sub-navigation');
    const mainSection = document.querySelector('#mza-main');

    const options = {
        root: null,
        threshold: 0
    };

    const callback = (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                subNavBar.classList.add('is-absolute');
                subNavBar.classList.remove('is-sticky');
                mainSection.classList.remove('no-padding');
            } else {
                subNavBar.classList.add('is-sticky');
                subNavBar.classList.remove('is-absolute');
                mainSection.classList.add('no-padding');
            }
        });
    };

    Mozilla.Utils.onDocumentReady(() => {
        const footer = document.querySelector('.moz24-footer');

        const observer = new IntersectionObserver(callback, options);
        observer.observe(mainNavBar);
        observer.observe(footer);
    });
})();
