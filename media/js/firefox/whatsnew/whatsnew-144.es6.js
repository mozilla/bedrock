/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FxaLink from '../../base/fxa-link.es6.js';

function init() {
    // Configure FxA links for Sync etc.
    if (typeof window._SearchParams !== 'undefined') {
        FxaLink.init();
    }

    document.body
        .querySelectorAll('[data-close-notification]')
        .forEach((button) => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const notification = button.closest(
                    '.wnp-page-header-notification'
                );
                if (notification) {
                    notification.style.display = 'none';
                }
            });
        });
}

if (
    typeof window.Mozilla !== 'undefined' &&
    typeof window.Mozilla.Client !== 'undefined' &&
    window.Mozilla.Client.isFirefoxDesktop
) {
    init();
}
