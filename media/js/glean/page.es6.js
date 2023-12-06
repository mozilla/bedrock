/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import GleanMetrics from '@mozilla/glean/metrics';
import * as page from '../libs/glean/page.js';
import Utils from './utils.es6';

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

    const params = Utils.getQueryParamsFromUrl();
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

    /**
     * Manually call Glean's default page_load event. Here
     * we override `url` and `referrer` since we need to
     * apply some custom logic to these values before they
     * are sent.
     */
    GleanMetrics.pageLoad({
        url: Utils.getUrl(),
        referrer: Utils.getReferrer()
    });

    /**
     * This old page hit event can be removed once we're
     * confident that the new page_load event is working
     * as expected.
     */
    page.hit.record();
}

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

export { initPageView, pageEvent };
