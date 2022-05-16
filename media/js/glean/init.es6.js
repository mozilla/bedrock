/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import Glean from '@mozilla/glean/web';

import { initPageView, pageEventPing } from './page.es6';
import { bindElementClicks } from './elements.es6';
import Utils from './utils.es6';

function initGlean() {
    // Automatically console.log() pings.
    // eslint-disable-next-line no-undef
    if (process.env.GLEAN_LOG_PINGS === 'True') {
        Glean.setLogPings(true);
    }

    // Enable debug view for all non-production environments.
    // https://debug-ping-preview.firebaseapp.com/
    if (window.location.href.indexOf('https://www.mozilla.org/') === -1) {
        Glean.setDebugViewTag('moz-bedrock');
    }

    // Ensure telemetry coming from automated testing is tagged
    // https://mozilla.github.io/glean/book/reference/debug/sourceTags.html
    if (window.location.href.indexOf('automation=true') !== -1) {
        Glean.setSourceTags(['automation']);
    }

    Glean.initialize('moz-bedrock', Utils.isTelemetryEnabled(), {
        maxEvents: 1 // Set max events to 1 so pings are sent as soon as registered.
    });
}

function initPageEventHelper() {
    if (typeof window.Mozilla === 'undefined') {
        window.Mozilla = {};
    }

    // Create a global for external bundles to fire interaction pings.
    window.Mozilla.Glean = { pageEventPing };
}

initGlean();
initPageView();
initPageEventHelper();
bindElementClicks();
