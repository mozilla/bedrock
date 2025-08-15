/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function init() {
    Mozilla.UITour.ping(() => {
        // show main CTA
        document.body.classList.add('wnp-uitour');

        // main CTA should open Protections Dashboard
        const button = document.querySelector('.wnp-main-cta .mzp-c-button');

        button.addEventListener(
            'click',
            (e) => {
                e.preventDefault();

                if (typeof window.dataLayer === 'undefined') {
                    window.dataLayer = [];
                }

                window.dataLayer.push({
                    event: 'widget_action',
                    type: 'protection report',
                    action: 'open',
                    label: 'View your dashboard'
                });

                Mozilla.UITour.showProtectionReport();
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
