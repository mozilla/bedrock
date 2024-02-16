/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import DataPreferencesCookie from './data-preferences-cookie.es6';

const prefStatus = document.querySelector('.data-preference-status');
const statusText = prefStatus.querySelector('.data-preference-text');
const optOutButton = document.querySelector('.js-opt-out-button');
const optInButton = document.querySelector('.js-opt-in-button');
let optOutText;
let optInText;

function updateStatus() {
    if (DataPreferencesCookie.hasOptedOut()) {
        statusText.innerText = optOutText;
        prefStatus.classList.add('is-opted-out');
        prefStatus.classList.remove('is-opted-in');
        optOutButton.disabled = true;
        optInButton.disabled = false;
    } else {
        statusText.innerText = optInText;
        prefStatus.classList.add('is-opted-in');
        prefStatus.classList.remove('is-opted-out');
        optOutButton.disabled = false;
        optInButton.disabled = true;
    }
}

function bindEvents() {
    optOutButton.addEventListener(
        'click',
        (e) => {
            e.preventDefault();
            DataPreferencesCookie.doOptOut();
            updateStatus();
        },
        false
    );

    optInButton.addEventListener(
        'click',
        (e) => {
            e.preventDefault();
            DataPreferencesCookie.doOptIn();
            updateStatus();
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
