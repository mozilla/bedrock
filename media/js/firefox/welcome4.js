/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';

    var content = document.querySelector('.mzp-u-modal-content');
    var buttons = document.getElementsByClassName('js-modal-link');

    for (var i = 0, len = buttons.length; i < len; i++) {
        var button = buttons[i];
        button.addEventListener('click', openModal);
        button.setAttribute('aria-role', 'button');
    }

    function openModal(e) {
        e.preventDefault();

        Mzp.Modal.createModal(e.target, content, {
            closeText: 'Close modal'
        });
    }

})();
