/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    var santaLocator;
    var status = document.getElementById('status');
    var error = document.getElementById('error');
    var panda = document.getElementById('panda');
    var cta = document.getElementById('cta');
    var time = Math.floor(Math.random() * 2000) + 8000; // randomize delay between 8-10 seconds

    function onLoad() {
        clearTimeout(santaLocator);
        error.classList.remove('show');
        status.classList.add('show');

        santaLocator = setTimeout(function () {
            status.classList.remove('show');
            error.classList.add('show');
            panda.classList.add('show');
            cta.classList.add('show');
        }, time);
    }

    window.Mozilla.run(onLoad);
})(window.Mozilla);
