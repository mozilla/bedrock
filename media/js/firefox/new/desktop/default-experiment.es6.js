/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../../base/experiment-utils.es6';
import {
    meetsExperimentCriteria,
    experimentCookieID
} from './default-experiment-criteria.es6';

const href = window.location.href;
const ATTRIBUTION_COOKIE_CODE_ID = 'moz-stub-attribution-code';
const ATTRIBUTION_COOKIE_SIGNATURE_ID = 'moz-stub-attribution-sig';

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

/**
 * Sets a cookie to remember which experiment variation has been seen.
 * @param {Object} traffic cop config
 */
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

/**
 * Removes existing stub attribution cookie
 */
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
            id: experimentCookieID,
            variant: 'control'
        });
    } else if (
        href.indexOf('experiment=download-as-default&variation=treatment') !==
        -1
    ) {
        /**
         * People only enter into this experiment if they do not already have stub
         * attribution data. However there's still the edge case that someone may
         * not download right away, and return back later. If that's the case,
         * then we don't know if they checked or unchecked the input originally.
         * To circumvent this, we delete their original attribution cookie,
         * which will then be created fresh when they load the page again.
         */
        if (
            window.Mozilla.Cookies.hasItem(ATTRIBUTION_COOKIE_CODE_ID) ||
            window.Mozilla.Cookies.hasItem(ATTRIBUTION_COOKIE_SIGNATURE_ID)
        ) {
            removeAttributionCookie();
        }

        window.dataLayer.push({
            event: 'experiment_view',
            id: experimentCookieID,
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
                id: experimentCookieID,
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
