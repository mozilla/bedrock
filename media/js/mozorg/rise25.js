/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

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
        // eslint-disable-next-line
        //  heroImage.style.transform = 'translate(' + amountMovedX + 'px,' + amountMovedY + 'px)'
    }

    // function handleMouseLeave() {
    //     for (var index = 0; index < images.length; index++) {
    //         var image = images[index];
    //         image.style.transform ='translate(0, 0)';
    //     }
    // }

    heroImageWrapper.addEventListener('mousemove', handleMouseMove);
    // heroImageWrapper.addEventListener("mouseleave", handleMouseLeave);
})();
