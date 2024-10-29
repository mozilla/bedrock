/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrackScroll from './datalayer-trackscroll.es6';

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

window.Mozilla.TrackScroll = TrackScroll;

window.addEventListener('scroll', TrackScroll.onScroll, false);
