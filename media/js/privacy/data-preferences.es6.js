/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const preferenceCookieID = 'moz-1st-party-data-opt-out';
const prefStatus = document.querySelector('.data-preference-status');
const statusText = prefStatus.querySelector('.data-preference-text');
let optOutText;
let optInText;

function updateStatus() {
    if (hasOptedOut()) {
        statusText.innerText = optOutText;
        prefStatus.classList.add('is-opted-out');
        prefStatus.classList.remove('is-opted-in');
    } else {
        statusText.innerText = optInText;
        prefStatus.classList.add('is-opted-in');
        prefStatus.classList.remove('is-opted-out');
    }
}

function doOptOut() {
    const date = new Date();
    const cookieDuration = 365 * 24 * 60 * 60 * 1000; // 1 year expiration
    date.setTime(date.getTime() + cookieDuration);
    Mozilla.Cookies.setItem(
        preferenceCookieID,
        'true',
        date.toUTCString(),
        '/',
        null,
        false,
        'lax'
    );

    updateStatus();
}

function doOptIn() {
    Mozilla.Cookies.removeItem(preferenceCookieID, '/', null);
    updateStatus();
}

function hasOptedOut() {
    return Mozilla.Cookies.hasItem(preferenceCookieID);
}

function bindEvents() {
    const optOutButton = document.querySelector('.js-opt-out-button');
    const optInButton = document.querySelector('.js-opt-in-button');

    optOutButton.addEventListener(
        'click',
        (e) => {
            e.preventDefault();
            doOptOut();
        },
        false
    );

    optInButton.addEventListener(
        'click',
        (e) => {
            e.preventDefault();
            doOptIn();
        },
        false
    );
}

if (
    typeof Mozilla.Cookies !== 'undefined' &&
    Mozilla.Cookies.enabled() &&
    typeof Mozilla.Utils !== 'undefined'
) {
    optOutText = window.Mozilla.Utils.trans('notification-opt-out');
    optInText = window.Mozilla.Utils.trans('notification-opt-in');

    updateStatus();
    bindEvents();
    prefStatus.classList.add('show');
}
