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
    window.Mozilla.Client &&
    window.Mozilla.Client.isMobile &&
    !window.Mozilla.Client.isFirefox
) {
    window.Mozilla.run(onLoad);
}
