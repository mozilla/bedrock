/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { pageEvent } from './page.es6';
import { clickEvent } from './elements.es6';
import Utils from './utils.es6';

if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

Utils.bootstrapGlean();

/**
 * Creates global helpers on the window.Mozilla.Glean
 * namespace, so that external JS bundles can trigger
 * custom interaction events.
 */
window.Mozilla.Glean = {
    pageEvent: (obj) => {
        pageEvent(obj);
    },
    clickEvent: (obj) => {
        clickEvent(obj);
    }
};
