/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import * as page from '../libs/glean/page.js';

function pageEvent(obj) {
    if (typeof obj !== 'object' && typeof obj.label !== 'string') {
        return;
    }

    const data = {
        label: obj.label,
        type: ''
    };

    if (typeof obj.type === 'string') {
        data['type'] = obj.type;
    }

    try {
        if (
            typeof obj.nonInteraction === 'boolean' &&
            obj.nonInteraction === true
        ) {
            page.nonInteraction.record(data);
        } else {
            page.interaction.record(data);
        }
    } catch (e) {
        //do nothing
    }
}

export { pageEvent };
