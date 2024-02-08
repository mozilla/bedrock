/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function init() {
    'use strict';

    Mozilla.UITour.ping(() => {
        // main CTA toggles reader mode
        const button = document.querySelector('.wnp-main-cta .mzp-c-button');

        button.addEventListener(
            'click',
            (e) => {
                e.preventDefault();

                Mozilla.UITour.toggleReaderMode();
            },
            false
        );

        // force show reader mode icon in Firefox UI bar
        Mozilla.UITour.forceShowReaderIcon();

        // show reader mode icon again on visibility change
        // see https://github.com/mozilla/bedrock/issues/13484
        document.addEventListener(
            'visibilitychange',
            () => {
                if (!document.hidden) {
                    Mozilla.UITour.forceShowReaderIcon();
                }
            },
            false
        );
    });
}

if (
    typeof window.Mozilla.Client !== 'undefined' &&
    typeof window.Mozilla.UITour !== 'undefined' &&
    window.Mozilla.Client.isFirefoxDesktop
) {
    init();
}
