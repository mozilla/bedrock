/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MozBanner from './mozilla-banner.es6';

function onLoad() {
    MozBanner.init('firefox-app-store-banner', true);
}

if (
    window.Mozilla.run &&
    window.site &&
    !window.Mozilla.Client.isFirefox &&
    (window.site.platform === 'android' || window.site.platform === 'ios')
) {
    window.Mozilla.run(onLoad);
}
