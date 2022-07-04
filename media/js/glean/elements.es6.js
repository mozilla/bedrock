/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { interaction as interactionPing } from '../libs/glean/pings.js';
import * as element from '../libs/glean/element.js';

function interaction(obj) {
    if (typeof obj !== 'object' && typeof obj.label !== 'string') {
        return;
    }

    const data = {
        label: obj.label
    };

    if (typeof obj.type === 'string') {
        data['type'] = obj.type;
    }

    if (typeof obj.position === 'string') {
        data['position'] = obj.position;
    }

    try {
        element.clicked.record(data);
        interactionPing.submit();
    } catch (e) {
        //do nothing
    }
}

function getElementAttributes(e) {
    let el = e.target;

    // If the node isn't a link or button, traverse upward
    // in case this is a nested child element.
    if (
        (el.nodeName !== 'A' || el.nodeName !== 'BUTTON') &&
        Element.prototype.closest
    ) {
        el = el.closest('a') || el.closest('button');
    }

    if (!el) {
        return;
    }

    // Check all link and button elements for data attributes.
    if (el.nodeName === 'A' || el.nodeName === 'BUTTON') {
        const ctaText = el.getAttribute('data-cta-text');
        const linkName = el.getAttribute('data-link-name');
        const linkType = el.getAttribute('data-link-type');

        // CTA link clicks
        if (ctaText) {
            const type = el.getAttribute('data-cta-type');
            const position = el.getAttribute('data-cta-position');
            interaction({
                label: ctaText,
                type: type,
                position: position
            });
        }
        // Firefox Download link clicks
        else if (linkType && linkType === 'download') {
            const os = el.getAttribute('data-download-os');
            const name = el.getAttribute('data-display-name');
            const position = el.getAttribute('data-download-location');

            if (os) {
                const label = `Firefox Download ${os}`;
                interaction({
                    label: label,
                    type: name,
                    position: position
                });
            }
        }
        // Older format links
        else if (linkName) {
            const position = el.getAttribute('data-link-position');
            interaction({
                label: linkName,
                type: linkType,
                position: position
            });
        }
    }
}

function bindElementClicks() {
    document
        .querySelector('body')
        .addEventListener('click', getElementAttributes, false);
}

function unbindElementClicks() {
    document
        .querySelector('body')
        .removeEventListener('click', getElementAttributes, false);
}

export { bindElementClicks, unbindElementClicks };
