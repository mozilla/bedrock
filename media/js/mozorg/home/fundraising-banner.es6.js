/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import MozBanner from '../../base/banners/mozilla-banner.es6';

function onLoad() {
    MozBanner.init('fundraising-banner');
}

window.Mozilla.run(onLoad);
