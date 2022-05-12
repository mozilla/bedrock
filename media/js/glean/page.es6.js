/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import * as page from '../libs/glean/page.js';
import Utils from './utils.es6';
import {
    pageView as pageViewPing,
    interaction as interactionPing,
    nonInteraction as nonInteractionPing
} from '../libs/glean/pings.js';

const validParams = [
    'utm_source',
    'utm_campaign',
    'utm_medium',
    'utm_content',
    'entrypoint_experiment',
    'entrypoint_variation',
    'experiment',
    'variation',
    'v', // short param for 'variation'
    'xv' // short param for 'experience version'.
];

function initPageView() {
    page.viewed.set();
    page.path.set(Utils.getPathFromUrl());
    page.locale.set(Utils.getLocaleFromUrl());
    page.referrer.set(Utils.getReferrer());

    const params = Utils.getQueryParamsFromURL();

    if (params) {
        // validate only known & trusted query params
        // for inclusion in Glean metrics.
        for (const param in validParams) {
            const allowedChars = /^[\w/.%-]+$/;
            const p = validParams[param];
            let v = params.get(p);

            if (v) {
                v = decodeURIComponent(v);
                if (allowedChars.test(v)) {
                    page.queryParams[p].set(v);
                }
            }
        }
    }

    pageViewPing.submit();
}

function pageEventPing(obj) {
    if (typeof obj !== 'object' && typeof obj.label !== 'string') {
        return;
    }

    const data = {
        label: obj.label
    };

    if (typeof obj.type === 'string') {
        data['type'] = obj.type;
    }

    page.pageEvent.record(data);

    if (
        typeof obj.nonInteraction === 'boolean' &&
        obj.nonInteraction === true
    ) {
        nonInteractionPing.submit();
    } else {
        interactionPing.submit();
    }
}

export { initPageView, pageEventPing };
