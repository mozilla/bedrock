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

const defaultParams = {
    utm_source: '',
    utm_campaign: '',
    utm_medium: '',
    utm_content: '',
    entrypoint_experiment: '',
    entrypoint_variation: '',
    experiment: '',
    variation: '',
    v: '', // short param for 'variation'
    xv: '' // short param for 'experience version'.
};

function initPageView() {
    page.viewed.set();
    page.path.set(Utils.getPathFromUrl());
    page.locale.set(Utils.getLocaleFromUrl());
    page.referrer.set(Utils.getReferrer());
    page.httpStatus.set(Utils.getHttpStatus());

    const params = Utils.getQueryParamsFromURL();
    const finalParams = {};

    // validate only known & trusted query params
    // for inclusion in Glean metrics.
    for (const param in defaultParams) {
        if (Object.prototype.hasOwnProperty.call(defaultParams, param)) {
            const allowedChars = /^[\w/.%-]+$/;
            let v = params.get(param);

            if (v) {
                v = decodeURIComponent(v);
                finalParams[param] = allowedChars.test(v) ? v : '';
            } else {
                finalParams[param] = '';
            }

            page.queryParams[param].set(finalParams[param]);
        }
    }

    pageViewPing.submit();
}

function pagePing(obj) {
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

export { initPageView, pagePing };
