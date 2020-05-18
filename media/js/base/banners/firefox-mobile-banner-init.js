// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

(function() {
    'use strict';

    function onLoad() {

        var platform = window.site.platform;

        if (platform === 'android') {
            window.Mozilla.Banner.init('firefox-mobile-android');
        } else if (platform === 'ios') {
            window.Mozilla.Banner.init('firefox-mobile-ios');
        }
    }

    window.Mozilla.run(onLoad);

})();
