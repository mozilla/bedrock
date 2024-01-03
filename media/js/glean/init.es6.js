/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import Glean from '@mozilla/glean/web';
import GleanMetrics from '@mozilla/glean/metrics';
import { BrowserSendBeaconUploader } from '@mozilla/glean/web';
import { recordCustomPageMetrics, pageEvent } from './page.es6';
import { clickEvent } from './elements.es6';
import Utils from './utils.es6';

function initGlean() {
    const pageUrl = window.location.href;
    const endpoint = 'https://www.mozilla.org';
    const channel = pageUrl.startsWith(endpoint) ? 'prod' : 'non-prod';

    /**
     * Ensure telemetry coming from automated testing is tagged
     * https://mozilla.github.io/glean/book/reference/debug/sourceTags.html
     */
    if (pageUrl.includes('automation=true')) {
        Glean.setSourceTags(['automation']);
    }

    Glean.initialize('bedrock', Utils.isTelemetryEnabled(), {
        channel: channel,
        serverEndpoint: endpoint,
        httpClient: BrowserSendBeaconUploader // use sendBeacon since Firefox does not yet support keepalive using fetch()
    });

    /**
     * Record some additional page metrics that
     * aren't in the default page_load event.
     */
    recordCustomPageMetrics();

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
}

/**
 * Creates global helpers on the window.Mozilla.Glean
 * namespace, so that external JS bundles can trigger
 * custom interaction events.
 */
function initHelpers() {
    if (typeof window.Mozilla === 'undefined') {
        window.Mozilla = {};
    }

    window.Mozilla.Glean = {
        pageEvent: (obj) => {
            pageEvent(obj);
        },
        clickEvent: (obj) => {
            clickEvent(obj);
        }
    };
}

initGlean();
initHelpers();
