/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';

    var things = document.querySelectorAll('.wnp-main-title .do');
    var index = 0;

    (function () {
        things[0].style.opacity = '1';
        setInterval(function () {
            things[index].style.opacity = '0';
            index = (index + 1) % things.length;
            things[index].style.opacity = '1';
        }, 1600);
    }());

})();
