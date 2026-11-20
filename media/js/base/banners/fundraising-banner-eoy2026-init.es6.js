/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MozBanner from './mozilla-banner.es6';

if (typeof window.dataLayer === 'undefined') {
    window.dataLayer = [];
}

// The template sets a per-campaign id, so read it rather than hard-coding it.
const banner = document.querySelector('.c-banner-fundraising');

if (banner) {
    MozBanner.init(banner.id, true);
}
