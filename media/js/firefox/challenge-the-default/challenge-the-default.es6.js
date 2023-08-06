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
const animatedButton = document.querySelector('.animated-button');
const heroEasterEgg = document.querySelector('.hero-easter-egg');
const animatedLogos = document.querySelectorAll('.ctd-logo-sprite');
let toggleWrapper;

for (let index = 0; index < animatedLogos.length; index++) {
    const logo = animatedLogos[index];
    logo.addEventListener(
        'animationend',
        () => {
            // when animation finishes, add a 1.5s delay in between cycles of the animation
            logo.style.animation = 'null';
            setTimeout(() => {
                logo.style.animation = '';
            }, 4500);
        },
        false
    );
}

compareSelect.addEventListener(
    'change',
    function (e) {
        compareTable.dataset.selectedBrowser = e.target.value || 'chrome';
    },
    false
);

kittenButton.addEventListener(
    'click',
    function (e) {
        e.preventDefault();
        MzpModal.createModal(e.target, kittenModal, {
            closeText: 'Close modal',
            className: 'kitten-modal-overlay',
            onDestroy: () => {
                kittenButton.focus();
            }
        });
    },
    false
);

function allTogglesChecked() {
    const small = document.querySelector('.toggle-grid.small');
    const medium = document.querySelector('.toggle-grid.medium');
    // check which toggle wrapper is active
    toggleWrapper = document.querySelector('.toggle-grid.small');
    if (getComputedStyle(small).display === 'grid') {
        toggleWrapper = small;
    } else if (getComputedStyle(medium).display === 'grid') {
        toggleWrapper = medium;
    } else {
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
    element.addEventListener(
        'change',
        function (e) {
            // check if the click was on the middle input, and if so remove the animation class
            const input = e.target;
            if (input.parentElement.classList.contains('middle')) {
                input.parentElement.classList.toggle('animate-slide');
            }
            checkToggles();
        },
        false
    );
}

heroClose.addEventListener(
    'click',
    function () {
        if (!window.Mozilla.Utils.allowsMotion()) {
            return;
        }
        const heroWrapper = document.querySelector('.hero-wrapper');
        heroWrapper.classList.add('animate-close');
        heroWrapper.classList.remove('animate-pop-in');
        heroEasterEgg.classList.toggle('hidden');

        setTimeout(() => {
            heroWrapper.classList.add('animate-pop-in');
            heroWrapper.classList.remove('animate-close');
            heroEasterEgg.classList.toggle('hidden');
        }, 4500);
    },
    false
);

// On click, animate the "It's Wednesday Dudes" screen
animatedButton.addEventListener('click', isWednesday, false);

function isWednesday() {
    let lizardImage;
    const wednesdayWrapper = document.querySelector('.c-animated-button');
    wednesdayWrapper.classList.add('animate-wednesday');

    const isWednesday = new Date().getDay() === 3;

    if (isWednesday) {
        lizardImage = wednesdayWrapper.querySelector('.is-wednesday');
    } else {
        lizardImage = wednesdayWrapper.querySelector('.not-wednesday');
    }
    lizardImage.style.display = 'block';
    setTimeout(function () {
        lizardImage.style.display = 'none';
        wednesdayWrapper.classList.remove('animate-wednesday');
    }, 5000);
}

// check toggle state on page load
checkToggles();
