/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MozConsentBanner from './mozilla-consent-banner.es6.js';

const banner = document.querySelector('.moz-consent-banner');

function debounce(func, delay) {
    let timer;
    return function () {
        clearTimeout(timer);
        timer = setTimeout(() => {
            func.apply(this, arguments);
        }, delay);
    };
}

function updateBodyPadding() {
    if (window.innerHeight > 600) {
        document.body.style.paddingBottom = banner.offsetHeight + 'px';
    } else {
        document.body.style.paddingBottom = '0px';
    }
}

const onResize = debounce(updateBodyPadding, 200);

function openBanner() {
    // Bind event listeners
    document
        .getElementById('moz-consent-banner-button-accept')
        .addEventListener('click', MozConsentBanner.onAcceptClick, false);
    document
        .getElementById('moz-consent-banner-button-reject')
        .addEventListener('click', MozConsentBanner.onRejectClick, false);

    // Show banner
    document.getElementById('moz-consent-banner').classList.add('is-visible');

    setTimeout(updateBodyPadding, 0);
    window.addEventListener('resize', onResize, false);
}

function closeBanner() {
    // Unbind event listeners
    document
        .getElementById('moz-consent-banner-button-accept')
        .removeEventListener('click', MozConsentBanner.onAcceptClick, false);
    document
        .getElementById('moz-consent-banner-button-reject')
        .removeEventListener('click', MozConsentBanner.onRejectClick, false);

    // Hide banner
    document
        .getElementById('moz-consent-banner')
        .classList.remove('is-visible');

    document.body.style.paddingBottom = '0';
    window.removeEventListener('resize', onResize, false);
}

// Make sure to bind open and close events before calling init().
window.addEventListener('mozConsentOpen', openBanner, false);
window.addEventListener('mozConsentClose', closeBanner, false);

MozConsentBanner.init({
    helper: window.Mozilla.Cookies,
    defaultConsent: true
});
