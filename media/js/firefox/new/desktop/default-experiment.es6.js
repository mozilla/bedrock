/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../../base/experiment-utils.es6';
import { meetsExperimentCriteria } from './default-experiment-criteria.es6';

const href = window.location.href;
const expID = 'download-as-default';
const ATTRIBUTION_COOKIE_CODE_ID = 'moz-stub-attribution-code';
const ATTRIBUTION_COOKIE_SIGNATURE_ID = 'moz-stub-attribution-sig';

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

function setVariationCookie(exp) {
    // set cookie to expire in 24 hours
    const date = new Date();
    date.setTime(date.getTime() + 1 * 24 * 60 * 60 * 1000);
    const expires = date.toUTCString();

    window.Mozilla.Cookies.setItem(
        exp.id,
        exp.chosenVariation,
        expires,
        undefined,
        undefined,
        false,
        'lax'
    );
}

function removeAttributionCookie() {
    window.Mozilla.Cookies.removeItem(
        ATTRIBUTION_COOKIE_CODE_ID,
        '/',
        undefined,
        false,
        'lax'
    );

    window.Mozilla.Cookies.removeItem(
        ATTRIBUTION_COOKIE_SIGNATURE_ID,
        '/',
        undefined,
        false,
        'lax'
    );
}

const init = () => {
    if (
        href.indexOf('experiment=download-as-default&variation=control') !== -1
    ) {
        window.dataLayer.push({
            event: 'experiment_view',
            id: expID,
            variant: 'control'
        });
    } else if (
        href.indexOf('experiment=download-as-default&variation=treatment') !==
        -1
    ) {
        // If has experiment cookie
        // and if has attribution cookie
        // then delete attribution cookie as it will  get set fresh on variation page load
        if (
            window.Mozilla.Cookies.hasItem(expID) &&
            (window.Mozilla.Cookies.hasItem(ATTRIBUTION_COOKIE_CODE_ID) ||
                window.Mozilla.Cookies.hasItem(ATTRIBUTION_COOKIE_SIGNATURE_ID))
        ) {
            removeAttributionCookie();
        }

        window.dataLayer.push({
            event: 'experiment_view',
            id: expID,
            variant: 'treatment'
        });
    } else if (TrafficCop) {
        if (
            isApprovedToRun() &&
            meetsExperimentCriteria(
                window.site.platform,
                window.location.search
            )
        ) {
            const cop = new TrafficCop({
                id: expID,
                variations: {
                    'experiment=download-as-default&variation=control': 25,
                    'experiment=download-as-default&variation=treatment&utm_source=www.mozilla.org&utm_campaign=SET_DEFAULT_BROWSER': 25
                }
            });
            cop.init();

            setVariationCookie(cop);
        }
    }
};

init();
