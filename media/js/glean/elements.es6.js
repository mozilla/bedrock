/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import * as element from '../libs/glean/element.js';

function clickEvent(obj) {
    if (typeof obj !== 'object' && typeof obj.label !== 'string') {
        return;
    }

    const data = {
        label: obj.label,
        type: '',
        position: ''
    };

    if (typeof obj.type === 'string') {
        data['type'] = obj.type;
    }

    if (typeof obj.position === 'string') {
        data['position'] = obj.position;
    }

    try {
        element.clicked.record(data);
    } catch (e) {
        //do nothing
    }
}

export { clickEvent };
