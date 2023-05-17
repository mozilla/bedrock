/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import '@mozilla-protocol/core/protocol/js/details';

const toggleGrid = document.querySelector('.toggle-grid');

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
