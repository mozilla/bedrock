/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import '@mozilla-protocol/core/protocol/js/details';
import MzpModal from '@mozilla-protocol/core/protocol/js/modal';

const toggleGrid = document.querySelector('.toggle-grid');
// beacuse of the way the modal grid is set up, there are multiple modal buttons in the DOM
const modalButtons = document.querySelectorAll('.modal-btn');
const content = document.querySelector('.mzp-u-modal-content');

function debounce(func, wait, immediate) {
    let timeout;
    return function () {
        const context = this;
        const args = arguments;
        const later = () => {
            timeout = null;
            if (!immediate) {
                func.apply(context, args);
            }
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) {
            func.apply(context, args);
        }
    };
}

function fillGrid() {
    const gridComputedStyle = getComputedStyle(toggleGrid);
    // get number of grid rows
    const gridRowCount = gridComputedStyle
        .getPropertyValue('grid-template-rows')
        .split(' ').length;
    // get number of grid columns
    const gridColumnCount = gridComputedStyle
        .getPropertyValue('grid-template-columns')
        .split(' ').length;

    const toggleAmount = gridRowCount * gridColumnCount;

    if (toggleAmount) {
        for (let index = 0; index < toggleAmount; index++) {
            toggleGrid.insertAdjacentHTML(
                'beforeend',
                `<label class="toggle" for="toggle-${index}">
                    <input type="checkbox" name="toggle" id="toggle-${index}" class="toggle-input" />
                    <span class="toggle-display"></span>
                </label>`
            );
        }
    }
}

function emptyGrid() {
    while (toggleGrid.firstChild) {
        toggleGrid.removeChild(toggleGrid.firstChild);
    }
}

window.addEventListener(
    'resize',
    debounce(function () {
        emptyGrid();
        fillGrid();
    }, 100)
);

fillGrid();

for (let index = 0; index < modalButtons.length; index++) {
    const button = modalButtons[index];
    button.addEventListener(
        'click',
        (e) => {
            e.preventDefault();
            MzpModal.createModal(e.target, content, {
                title: 'Von Anfang an für alle',
                className: 'ctd-modal',
                closeText: 'Close modal'
            });
        },
        false
    );
}
