/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';

    var h = document.documentElement;

    // remove js class from body if IE 8 or below
    if (window.site.platform === 'windows' && /MSIE\s8\./.test(navigator.userAgent)) {
        h.className = h.className.replace(/\bjs\b/, 'no-js');
    }
})();
