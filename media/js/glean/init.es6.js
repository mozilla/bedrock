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

let gleanInitialized = false;
let pageEventLoaded = false;

function initGlean(telemetryEnabled) {
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

    Glean.initialize('bedrock', telemetryEnabled, {
        channel: channel,
        serverEndpoint: endpoint,
        httpClient: BrowserSendBeaconUploader // use sendBeacon since Firefox does not yet support keepalive using fetch()
    });

    gleanInitialized = true;
}

function initPageLoadEvent() {
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

    pageEventLoaded = true;
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

/**
 * initGlean() should always be called, even if cookie consent is not given.
 * When `hasConsent === true`, Glean will send analytics pings as normal.
 * When `hasConsent === false`, Glean will instead sent `deletion-request`
 * pings to automatically remove a client's telemetry data.
 */
window.addEventListener(
    'mozConsentStatus',
    (e) => {
        const hasConsent = e.detail.analytics;

        if (!gleanInitialized) {
            initGlean(hasConsent);
        } else {
            Glean.setUploadEnabled(hasConsent);
        }

        if (hasConsent && !pageEventLoaded) {
            initPageLoadEvent();
        }
    },
    false
);

initHelpers();
