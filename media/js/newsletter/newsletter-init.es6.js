/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MzpNewsletter from '@mozilla-protocol/core/protocol/js/newsletter';

const successCustomCallback = () => {
    const newsletters = Array.from(
        document.querySelectorAll(
            ".mzp-c-newsletter-form input[name='newsletters']:checked"
        )
    ).map((newsletter) => newsletter.value);

    if (window.dataLayer) {
        // UA
        window.dataLayer.push({
            event: 'newsletter-signup-success',
            newsletter: newsletters
        });
        // GA4
        for (let i = 0; i < newsletters.length; ++i) {
            window.dataLayer.push({
                event: 'newsletter_subscribe',
                newsletter_id: newsletters[i]
            });
        }
    }

    // Glean
    if (typeof window.Mozilla.Glean !== 'undefined') {
        window.Mozilla.Glean.pageEvent({
            label: 'newsletter-sign-up-success',
            type: newsletters.join(', ')
        });
    }
};

MzpNewsletter.init(successCustomCallback);
