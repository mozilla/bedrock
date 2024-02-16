/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const relayAnimationWrapper = document.querySelector('.wnp-relay-animation');
const relayDropdown = document.querySelector('.relay-dropdown');
const relayInput = document.querySelector('.relay-input');
const inputText = document.querySelector('.relay-input span');

if (window.Mozilla.Utils.allowsMotion()) {
    relayAnimationWrapper.addEventListener('animationend', (e) => {
        if (e.animationName === 'pop-in') {
            relayAnimationWrapper.classList.add('click-animation');
        }

        if (e.animationName === 'click' && e.target === relayAnimationWrapper) {
            relayDropdown.classList.add('active');
            setTimeout(() => {
                inputText.textContent = '';
            }, 500);
        }
    });

    relayDropdown.addEventListener(
        'animationend',
        (e) => {
            if (e.animationName === 'button-press') {
                relayDropdown.style.opacity = 0;
                relayInput.classList.add('animation-end');
                inputText.textContent = 'hxty0y40@mozmail.com';
            }
        },
        false
    );
} else {
    document.querySelector('.wnp-content-main').classList.add('static');
}

(function () {
    Mozilla.Client.getFxaDetails(function (details) {
        if (details.setup) {
            document
                .querySelector('.wnp-content-main')
                .classList.add('fxa-active');
        }
    });
})();
