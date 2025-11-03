/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';
    const options = {
        root: null,
        threshold: 0.3
    };

    const callback = (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                document
                    .querySelectorAll('.mza-c-callout-bg .layer-2')
                    .forEach((image) => image.classList.add('active'));
            }
        });
    };
    const observer = new IntersectionObserver(callback, options);
    observer.observe(document.querySelector('#callout-image-trigger'));
})();
