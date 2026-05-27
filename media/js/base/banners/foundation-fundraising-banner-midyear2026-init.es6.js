/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MozBanner from './mozilla-banner.es6';
import TrafficCop from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../base/experiment-utils.es6.js';

MozBanner.init('foundation-fundraising-banner-midyear2026', true);

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

const href = window.location.href;

const initTrafficCop = () => {
    if (href.indexOf('v=') !== -1) {
        if (href.indexOf('v=2') !== -1) {
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'MOFO-donation-green',
                variant: 'mofo-donation-v2'
            });
        } else if (href.indexOf('v=3') !== -1) {
            // GA4
            window.dataLayer.push({
                event: 'experiment_view',
                id: 'MOFO-donation-orange',
                variant: 'mofo-donation-v3'
            });
        }
    } else if (TrafficCop) {
        const cop = new TrafficCop({
            variations: {
                'v=2': 50, // MoFo donate green
                'v=3': 50 // MoFo donate orange
            }
        });
        cop.init();
    }
};

// Avoid entering automated tests into random experiments.
const applyVariant = () => {
    const bannerImage = document.querySelector('.c-banner-image');

    if (href.indexOf('v=2') !== -1) {
        bannerImage.setAttribute(
            'src',
            '/media/img/banners/fundraiser/banner-green.png'
        );
        document
            .querySelector('.c-banner-fundraising')
            .classList.add('c-variant-green');
    } else if (href.indexOf('v=3') !== -1) {
        // Orange variant
        bannerImage.setAttribute(
            'src',
            '/media/img/banners/fundraiser/banner-orange.png'
        );
        document
            .querySelector('.c-banner-fundraising')
            .classList.add('c-variant-orange');
    }
};

if (isApprovedToRun()) {
    initTrafficCop();
}

// Run on page load (after TrafficCop may have redirected back)
applyVariant();
