/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function () {
    'use strict';

    function onLoad() {
        window.Mozilla.Banner.init('firefox-app-store-banner', true);
    }

    if (
        window.Mozilla.run &&
        window.site &&
        !window.Mozilla.Client.isFirefox &&
        (window.site.platform === 'android' || window.site.platform === 'ios')
    ) {
        window.Mozilla.run(onLoad);
    }
})();
