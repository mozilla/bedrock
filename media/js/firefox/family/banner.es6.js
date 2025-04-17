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
    // GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'banner',
        action: 'display',
        name: 'dad-jokes-banner',
        non_interaction: true
    });
    // allow dismissal click
    dadJokesBannerClose.addEventListener('click', hideBanner);
}

function hideBanner() {
    // Ensure all elements are available before proceeding
    if (!dadJokesBanner || !dadJokesBannerClose || !emojiWrapper) {
        return;
    }

    // GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'banner',
        action: 'accept',
        name: 'dad-jokes-banner'
    });

    // Disable button to prevent repeated clicks
    dadJokesBannerClose.setAttribute('disabled', 'true');
    dadJokesBannerClose.removeEventListener('click', hideBanner);

    // start emoji animation according to user preference
    const userPrefAnimation = motionAllowed()
        ? 'animate-bubbles'
        : 'animate-emoji-appearance';
    emojiWrapper.classList.add(userPrefAnimation);

    // Wait for emoji animation to finish, then fade out and remove the banner
    emojiWrapper.addEventListener('animationend', onEmojiAnimationEnd, {
        once: true
    });
}

function onEmojiAnimationEnd() {
    // Start the fade-out AFTER emoji animation completes
    dadJokesBanner.classList.remove('fade-in-banner');
    dadJokesBanner.classList.add('fade-out-banner');

    // Wait for fade-out to complete before removing from DOM
    dadJokesBanner.addEventListener('transitionend', onFadeOutTransitionEnd, {
        once: true
    });
}

function onFadeOutTransitionEnd() {
    dadJokesBanner.remove();
}

const init = function () {
    // set element references
    dadJokesBanner = document.getElementById('dad-jokes-banner');
    dadJokesBannerClose = document.getElementById('dad-jokes-banner-close');

    if (!dadJokesBanner || !dadJokesBannerClose) {
        return;
    }

    // Create emoji wrapper with images
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
