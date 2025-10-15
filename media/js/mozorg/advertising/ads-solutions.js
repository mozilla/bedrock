/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';
    const modalWrappers = document.querySelectorAll('.modal-wrapper');

    modalWrappers.forEach((wrapperEl) => {
        const trigger = wrapperEl.querySelector('.modal-trigger');
        const content = wrapperEl.querySelector('.mzp-u-modal-content');

        if (trigger && content) {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                window.MzpModal.createModal(trigger, content);
            });
        }
    });

    window.MzpModal;
})();
