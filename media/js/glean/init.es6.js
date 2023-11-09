/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import Glean from '@mozilla/glean/web';
import { initPageView, pageEvent } from './page.es6';
import { clickEvent } from './elements.es6';
import Utils from './utils.es6';

const shouldInitialize = Utils.hasValidURLScheme(window.location.href);

function initGlean() {
    const pageUrl = window.location.href;
    const endpoint = 'https://www.mozilla.org';
    const channel = pageUrl.startsWith('https://www.mozilla.org/')
        ? 'prod'
        : 'non-prod';

    // Ensure telemetry coming from automated testing is tagged
    // https://mozilla.github.io/glean/book/reference/debug/sourceTags.html
    if (pageUrl.includes('automation=true')) {
        Glean.setSourceTags(['automation']);
    }

    Glean.initialize('bedrock', Utils.isTelemetryEnabled(), {
        channel: channel,
        serverEndpoint: endpoint
    });
}

function initHelpers() {
    if (typeof window.Mozilla === 'undefined') {
        window.Mozilla = {};
    }

    // Create a global for external bundles to fire interaction pings.
    window.Mozilla.Glean = {
        pageEvent: (obj) => {
            if (shouldInitialize) {
                pageEvent(obj);
            }
        },
        clickEvent: (obj) => {
            if (shouldInitialize) {
                clickEvent(obj);
            }
        }
    };
}

if (shouldInitialize) {
    initGlean();
    initPageView();
}

initHelpers();
