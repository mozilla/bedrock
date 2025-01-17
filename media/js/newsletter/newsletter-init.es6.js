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
        // GA4
        for (let i = 0; i < newsletters.length; ++i) {
            window.dataLayer.push({
                event: 'newsletter_subscribe',
                newsletter_id: newsletters[i]
            });
        }
    }
};

MzpNewsletter.init(successCustomCallback);
