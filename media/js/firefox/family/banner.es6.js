/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

let dadJokesBanner;
let dadJokesBannerClose;
let emojiWrapper;

function motionAllowed() {
    return (
        'matchMedia' in window &&
        window.matchMedia('(prefers-reduced-motion: no-preference)').matches
    );
}

function showBanner() {
    // remove unneeded event listener
    document.removeEventListener('scroll', showBanner);
    dadJokesBanner.classList.remove('hide-banner');
    dadJokesBanner.classList.add('fade-in-banner');
    // allow dismissal click
    dadJokesBannerClose.addEventListener('click', hideBanner);
}

function hideBanner() {
    window.dataLayer.push({
        eLabel: 'Banner Dismissal',
        'data-banner-name': 'firefox-for-families-banner',
        'data-banner-dismissal': '1',
        event: 'in-page-interaction'
    });
    // start emoji animation according to user preference
    const userPrefAnimation = motionAllowed()
        ? 'animate-bubbles'
        : 'animate-emoji-appearance';
    emojiWrapper.classList.add(userPrefAnimation);
    dadJokesBannerClose.setAttribute('disabled', 'true');
    // fade out banner
    emojiWrapper.addEventListener('animationend', (e) => fadeOutBanner(e));
    // remove banner from accessibility tree
    dadJokesBanner.addEventListener('transitionend', removeBanner);
    // remove unusable event listeners
    dadJokesBannerClose.removeEventListener('click', hideBanner);
    emojiWrapper.removeEventListener('animationend', (e) => fadeOutBanner(e));
    dadJokesBanner.removeEventListener('transitionend', removeBanner);
}

function fadeOutBanner(e) {
    if (!e.target.nextSibling) {
        dadJokesBanner.classList.remove('fade-in-banner');
    }
}

function removeBanner() {
    dadJokesBanner.classList.add('hide-banner');
}

const init = function () {
    // set element references
    dadJokesBanner = document.getElementById('dad-jokes-banner');
    dadJokesBannerClose = document.getElementById('dad-jokes-banner-close');

    // create emoji wrapper and images inside banner
    const eyeroll = '/media/img/firefox/family/banner-emoji-eyeroll.svg';
    const grimace = '/media/img/firefox/family/banner-emoji-grimace.svg';

    const emojis = [eyeroll, grimace, grimace, eyeroll, eyeroll];

    emojiWrapper = document.createElement('div');
    emojiWrapper.setAttribute('class', 'emoji-wrapper');

    emojis.forEach((src) => {
        const img = document.createElement('img');
        img.setAttribute('src', src);
        img.setAttribute('alt', '');
        emojiWrapper.appendChild(img);
    });

    dadJokesBanner
        .querySelector('.c-dad-jokes-banner-button-wrapper')
        .appendChild(emojiWrapper);

    // add event listeners
    document.addEventListener('scroll', showBanner);
};

export default init;
