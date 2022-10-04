/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

let dadJokesBanner;
let dadJokesBannerClose;
// let dadJokesBannerButton;
let dadJokesEyeroll;

function showBanner() {
    // remove unneeded event listener
    document.removeEventListener('scroll', showBanner);
    // show banner (potentially use setTimeout?)
    dadJokesBanner.setAttribute('aria-hidden', 'false');
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
    // hide banner
    dadJokesBannerClose.style.opacity = 0;
    dadJokesEyeroll.style.opacity = 1;
    setTimeout(function () {
        dadJokesBanner.setAttribute('aria-hidden', 'true');
    }, 600);
    // remove unusable event listener
    dadJokesBannerClose.removeEventListener('click', hideBanner);
    // dadJokesEyeroll.style.display = 'block';
}

const init = function () {
    // set element references
    dadJokesBanner = document.getElementById('dad-jokes-banner');
    dadJokesBannerClose = document.getElementById('dad-jokes-banner-close');

    dadJokesEyeroll = document.getElementById('dad-jokes-eyeroll');
    // add event listeners
    document.addEventListener('scroll', showBanner);
};

export default init;
