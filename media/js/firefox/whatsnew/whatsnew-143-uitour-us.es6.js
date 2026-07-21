/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function init() {
    Mozilla.UITour.ping(() => {
        // show new tab CTA
        document.body.classList.add('wnp-uitour');

        // new tab CTA should open new tab
        const newtabCta = document.querySelector('.wnp143-uitour-newtab');

        if (typeof window.dataLayer === 'undefined') {
            window.dataLayer = [];
        }

        newtabCta.addEventListener(
            'click',
            (e) => {
                e.preventDefault();

                window.dataLayer.push({
                    event: 'widget_action',
                    type: 'new tab',
                    action: 'open',
                    label: 'Personalize my new tab'
                });

                Mozilla.UITour.showNewTab();
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
