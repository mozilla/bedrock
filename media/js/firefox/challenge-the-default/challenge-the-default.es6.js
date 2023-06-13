/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import '@mozilla-protocol/core/protocol/js/details';
import MzpModal from '@mozilla-protocol/core/protocol/js/modal';

const compareSelect = document.querySelector('.mobile-select');
const compareTable = document.querySelector('.comparison-table');
const cookieButton = compareTable.querySelector('.cookie-button');
const cookieModal = document.querySelector('.cookie-modal');
const toggles = document.querySelectorAll('.toggle input');

compareSelect.addEventListener('change', function (e) {
    compareTable.dataset.selectedBrowser = e.target.value || 'chrome';
});

cookieButton.addEventListener('click', function (e) {
    MzpModal.createModal(e.target, cookieModal, {
        closeText: 'close modal but in german'
    });
});

function allTogglesChecked() {
    // check which toggle wrapper is active
    let toggleWrapper = document.querySelector('.toggle-grid.small');
    if (getComputedStyle(toggleWrapper).display === 'none') {
        toggleWrapper = document.querySelector('.toggle-grid.large');
    }
    const currentToggles = toggleWrapper.querySelectorAll('.toggle input');
    // check if all currently visible toggles are checked
    return Array.from(currentToggles).every(({ checked }) => checked);
}

// whenever a toggle is switched, check to see if all of the toggles are switched to true
for (let index = 0; index < toggles.length; index++) {
    const element = toggles[index];
    element.addEventListener('change', function () {
        if (allTogglesChecked()) {
            document
                .querySelector('.wednesday-wrapper')
                .classList.add('active');
        }
    });
}
