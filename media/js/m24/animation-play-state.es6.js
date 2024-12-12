/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const ANIMATION_RUNNING = 'data-animation-running';

function togglePlayState(e) {
    const animationContainer = e.target.closest(`[${ANIMATION_RUNNING}]`);
    if (animationContainer.getAttribute(ANIMATION_RUNNING) === 'true') {
        animationContainer.setAttribute(ANIMATION_RUNNING, 'false');
    } else {
        animationContainer.setAttribute(ANIMATION_RUNNING, 'true');
    }
}

function init() {
    // play animations if motion is allowed
    if (window.Mozilla.Utils.allowsMotion()) {
        const animationContainers = document.querySelectorAll(
            `[${ANIMATION_RUNNING}]`
        );
        animationContainers.forEach((container) =>
            container.setAttribute(ANIMATION_RUNNING, 'true')
        );
    }

    // play or pause animations on button click
    const playStateButtons = document.querySelectorAll('.js-animation-button');
    playStateButtons.forEach((button) =>
        button.addEventListener('click', (e) => togglePlayState(e))
    );
}

init();
