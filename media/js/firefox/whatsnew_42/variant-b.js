/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function(Mozilla) {
    'use strict';

    function registerTabVisibility() {
        window.dataLayer.push({
            'event': 'whatsnew-interactions',
            'interaction': 'tab-visible'
        });
    }

    Mozilla.HighlightTarget.init('.button-flat-dark');

    // register first time tab becomes visible
    if (document.hidden) {
        $(document).one('visibilitychange.whatsnew', registerTabVisibility);
    } else {
        registerTabVisibility();
    }

})(window.Mozilla);
