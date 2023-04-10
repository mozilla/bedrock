/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    var isReduced =
        window.matchMedia('(prefers-reduced-motion: reduce)') === true ||
        window.matchMedia('(prefers-reduced-motion: reduce)').matches === true;

    var heroImageWrapper = document.querySelector('.rise25-hero-image');
    var images = heroImageWrapper.querySelectorAll('.hero-image');

    function handleMouseMove(e) {
        var amountMovedX = (e.clientX * -0.3) / 8;
        var amountMovedY = (e.clientY * -0.5) / 8;

        for (var index = 0; index < images.length; index++) {
            var image = images[index];
            image.style.transform =
                'translate(' + amountMovedX + 'px,' + amountMovedY + 'px)';
        }
    }

    if (!isReduced) {
        heroImageWrapper.addEventListener('mousemove', handleMouseMove);
    }
})();
