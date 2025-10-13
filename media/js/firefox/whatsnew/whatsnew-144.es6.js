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
        const newtabCta = document.querySelector('.wnp144-uitour-newtab');

        if (typeof window.dataLayer === 'undefined') {
            window.dataLayer = [];
        }

        if (newtabCta) {
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
        }
    });

    document.body.querySelectorAll('[data-close-notification]').forEach((button) => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const notification = button.closest('.wnp-page-header-notification');
            if (notification) {
                notification.style.display = 'none';
            }
        });
    });
}

if (
    typeof window.Mozilla !== 'undefined' &&
    typeof window.Mozilla.Client !== 'undefined' &&
    typeof window.Mozilla.UITour !== 'undefined' &&
    window.Mozilla.Client.isFirefoxDesktop
) {
    init();
}
