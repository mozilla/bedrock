/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import '@mozilla-protocol/core/protocol/js/details';
import MzpModal from '@mozilla-protocol/core/protocol/js/modal';

const compareSelect = document.querySelector('.mobile-select');
const compareTable = document.querySelector('.comparison-table');
const kittenButton = document.querySelector('.kitten-button');
const kittenModal = document.querySelector('.kitten-modal');
const toggles = document.querySelectorAll('.toggle input');
const heroClose = document.querySelector('.close');
let toggleWrapper;

compareSelect.addEventListener('change', function (e) {
    compareTable.dataset.selectedBrowser = e.target.value || 'chrome';
});

kittenButton.addEventListener('click', function (e) {
    MzpModal.createModal(e.target, kittenModal, {
        closeText: 'Close modal',
        className: 'kitten-modal-overlay'
    });
});

function allTogglesChecked() {
    // check which toggle wrapper is active
    toggleWrapper = document.querySelector('.toggle-grid.small');
    if (getComputedStyle(toggleWrapper).display === 'none') {
        toggleWrapper = document.querySelector('.toggle-grid.large');
    }
    const currentToggles = toggleWrapper.querySelectorAll('.toggle input');
    // check if all currently visible toggles are checked
    return Array.from(currentToggles).every(({ checked }) => checked);
}

function checkToggles() {
    if (allTogglesChecked()) {
        document.querySelector('.c-ctd-toggles').classList.add('all-checked');
    } else {
        document
            .querySelector('.c-ctd-toggles')
            .classList.remove('all-checked');
    }
}

// whenever a toggle is switched, check to see if all of the toggles are switched to true
for (let index = 0; index < toggles.length; index++) {
    const element = toggles[index];
    element.addEventListener('change', checkToggles);
}

heroClose.addEventListener('click', function () {
    const heroWrapper = document.querySelector('.hero-wrapper');
    heroWrapper.classList.add('animate-close');
    heroWrapper.classList.remove('animate-pop-in');

    setTimeout(() => {
        heroWrapper.classList.add('animate-pop-in');
        heroWrapper.classList.remove('animate-close');
    }, 3000);
});

// check toggle state on page load
checkToggles();
